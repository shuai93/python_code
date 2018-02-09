#!/usr/bin/env python3  
# @Time    : 18-1-31 下午2:56
# @Author  : ys
# @Email   : youngs@yeah.net

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web


def test():
    start = datetime.datetime(2016, 1, 1) # or start = '1/1/2016'
    end = datetime.date.today()
    prices = web.DataReader('AAPL', 'yahoo', start, end)


def main():
    test


if __name__ == "__main__":
    main()
