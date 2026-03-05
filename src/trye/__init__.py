"""
trye - Ergonomic exception handling for Python.

Wraps callable invocations in a Result type, capturing exceptions
as Err values instead of raising them.
"""

__all__ = ["Ok", "Err", "Result", "is_ok", "is_err", "trye"]

from .trye import Err, Ok, Result, is_err, is_ok, trye
