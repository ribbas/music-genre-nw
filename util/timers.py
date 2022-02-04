#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time


def time_func(func, *args, **kwargs):
    t1 = time()
    result = func(*args, **kwargs)
    t2 = time()
    print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
    return result
