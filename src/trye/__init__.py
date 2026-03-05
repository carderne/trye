"""
trye - Ergonomic exception handling for Python.

Wraps callable invocations in a Result type, capturing exceptions
as Err values instead of raising them.
"""

__all__ = ["Ok", "Err", "Result", "is_ok", "is_err", "trye", "atrye"]

from .trye import Err, Ok, Result, atrye, is_err, is_ok, trye
