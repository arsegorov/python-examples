#%%
from datetime import date, datetime, timedelta
import logging
from types import NoneType
from typing import Union, Optional, Generator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("dates_range.log", mode="w")
fmtr = logging.Formatter("[%(asctime)s] <%(filename)s> line %(lineno)s, in %(funcName)s: [%(levelname)s] %(message)s")
fh.setFormatter(fmtr)

logger.addHandler(fh)

ZERO_DELTA = timedelta(0)


#%%
def dates_range(
    start_day: Union[date, str],
    stop_at: Optional[Union[date, str, int]] = None,
    interval: Union[timedelta, int] = timedelta(days=1),
) -> Generator[date, Optional[Union[date, str, int]], None]:
    if not isinstance(start_day, (date, str)):
        msg = (
            "`start_day` should be either a datetime.date or a str. "
            f"Instead got a {type(start_day).__name__}"
        )
        logger.error(msg)
        raise TypeError(msg)
    if not isinstance(stop_at, (date, str, int, NoneType)):
        msg = (
            "`stop_at` should be either a datetime.date, a str, an int or None. "
            f"Instead got a {type(stop_at).__name__}"
        )
        logger.error(msg)
        raise TypeError(msg)
    if not isinstance(interval, (timedelta, int)):
        msg = (
            "`interval` should be either a datetime.timedelta or an int. "
            f"Instead got a {type(interval).__name__}"
        )
        logger.error(msg)
        raise TypeError(msg)

    try:
        # Doing all the type conversions now,
        #  so that any incorrect argument formatting
        #  could be caught before proceeding
        if isinstance(start_day, str):
            start_day = datetime.strptime(start_day, "%Y-%m-%d").date()

        if isinstance(interval, int):
            interval = timedelta(days=interval)
        elif (
            interval - timedelta(days=interval.days) != ZERO_DELTA or interval == ZERO_DELTA
        ):
            msg = (
                "`interval` should be a non-zero integer number of days. "
                f"Instead got a '{interval}'"
            )
            logger.error(msg)
            raise ValueError(msg)

        if isinstance(stop_at, str):
            stop_at = datetime.strptime(stop_at, "%Y-%m-%d").date()
        elif isinstance(stop_at, int):
            stop_at = start_day + interval * stop_at
    except Exception as e:
        logger.error(e.args[0], exc_info=True)
        raise e

    logger.info(
        f"Running with start_day = '{start_day}', interval = '{interval}', stop_at = '{stop_at}'"
    )

    # If a stop day is provided,
    #  the interval should have the same direction
    #  as the direction from start to stop
    #  or be a zero interval
    if stop_at and interval.days * (stop_at - start_day).days <= 0:
        logger.warning("No dates exist in the range. Exiting")
        return

    def _in_range(d: date) -> bool:
        if not stop_at or d == start_day:
            logger.debug(f"'{d}' is in the range")
            return True
        if (d - start_day).days * (stop_at - d).days > 0:
            logger.debug(f"'{d}' is in the range")
            return True
        else:
            logger.debug(f"'{d}' is not in the range")
            return False

    day = start_day
    while _in_range(day):
        logger.debug(f"day: {day}")
        logger.debug(f"stop_at: {stop_at}")
        new_stop_at = yield day
        logger.debug(f"Sent {new_stop_at!r} to the generator")
        if not isinstance(new_stop_at, (date, str, int, NoneType)):
            msg = (
                "Value sent to the generator should be either "
                "a datetime.date, a str, an int or None. "
                f"Instead got a {type(new_stop_at).__name__}"
            )
            logger.error(msg)
            raise TypeError(msg)
        if isinstance(new_stop_at, str):
            stop_at = datetime.strptime(new_stop_at, "%Y-%m-%d").date()
        elif isinstance(new_stop_at, date):
            stop_at = new_stop_at
        elif isinstance(new_stop_at, int):
            stop_at = day + interval * (new_stop_at + 1) if new_stop_at >= 0 else None
        day += interval


#%%
def main():
    g = dates_range("2021-01-01", stop_at=1, interval=timedelta(days=30))
    print(next(g))
    print(g.send(5))
    for d in g:
        print(d)


#%%
if __name__ == "__main__":
    main()
