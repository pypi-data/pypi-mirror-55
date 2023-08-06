import datetime
import pytz
import numpy as np
from functools import singledispatch


@singledispatch
def parse_datetime(dt) -> float:
    return dt


@parse_datetime.register
def _(dt: float) -> float:
    return dt


@parse_datetime.register
def _(dt: int):
    return float(dt)


@parse_datetime.register
def _(dt: datetime.datetime) -> float:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)
    return dt.timestamp()


@parse_datetime.register
def _(dt: str) -> float:
    return float(dt)


@parse_datetime.register
def _(dt: np.ndarray) -> np.ndarray:
    convert = {np.dtype("<M8[ns]"): lambda x: x.astype("int64") / 1e9,
               np.dtype("<M8[us]"): lambda x: x.astype("int64") / 1e6,
               np.dtype("<M8[ms]"): lambda x: x.astype("int64") / 1e3}
    dt = convert.get(dt.dtype, lambda x: x.astype("int64") / 1e0)(dt)
    return dt


@parse_datetime.register
def _(dt: list) -> list:
    return [parse_datetime(i) for i in dt]


@singledispatch
def parse_value(val) -> float:
    return float(val)
