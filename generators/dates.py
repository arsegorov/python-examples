#%%
from datetime import date, datetime, timedelta
import logging
from types import NoneType
from typing import Any, Generator, Iterable, Optional, Union


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(f"{__file__.split('.')[0]}.log", mode="w")
fmtr = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] <%(filename)s> line %(lineno)s, in %(funcName)s: "
    "%(message)s"
)
fh.setFormatter(fmtr)

logger.addHandler(fh)

ZERO_DELTA = timedelta(0)


#%%
def _check_type(
    object: Any, object_description: str, types: Union[type, Iterable[type]]
) -> None:
    """If the object isn't of one of the types, logs the error and raises TypeError."""
    if not isinstance(object, types):
        error_message = (
            f"{object_description} is expected to be "
            + (
                f"one of {tuple(t.__name__ for t in types)}"
                if isinstance(types, Iterable)
                else f"'{types.__name__}'"
            )
            + f". Instead got a value of {object!r} ('{type(object).__name__}')"
        )
        # logger.error(error_message, stack_info=True)
        raise TypeError(error_message)


def dates_range(
    start_day: Union[date, str],
    stop_at: Optional[Union[date, str, int]] = None,
    interval: Union[timedelta, int] = timedelta(days=1),
) -> Generator[date, Optional[Union[date, str, int]], None]:
    try:
        _check_type(start_day, "`start_day`", (date, str))
        _check_type(stop_at, "`stop_at`", (date, str, int, NoneType))
        _check_type(interval, "`interval`", (timedelta, int))
        # Doing all the type conversions now,
        #  so that any incorrect argument formatting
        #  could be caught before proceeding
        if isinstance(start_day, str):
            start_day = datetime.strptime(start_day, "%Y-%m-%d").date()

        if isinstance(interval, int):
            interval = timedelta(days=interval)
        elif (
            interval - timedelta(days=interval.days) != ZERO_DELTA
            or interval == ZERO_DELTA
        ):
            msg = (
                "`interval` should be a non-zero integer number of days. "
                f"Instead got '{interval}'"
            )
            raise ValueError(msg)

        if isinstance(stop_at, str):
            stop_at = datetime.strptime(stop_at, "%Y-%m-%d").date()
        elif isinstance(stop_at, int):
            stop_at = start_day + interval * stop_at
    except Exception as e:
        logger.error(e.args[0], exc_info=True)
        raise e

    logger.info(
        f"Running with start_day = '{start_day}', "
        f"stop_at = '{stop_at}', "
        f"interval = '{interval.days} days'"
    )

    # If a stop day is provided,
    #  the interval should have the same direction
    #  as the direction from start to stop
    #  or be a zero interval
    if stop_at and interval.days * (stop_at - start_day).days <= 0:
        logger.warning("No dates exist in the range. Exiting")
        return

    def _in_range(d: date) -> bool:
        return (
            not stop_at
            or d == start_day
            or (d - start_day).days * (stop_at - d).days > 0
        )

    day = start_day
    while _in_range(day):
        logger.debug(f"day: '{day}', range: ['{start_day}', '{stop_at}')")
        logger.debug(f"'{day}' IN the range")

        new_stop_at = yield day

        logger.debug(f"Sent {new_stop_at!r} back to generator")

        _check_type(new_stop_at, "Value sent back", (date, str, int, NoneType))
        if isinstance(new_stop_at, str):
            stop_at = datetime.strptime(new_stop_at, "%Y-%m-%d").date()
        elif isinstance(new_stop_at, date):
            stop_at = new_stop_at
        elif isinstance(new_stop_at, int):
            stop_at = day + interval * (new_stop_at + 1) if new_stop_at >= 0 else None

        day += interval
    else:
        logger.debug(f"day: '{day}', range: ['{start_day}', '{stop_at}')")
        logger.debug(f"'{day}' NOT in the range")


#%%
def _main():
    start_day, stop_at, interval = "2021-01-01", 10, 3
    g = dates_range(start_day, stop_at, interval)
    logger.debug(
        f'Using dates_range(start_day="{start_day}", '
        f"stop_at={stop_at}, "
        f"interval={interval})"
    )
    # fh.setLevel(logging.INFO)

    guard = 1
    d = None
    for d in g:
        if guard > 10:
            break
        print(d)
        guard += 1
    else:
        msg = f"Finished the entire sequence, at '{d}'"
        print(msg)
        logger.info(msg)


#%%
if __name__ == "__main__":
    _main()
