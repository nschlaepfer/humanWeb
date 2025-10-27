"""Compatibility helpers for features that vary across Python versions."""

from __future__ import annotations

import sys
from dataclasses import dataclass as _dataclass
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def slotted_dataclass(_cls: T | None = None, /, **kwargs: Any) -> Callable[[T], T] | T:
    """
    Apply dataclass semantics while using `slots=True` when the runtime supports it.

    Python 3.10 introduced the `slots` parameter to `@dataclass`. When running on an
    earlier interpreter we silently drop the argument so the decorator stays usable.
    """

    if sys.version_info >= (3, 10):
        kwargs.setdefault("slots", True)
    else:
        kwargs.pop("slots", None)

    def wrap(cls: T) -> T:
        return _dataclass(cls, **kwargs)

    if _cls is None:
        return wrap
    return wrap(_cls)

