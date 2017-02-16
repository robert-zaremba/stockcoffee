import cmd
import arrow

from .db import DB
from .operator import Operator


class Prompt(cmd.Cmd):
    intro = 'Welcome to the Stock Calculator shell.  \
Type help or ? to list commands.\n'
    prompt = '> '

    def __init__(self, operator):
        super().__init__()
        self.operator = operator

    def run_dividend(self, line):
        args = line.split()
        price = float(args[1])
        return self.operator.dividend(args[0], price)

    def do_dividend(self, line):
        '''dividend stock_symbol market_price
        Calculates the dividend yield'''
        try:
            print(self.run_dividend(line))
        except Exception as e:
            print("""Wrong request. Expected arguments:
 stock_symbol: string,  market_price: decimal.\n""", e)

    def run_pe(self, line):
        args = line.split()
        price = float(args[1])
        return self.operator.pe(args[0], price)

    def do_pe(self, line):
        '''pe stock_name
calculates P/E ratio.'''
        try:
            print(self.run_pe(line))
        except Exception as e:
            print("""Wrong request. Expected arguments:
 stock_symbol: string,  market_price: decimal.\n""", e)

    def run_record_trade(self, line):
        args = line.split()
        timestamp = arrow.get(args[1]).datetime
        volume = float(args[2])
        price = float(args[4])
        return self.operator.db.add_trade(
            args[0], timestamp, volume, args[3], price)

    def do_record_trade(self, line):
        '''record_trade stock_symbol timestamp volume type price
Adds trade to the database. Timestamp can't contain space, though most\
widely formats are supported (eg yyyy-mm-ddThh:mm). \
Type is one of 'b' or 's'.'''
        try:
            t = self.run_record_trade(line)
            print("trade added", t)
        except Exception as e:
            print("""Wrong request. Expected arguments:
  stock_symbol: string,
  timestamp: datetime without spaces (eg 2016-01-22T15:01),
  volume: decimal number
  price: traded price value.\n""", e)

    def run_vwsp(self, line):
        args = line.split()
        return self.operator.recent_vwsp(*args)

    def do_vwsp(self, line):
        '''vwsp stock_symbol
calculates Volume Weighted Stock Price of given stock from last 15 minutes'''
        try:
            print(self.run_vwsp(line))
        except Exception as e:
            print("""Wrong request. Expected arguments:
 stock_symbol: string\n""", e)

    def run_r_gmean(self):
        return self.operator.recent_gmean()

    def do_r_gmean(self, line):
        '''r_gmean
calculates geometric mean of all recent (from last 15 min) stock prices\
stored in the program'''
        try:
            print(self.run_r_gmean())
        except Exception as e:
            print("Wrong request.\n", e)

    def run_gmean(self):
        return self.operator.all_gmean()

    def do_gmean(self, line):
        '''gmean
calculates geometric mean of all stock prices\
stored in the program'''
        try:
            print(self.run_gmean())
        except Exception as e:
            print("Wrong request.\n", e)

    def do_quit(self, line):
        '''quit the program'''
        print("Good bye")
        return True

    def do_EOF(self, line):
        return self.do_quit(line)


def main(db_filename):
    db = DB(db_filename)
    Prompt(Operator(db)).cmdloop()
