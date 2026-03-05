"""
trye - Ergonomic exception handling for Python.

Wraps callable invocations in a Result type, capturing exceptions
as Err values instead of raising them.
"""

__version__ = "0.1.0"
__all__ = ["Ok", "Err", "Result", "trye"]

from .trye import Err, Ok, Result, trye
