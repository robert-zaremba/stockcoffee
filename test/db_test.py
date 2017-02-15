import os.path

from stockjournal.db import DB


def mk_db():
    p = os.path.dirname(os.path.dirname(__file__))
    return DB(os.path.join(p, "data", "stock-summary.csv"))


def test_db_symbol_summary():
    d = mk_db()
    s = d.get_summary("TEA")
    assert s.is_common is True
    assert s.dividend == 0

    s = d.get_summary("tea")
    assert s.is_common is True
    assert s.dividend == 0

    s = d.get_summary('gin')
    assert s.is_common is False
    assert s.dividend == 8
