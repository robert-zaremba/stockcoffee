import csv
from collections import defaultdict

from pycommon.clshelpers import lazy_init

csv_header = "Stock Symbol,Type,Last Dividend,Fixed Dividend,Par Value"\
             .split(',')


class StockSummary:
    def __init__(self, typ, dividend, fixed_dividend, par_val):
        '''StockSummary structure
        Args:
          typ (string): common or preferred
          dividend (float): real value of last dividend
          fixed_dividend (float)
          par_val (float)'''
        self.is_common = typ.lower() == 'common'
        self.dividend = dividend
        self.fixed_dividend = fixed_dividend
        self.par_val = par_val

    @staticmethod
    def read(record):
        try:
            fixed_dividend = record[3].strip()
            if fixed_dividend == "":
                fd = None
            elif fixed_dividend.endswith("%"):
                fd = float(fixed_dividend[:-1]) / 100.
            else:
                fd = float(fixed_dividend[:-1])
            return StockSummary(
                record[1],
                float(record[2]),
                fd,
                float(record[4]))
        except Exception as e:
            raise ValueError("expecting stock type followed by 3 numbers:\
 dividend, fixed dividend, par value. Got: %s" % record, e)


class Trade:
    mapper = {'buy': 'b', 'sell': 's', 'b': 'b', 's': 's'}

    @lazy_init
    def __init__(self, timestamp, volume, typ, price):
        self.typ = self.mapper[typ.lower()]


class DB:
    def __init__(self, filename):
        """A database interface for the calculator
        Args:
          filename: a csv file with stock symbols"""
        db = {}
        trades = defaultdict(list)
        with open(filename) as f:
            reader = csv.reader(f)
            h = next(reader)
            assert h == csv_header, "expected %s, got %s" % (csv_header, h)
            for r in reader:
                stock = r[0].upper()
                db[stock] = StockSummary.read(r)
                trades[stock]
        self.db = db
        self.trades = trades

    def has_symbol(self, name):
        name = name.upper()
        return name in self.db

    def get_summary(self, name):
        name = name.upper()
        s = self.db.get(name)
        if s is None:
            raise KeyError("Unknown stock symbol %s" % name)
        return s

    def get_trades(self, name):
        name = name.upper()
        s = self.trades.get(name)
        if s is None:
            raise KeyError("Unknown stock symbol %s" % name)
        return s

    def add_trade(self, stock, timestamp, volume, typ, price):
        self.trades[stock.upper()].append(
            Trade(timestamp, volume, typ, price))
