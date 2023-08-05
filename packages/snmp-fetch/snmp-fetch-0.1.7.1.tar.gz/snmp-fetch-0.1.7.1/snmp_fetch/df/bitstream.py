"""Helper functions for dealing with variable length data in a numpy array."""

from typing import Any, Callable, List, Optional, Text, Tuple, Type, Union

import numpy as np
from mypy_extensions import Arg, KwArg

from .types.inet_address import ip
from .utils import bytes_to_int

EXTRACT_T = Callable[  # pylint: disable=invalid-name
    [Arg(Any, 'df'), Arg(Text, 'source'), KwArg(Any)], Tuple[Any, np.ndarray]
]
EXTRACT2_T = Callable[  # pylint: disable=invalid-name
    [Arg(Any, 'df'), Arg(Text, 'source'), KwArg(Any)], Tuple[Any, ...]
]
COLUMNS_T = Union[Text, List[Text]]  # pylint: disable=invalid-name
DTYPE_T = Union[Type[object], np.dtype]  # pylint: disable=invalid-name
DTYPES_T = Union[DTYPE_T, List[DTYPE_T]]  # pylint: disable=invalid-name
COMPOSABLE_T = Callable[[Text, Any], Tuple[Text, Any]]  # pylint: disable=invalid-name


def bitstream(source: Text, handler: COMPOSABLE_T) -> Callable[[Any], Any]:
    """Extract values from a structured numpy array with variable length data."""
    def _bitstream(df: Any) -> Any:
        _, df = handler(source, df)
        return df
    return _bitstream


def extract(
        f: EXTRACT_T,
        destination: COLUMNS_T,
        dtypes: Optional[DTYPES_T] = None,
        **kwargs: Any
) -> COMPOSABLE_T:
    """Extract one value from a structured numpy array with variable length data."""
    # flatten return type while enforcing strict input function that returns tail return type of an
    # numpy array
    def expand(f: EXTRACT2_T) -> EXTRACT2_T:
        def _expand(df: Any, source: Text, **kwargs: Any) -> Tuple[Any, ...]:
            results, remaining = f(df, source, **kwargs)
            if isinstance(results, tuple):
                return (*results, remaining)
            return results, remaining
        return _expand

    def _extract(source: Text, df: Any) -> Tuple[Text, Any]:
        if df.empty:
            if isinstance(destination, List) and isinstance(dtypes, List):
                for column, dtype in zip(destination, dtypes):
                    df[column] = None
                    df[column] = df[column].astype(dtype)
            else:
                df[destination] = None
                df[destination] = df[destination].astype(dtypes)
        else:
            columns = [*(destination if isinstance(destination, List) else [destination]), source]
            df[columns] = df.apply(expand(f), axis=1, result_type='expand', source=source, **kwargs)
            if dtypes is not None:
                if isinstance(destination, List) and isinstance(dtypes, List):
                    for column, dtype in zip(destination, dtypes):
                        df[column] = df[column].astype(dtype)
                else:
                    df[destination] = df[destination].astype(dtypes)
        return source, df
    return _extract


def integer(df: Any, source: Text, **kwargs: Any) -> Tuple[int, np.ndarray]:
    # pylint: disable=unused-argument
    """Extract first element of a numpy array as an integer."""
    return df[source][0], df[source][1:]


def object_identifier(df: Any, source: Text, **kwargs: Any) -> Tuple[np.ndarray, np.ndarray]:
    # pylint: disable=unused-argument
    """Extract an object identifier array as a numpy array."""
    return df[source][1:int(df[source][0])+1], df[source][int(df[source][0])+1:]


def inet_address(df: Any, source: Text, **kwargs: Any) -> Tuple[Any, np.ndarray]:
    """Extract an inet address with leading address size and possible zone."""
    default_zone = kwargs.pop('default_zone', None)
    if df[source][0] == 4:
        return (
            (ip.IPv4Address(bytes_to_int(df[source][1:5])), default_zone),
            df[source][5:]
        )
    if df[source][0] == 16:
        return (
            (ip.IPv6Address(bytes_to_int(df[source][1:17])), default_zone),
            df[source][17:]
        )
    if df[source][0] == 8:
        return (
            (ip.IPv4Address(bytes_to_int(df[source][1:9])), bytes_to_int(df[source][9:13])),
            df[source][13:]
        )
    if df[source][0] == 20:
        return (
            (ip.IPv6Address(bytes_to_int(df[source][1:17])), bytes_to_int(df[source][17:21])),
            df[source][21:]
        )
    raise TypeError('Datatype not understood')
