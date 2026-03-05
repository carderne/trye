from collections.abc import Callable
from typing import final


@final
class Ok[T]:
    """Represents a successful result containing a value."""

    err: None = None

    def __init__(self, val: T):
        self.val = val


@final
class Err:
    """Represents a failed result containing an exception."""

    val: None = None

    def __init__(self, err: Exception):
        self.err = err


type Result[T] = Ok[T] | Err


def trye[**P, R](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Result[R]:
    """Call `f` with the given arguments, returning Ok(result) or Err(exception)."""
    try:
        return Ok(f(*args, **kwargs))
    except Exception as e:
        return Err(e)
