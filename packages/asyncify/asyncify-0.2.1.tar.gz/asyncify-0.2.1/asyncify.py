# -*- coding: utf-8 -*-
"""Asyncify your code

...or else...
"""
from asyncio import coroutine
from asyncio import get_event_loop
from functools import partial
from functools import wraps
from inspect import getmembers
from inspect import isawaitable
from inspect import isclass
from inspect import iscoroutine
from inspect import iscoroutinefunction
from inspect import isfunction
from inspect import ismethod
from inspect import ismodule
from typing import Any
from typing import Callable
from typing import TypeVar
from typing import cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def asyncify(funk: F, functions=True, classes=True) -> F:
    """ASYNCIFY STUFF"""

    @coroutine
    @wraps(funk)
    def afunk(*args, loop=None, executor=None, **kwargs):
        """WRAPPER"""
        loop = loop if loop else get_event_loop()
        pfunc = partial(funk, *args, **kwargs)
        return loop.run_in_executor(executor, pfunc)

    if ismodule(funk):
        for fname, f in getmembers(funk, isfunction):
            setattr(funk, "{}_async".format(fname), asyncify(f))
        for fname, f in getmembers(funk, isclass):
            asyncify(f)
    elif isclass(funk):
        members = [
            el
            for el in getmembers(funk)
            if not el[0].startswith("__")
            and not el[0].endswith("__")
            and not el[0].endswith("_async")
        ]
        for mem in members:
            setattr(funk, "{}_async".format(mem[0]), cast(F, mem[-1]))
        members = [
            el
            for el in getmembers(funk)
            if not el[0].startswith("__") and not el[0].endswith("__")
        ]
    elif (
        isfunction(funk)
        and not funk.__name__.endswith("_async")
        and not iscoroutinefunction(funk)
        and not iscoroutine(funk)
        and not isawaitable(funk)
    ):
        return cast(F, afunk)


a = asyncify
