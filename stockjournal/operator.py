from datetime import timedelta
import numpy as np

import arrow


class Operator:
    def __init__(self, db):
        """the stockjournal operator.
        @db: should be the instance of db.DB interface"""
        self.db = db

    def dividend(self, stock, market_price):
        s = self.db.get_summary(stock)
        if market_price == 0:
            return None
        if s.is_common:
            return s.dividend / market_price
        return s.fixed_dividend * s.par_val / market_price

    def pe(self, stock, market_price):
        s = self.db.get_summary(stock)
        if s.dividend <= 0:
            return None
        return market_price / s.dividend

    def recent_vwsp(self, stock):
        now, treshold = self.recent_time()
        trades = self.db.get_trades(stock)
        volume, total_value = 0, 0
        i = 0
        for t in reversed(trades):
            if treshold <= t.timestamp <= now:
                total_value += t.price * t.volume
                volume += t.volume
                i += 1
        if volume == 0:
            return None
        return total_value / volume

    def all_gmean(self):
        all_lists = self.db.trades.values()
        vals = [t.price for ts in all_lists for t in ts]
        return gmean(vals)

    def recent_gmean(self):
        now, treshold = self.recent_time()
        all_lists = self.db.trades.values()
        vals = [t.price for ts in all_lists for t in ts
                if treshold <= t.timestamp <= now]
        return gmean(vals)

    def recent_time(self):
        now = arrow.now()
        return now, now - timedelta(minutes=15)


def gmean_naive(vals):
    '''Naive computation of geometric mean of the given iterable.
This computation will have numeric problems because we are multiplying
big numbers. Better option is to use scipy.stats.gmean'''
    n, product = 0, 1
    for v in vals:
        product *= v
        n += 1
    if n == 0:
        return 0
    return product ** (1./n)


def gmean(vals):
    '''Naive computation of geometric mean of the given iterable.
    We temporarly we take logarithm of values to do safe sumation
    instead of unstable product.'''
    a = np.array(vals)
    if len(a) == 0:
        return 0
    logs = np.log(a)
    return np.exp(logs.mean())
