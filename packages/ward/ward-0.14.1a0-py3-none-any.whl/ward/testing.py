import functools
import inspect
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Callable, Dict, List, Optional, Any

from ward.errors import FixtureError
from ward.fixtures import Fixture, FixtureCache, Scope
from ward.models import Marker, SkipMarker, XfailMarker, WardMeta


def skip(func_or_reason=None, *, reason: str = None):
    if func_or_reason is None:
        return functools.partial(skip, reason=reason)

    if isinstance(func_or_reason, str):
        return functools.partial(skip, reason=func_or_reason)

    func = func_or_reason
    marker = SkipMarker(reason=reason)
    if hasattr(func, "ward_meta"):
        func.ward_meta.marker = marker
    else:
        func.ward_meta = WardMeta(marker=marker)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def xfail(func_or_reason=None, *, reason: str = None):
    if func_or_reason is None:
        return functools.partial(xfail, reason=reason)

    if isinstance(func_or_reason, str):
        return functools.partial(xfail, reason=func_or_reason)

    func = func_or_reason
    marker = XfailMarker(reason=reason)
    if hasattr(func, "ward_meta"):
        func.ward_meta.marker = marker
    else:
        func.ward_meta = WardMeta(marker=marker)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def generate_id():
    return uuid.uuid4().hex


@dataclass
class Test:
    """
    A representation of a single Ward test.
    """
    fn: Callable
    module_name: str
    id: str = field(default_factory=generate_id)
    marker: Optional[Marker] = None
    description: Optional[str] = None

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    @property
    def name(self):
        return self.fn.__name__

    @property
    def qualified_name(self):
        name = self.name or ""
        return f"{self.module_name}.{name}"

    @property
    def line_number(self):
        return inspect.getsourcelines(self.fn)[1]

    def deps(self) -> MappingProxyType:
        return inspect.signature(self.fn).parameters

    def has_deps(self) -> bool:
        return len(self.deps()) > 0

    def resolve_fixtures(self, cache: FixtureCache) -> Dict[str, Fixture]:
        """
        Resolve fixtures and return the resultant name -> Fixture dict.
        Resolved values will be stored in fixture_cache, accessible
        using the fixture cache key (See `Fixture.key`).
        """
        signature = inspect.signature(self.fn)
        default_binding = signature.bind_partial()
        if not self.has_deps():
            return {}

        default_binding.apply_defaults()

        resolved_args: Dict[str, Fixture] = {}
        for name, arg in default_binding.arguments.items():
            if hasattr(arg, "ward_meta") and arg.ward_meta.is_fixture:
                resolved = self._resolve_single_fixture(arg, cache)
            else:
                resolved = arg
            resolved_args[name] = resolved
        return resolved_args

    def _resolve_single_fixture(
        self, fixture_fn: Callable, cache: FixtureCache
    ) -> Fixture:
        fixture = Fixture(fixture_fn)

        if fixture.key in cache:
            cached_fixture = cache[fixture.key]
            if fixture.scope == Scope.Global:
                return cached_fixture
            elif fixture.scope == Scope.Module:
                if cached_fixture.last_resolved_module_name == self.module_name:
                    return cached_fixture
            elif fixture.scope == Scope.Test:
                if cached_fixture.last_resolved_test_id == self.id:
                    return cached_fixture

        # Cache miss, so update the fixture metadata before we resolve and cache it
        fixture.last_resolved_test_id = self.id
        fixture.last_resolved_module_name = self.module_name

        has_deps = len(fixture.deps()) > 0
        is_generator = fixture.is_generator_fixture
        if not has_deps:
            try:
                if is_generator:
                    fixture.gen = fixture_fn()
                    fixture.resolved_val = next(fixture.gen)
                else:
                    fixture.resolved_val = fixture_fn()
            except Exception as e:
                raise FixtureError(f"Unable to resolve fixture '{fixture.name}'") from e
            cache.cache_fixture(fixture)
            return fixture

        signature = inspect.signature(fixture_fn)
        children_defaults = signature.bind_partial()
        children_defaults.apply_defaults()
        children_resolved = {}
        for name, child_fixture in children_defaults.arguments.items():
            child_resolved = self._resolve_single_fixture(child_fixture, cache)
            children_resolved[name] = child_resolved
        try:
            if is_generator:
                fixture.gen = fixture_fn(
                    **self._resolve_fixture_values(children_resolved)
                )
                fixture.resolved_val = next(fixture.gen)
            else:
                fixture.resolved_val = fixture_fn(
                    **self._resolve_fixture_values(children_resolved)
                )
        except Exception as e:
            raise FixtureError(f"Unable to resolve fixture '{fixture.name}'") from e
        cache.cache_fixture(fixture)
        return fixture

    def _resolve_fixture_values(
        self, fixture_dict: Dict[str, Fixture]
    ) -> Dict[str, Any]:
        return {key: f.resolved_val for key, f in fixture_dict.items()}


# Tests declared with the name _, and with the @test decorator
# have to be stored in here, so that they can later be retrieved.
# They cannot be retrieved directly from the module due to name
# clashes. When we're later looking for tests inside the module,
# we can retrieve any anonymous tests from this dict.
anonymous_tests: Dict[str, List[Callable]] = defaultdict(list)


def test(description: str):
    def decorator_test(func):
        if func.__name__ == "_":
            mod_name = func.__module__
            if hasattr(func, "ward_meta"):
                func.ward_meta.description = description
            else:
                func.ward_meta = WardMeta(description=description)
            anonymous_tests[mod_name].append(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator_test
