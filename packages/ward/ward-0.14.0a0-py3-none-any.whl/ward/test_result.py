from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from ward.testing import Test


class TestOutcome(Enum):
    PASS = auto()
    FAIL = auto()
    SKIP = auto()
    XFAIL = auto()  # expected fail
    XPASS = auto()  # unexpected pass


@dataclass
class TestResult:
    test: Test
    outcome: TestOutcome
    error: Optional[Exception] = None
    message: str = ""
    captured_stdout: str = ""
    captured_stderr: str = ""
