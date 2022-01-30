from datetime import date
import logging
from generators.dates import dates_range


def test_dates_range(caplog):
    caplog.clear()
    g = dates_range("2021-01-01", 5)
    l = [d for d in g]
    assert len([r for r in caplog.record_tuples if r[1] == logging.INFO]) == 1
    assert len([r for r in caplog.record_tuples if r[1] == logging.DEBUG]) == 3 * 5 + 2
    assert l == [date(2021, 1, i) for i in range(1, 6)]
