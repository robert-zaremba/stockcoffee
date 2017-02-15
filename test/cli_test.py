"""Functional level tests for CLI"""

from datetime import datetime as dt
from datetime import timedelta, timezone

import arrow
import pytest

from stockjournal.cli import Prompt
from stockjournal.operator import Operator

from .db_test import mk_db

utc = timezone.utc


def mk_cli():
    return Prompt(Operator(mk_db()))


def test_run_dividend():
    cli = mk_cli()
    assert cli.run_dividend("tea 10") == 0
    assert cli.run_dividend("pop 10") == 0.8
    assert cli.run_dividend("pop 0") is None

    with pytest.raises(ValueError):
        cli.run_pe("pop xxx")

    with pytest.raises(KeyError):
        cli.run_pe("xxx 10")


def test_run_pe():
    cli = mk_cli()
    assert cli.run_pe("tea 10") is None
    assert cli.run_pe("pop 10") == 10. / 8
    assert cli.run_pe("pop 0") == 0


def test_run_record_trade():
    cli = mk_cli()
    cli.run_record_trade("pop 2017-02-16T01:10 10 Buy 20")
    cli.run_record_trade("pop 2017-02-10T15:00 1 s 2")
    cli.run_record_trade("xxx 2017-02-10 1 s 2")
    trades = cli.operator.db.trades["POP"]
    assert len(trades) == 2
    assert trades[0].timestamp == dt(2017, 2, 16, 1, 10, tzinfo=utc)
    assert trades[0].typ == 'b'
    assert trades[0].volume == 10
    assert trades[0].price == 20


def test_run_record_trade_and_ops():
    cli = mk_cli()
    step = timedelta(minutes=1)
    start = arrow.utcnow() - timedelta(minutes=20, seconds=1)
    for x in range(1, 26):
        vol = x * 10
        cli.run_record_trade("pop {} {} Buy {}".format(
            start.strftime("%Y-%m-%dT%H:%M"), vol, x))
        start += step

    trades = cli.operator.db.get_trades("pop")
    assert len(trades) == 25

    check_vwsp(cli)
    check_recent_gmean(cli)
    check_gmean(cli)


def check_vwsp(cli):
    expected = 0
    for x in range(7, 22):
        expected += x * x * 10
    vol = 21 * 20 / 2 * 10
    expected /= vol
    assert cli.run_vwsp("pop") == expected


def check_recent_gmean(cli):
    expected = 1
    for x in range(7, 22):
        expected *= x
    assert eq(cli.run_r_gmean(), expected ** (1/15.))


def check_gmean(cli):
    expected = 1
    for x in range(1, 26):
        expected *= x
    assert eq(cli.run_gmean(), expected ** (1/25.))


def eq(a, b):
    return abs(a - b) < 1e-6
