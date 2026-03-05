from collections.abc import Callable
from typing import Never, TypeIs, final


@final
class Ok[T]:
    """Represents a successful result containing a value."""

    err: None = None

    def __init__(self, val: T):
        self.val = val

    def unwrap(self) -> T:
        """Return the contained value."""
        return self.val

    def unwrap_or(self, default: T) -> T:  # pyright:ignore[reportUnusedParameter]
        """Return the contained value."""
        return self.val


@final
class Err[T]:
    """Represents a failed result containing an exception."""

    val: None = None

    def __init__(self, err: Exception):
        self.err = err

    def unwrap(self) -> Never:
        """Raise the contained exception."""
        raise self.err

    def unwrap_or(self, default: T) -> T:
        """Return the contained value."""
        return default


type Result[T] = Ok[T] | Err[T]


def is_ok[T](result: Result[T]) -> TypeIs[Ok[T]]:
    """Check if a Result is Ok, narrowing the type."""
    return isinstance(result, Ok)


def is_err[T](result: Result[T]) -> TypeIs[Err[T]]:
    """Check if a Result is Err, narrowing the type."""
    return isinstance(result, Err)


def trye[**P, R](f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Result[R]:
    """Call `f` with the given arguments, returning Ok(result) or Err(exception)."""
    try:
        return Ok(f(*args, **kwargs))
    except Exception as e:
        return Err(e)
