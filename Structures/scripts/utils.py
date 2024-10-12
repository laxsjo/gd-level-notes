from typing import *
from itertools import *
import sys
import os
import traceback
import inspect
import itertools
from decimal import *
from numbers import Number
import math

# pyright: reportCallIssue=false, reportInvalidTypeVarUse=false

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def panic(reason: str, traceback_level: int = 0) -> Never:
    location = traceback.extract_stack()[-(traceback_level + 2)]
    
    path = os.path.relpath(location.filename, os.getcwd())
    
    message = f"Paniced at '{reason}'\n"
    message += f" --> {path}:{location.lineno}"
    if location.colno is not None:
        message += f":{location.colno}"
    message += f" in {location.name}"
    
    eprint(message)
    exit(101)

def expect[T](option: T|None, message: str) -> T:
    if option is None:
        panic(message, 1)
    return option

def todo() -> Never:
    panic("reached unfinished code", 1)
    
def unreachable() -> Never:
    panic("reached unreachable code", 1)

# Cast value to Never, so that it can be assigned to any type.
def as_never(value: Any):
    return cast(Never, value)

# flattens multi-dimensional iterable one level
# ex: flatten([[1, [2, 3]], [4, 5, 6]]) = [1, [2, 3], 4, 5, 6]
def flatten[T](list: Iterable[Iterable[T]]) -> List[T]:
    # source: https://stackoverflow.com/a/952952/15507414
    return [x for xs in list for x in xs]

def as_chunks[T: Sequence[Any]](iter: T, n: int) -> List[T]:
    # cast is required because slice operation is not required to return a
    # sequence of the same type.
    # source: https://stackoverflow.com/a/68876155/15507414
    return cast(List[T], [iter[i:min(i+n, len(iter))] for i in range(0, len(iter), n)])

def map_dict_values[K, V, R](func: Callable[[V], R], dict: Dict[K, V]) -> Dict[K, R]:
    return {k: func(v) for k, v in dict.items()}

# Modify iterator such that at most n elements are returned
def shorten[T](n: int, iterable: Iterable[T]) -> Iterator[T]:
    iterator = iter(iterable)
    for _ in range(n):
        try:
            yield next(iterator)
        except StopIteration:
            return


def func_pos_args_len(func: Callable) -> int:
    # source: https://stackoverflow.com/a/57886262/15507414
    signature = inspect.signature(func)
    return sum(1 for param in signature.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD)

class Placeholder():
    pass
def placeholder():
    return Placeholder()

class Curry[**P, R]():
    args: Tuple
    func: Callable[P, R]
    def __call__(self, *args) -> R:
        arg_count = func_pos_args_len(self.func)
        placeholder_count = len(list(filter(lambda x: isinstance(x, Placeholder), self.args)))
        
        resolved_count = len(self.args) - placeholder_count + len(args)
        
        if resolved_count > arg_count:
            stored_args = f"({", ".join(map(lambda arg: "_" if isinstance(arg, Placeholder) else arg, self.args))})"
            panic(f"Too many arguments given to {self.func}, expected at most {arg_count}, got {resolved_count}. stored args = {stored_args}, args = {args}")
        
        args_iter = iter(args)
        final_args = list(itertools.chain(
            map(lambda arg: next(args_iter) if isinstance(arg, Placeholder) else arg, self.args),
            args_iter,
        ))
        return self.func(*final_args)

def curry[**P, R](func: Callable[P, R], *arguments: Any | Placeholder) -> Callable[..., R]:
    result = Curry[P, R]()
    result.args = arguments
    result.func = func
    
    return result

# ex: compose((h, g, f))(x) = h(g(f(x)))
@overload
def compose[A, B, C](functions: tuple[Callable[[B], C], Callable[[A], B]]) -> Callable[[A], C]:
    ...
@overload
def compose[A, B](functions: tuple[Callable[[Any], B], *tuple[Callable, ...], Callable[[A], Any]]) -> Callable[[A], B]:
    ...
# def compose[A, B, C](functions: tuple[Callable[[Any], C], *tuple[Callable, ...], Callable[[A], Any]]|tuple[Callable[[B], C], Callable[[A], B]]) -> Callable[[A], C]:
def compose(functions: Any) -> Any:
    # return cast(Never, None)
    outermost, *other, innermost = functions
    if len(other) == 0:
        return lambda x: outermost(innermost(x))
    else:
        first_other = other[0]
        other = other[1:]
        remaining = compose((first_other, *other, innermost))
        
        return lambda x: outermost(remaining(x))

def map_some[T, U](value: T|None, func: Callable[[T], U]) -> U|None:
    match value:
        case None:
            return None
        case _:
            return func(value)

def parse_int(input: str, base: int = 10) -> int | None:
    try:
        return int(input, base=base)
    except ValueError:
        return None

# Cast number to int if the number does not include any decimals. Otherwise
# return as float.
def num_as_minimal_type(num: float|int) -> float|int:
    if num == int(num):
        return int(num)
    else:
        return num

# Round num to nearest multiple of factor. The function allows you to control
# how a number is rounded. You could for instance round to the nearest 0.2
# increment using round_factor(num, 0.2).
def round_multiple(num: float, factor: float) -> float:
    # might contain rounding errors
    rounded_raw = Decimal(round(num / factor) * factor)
    
    num_digits = -Decimal(factor).log10().__floor__()
    return float(round(rounded_raw, num_digits))

# Wrap num into range, such that start <= result < end.
def wrap_range[T: (float,int)](num: T, start: T, end: T) -> T:
    # source: https://stackoverflow.com/a/28313586/15507414
    return start + (num - start) % (end - start)