import os.path

from stockjournal.cli import main


if __name__ == '__main__':
    d = os.path.dirname(os.path.abspath(__file__))
    main(os.path.join(d, "data", "stock-summary.csv"))
