'''This module computes '''

import argparse
import csv
import io
import os.path
from datetime import datetime
from urllib.request import urlopen

from stockjournal.operator import gmean

csv_header = "Date,Open,High,Low,Close,Volume,Adj Close"
parser = argparse.ArgumentParser(description='Stock stats tool using data \
from Yahoo Finance service or local file.')
parser.add_argument('src',
                    help="csv file with Yahoo Finance format (%s) or \
a valid stock symbol name to fetch from Yahoo Finance" % csv_header)


# months in yahoo finance starts from 0
# http://chart.finance.yahoo.com/table.csv?s=JPM&a=11&b=30&c=1983&d=1&e=16&f=2017&g=d&ignore=.csv
# all:
## "http://chart.finance.yahoo.com/table.csv?s=JPM&d=1&e=16&f=2017&g=d&ignore=.csv"
def read_from_yahoo(name):
    now = datetime.now()
    params = "s={}&d={}&e={}&f={}&g=d&ignore=.csv".format(
        name.upper(), now.month - 1, now.day, now.year)
    url = 'http://chart.finance.yahoo.com/table.csv?' + params
    with urlopen(url) as f:
        return get_values(io.TextIOWrapper(f, encoding='ascii'))


def read_from_file(filename):
    with open(filename) as f:
        return get_values(f)


def get_values(resource):
    h = resource.readline()[:-1]
    assert h == csv_header,\
        'csv header must be:\n%s got:\n%s' % (csv_header, h)
    reader = csv.reader(resource)
    vals = [float(r[4]) for r in reader]
    return vals


def main():
    args = parser.parse_args()

    if os.path.exists(args.src):
        vals = read_from_file(args.src)
    else:
        try:
            vals = read_from_yahoo(args.src)
        except Exception as e:
            print("Can't get the stock data from Yahoo Finance service.\
Probably the stock code is wrong: %s\n" % args.src, e)
            return
    print(gmean(vals))


main()
