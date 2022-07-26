import random
import time
from typing import Any, Callable


def time_it(func: Callable[..., Any], *args: str, **kwargs: str) -> Any:

    t1 = time.time()
    result = func(*args, **kwargs)
    t2 = time.time()
    print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")

    return result


def pause(str_fmt: str, **kwargs: str) -> None:

    wait = random.uniform(1.0, 2.0)
    print(str_fmt.format(**kwargs, wait=wait))
    time.sleep(wait)
