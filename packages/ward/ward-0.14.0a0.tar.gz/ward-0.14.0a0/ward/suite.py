import io
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from typing import Generator, List

from ward.errors import FixtureError
from ward.fixtures import FixtureCache
from ward.models import Scope
from ward.test_result import TestOutcome, TestResult
from ward.testing import Test


@dataclass
class Suite:
    tests: List[Test]
    cache: FixtureCache = field(default_factory=FixtureCache)

    @property
    def num_tests(self):
        return len(self.tests)

    def generate_test_runs(self) -> Generator[TestResult, None, None]:
        previous_test_module = None
        for test in self.tests:
            if previous_test_module and test.module_name != previous_test_module:
                # We've moved into a different module, so clear out all of
                # the module scoped fixtures from the previous module.
                to_teardown = self.cache.get(
                    scope=Scope.Module, module_name=previous_test_module, test_id=None
                )
                self.cache.teardown_fixtures(to_teardown)

            marker = test.marker.name if test.marker else None
            if marker == "SKIP":
                yield TestResult(test, TestOutcome.SKIP)
                previous_test_module = test.module_name
                continue

            sout, serr = io.StringIO(), io.StringIO()
            try:
                resolved_fixtures = test.resolve_fixtures(self.cache)
                with redirect_stdout(sout), redirect_stderr(serr):
                    pass
            except FixtureError as e:
                # We can't run teardown code here because we can't know how much
                # of the fixture has been executed.
                yield TestResult(
                    test,
                    TestOutcome.FAIL,
                    e,
                    captured_stdout=sout.getvalue(),
                    captured_stderr=serr.getvalue(),
                )
                sout.close()
                serr.close()
                previous_test_module = test.module_name
                continue
            try:
                resolved_vals = {
                    k: fix.resolved_val for (k, fix) in resolved_fixtures.items()
                }

                # Run the test, while capturing output.
                with redirect_stdout(sout), redirect_stderr(serr):
                    test(**resolved_vals)

                # The test has completed without exception and therefore passed
                if marker == "XFAIL":
                    yield TestResult(
                        test,
                        TestOutcome.XPASS,
                        captured_stdout=sout.getvalue(),
                        captured_stderr=serr.getvalue(),
                    )
                else:
                    yield TestResult(test, TestOutcome.PASS)
            except Exception as e:
                # TODO: Differentiate between ExpectationFailed and other Exceptions.
                if marker == "XFAIL":
                    yield TestResult(test, TestOutcome.XFAIL, e)
                else:
                    yield TestResult(
                        test,
                        TestOutcome.FAIL,
                        e,
                        captured_stdout=sout.getvalue(),
                        captured_stderr=serr.getvalue(),
                    )
            finally:
                sout.close()
                serr.close()

            self._teardown_fixtures_scoped_to_test(test)
            previous_test_module = test.module_name

        # Take care of any additional teardown.
        self.cache.teardown_all()

    def _teardown_fixtures_scoped_to_test(self, test: Test):
        """
        Get all the test-scoped fixtures that were used to form this result,
        tear them down from the cache, and return the result.
        """
        to_teardown = self.cache.get(
            scope=Scope.Test, test_id=test.id, module_name=test.module_name
        )
        self.cache.teardown_fixtures(to_teardown)
