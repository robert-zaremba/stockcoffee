from stockjournal.operator import Operator

from .db_test import mk_db

sample_db = mk_db()


def mk_operator():
    return Operator(sample_db)


def test_dividend():
    o = mk_operator()
    assert o.dividend("TEA", 1000) == 0
    assert o.dividend("gin", 1000) == 100 * 0.02 / 1000


def test_pe():
    o = mk_operator()
    assert o.pe("TEA", 1000) is None
    assert o.pe("gin", 1000) == 1000 / 8.
