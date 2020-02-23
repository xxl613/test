import baostock as bs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import tushare as ts


def get_data(year, quarter):
    df = ts.get_report_data(year=year, quarter=quarter).set_index('code')
    con = sqlite3.connect("stock_data.db")
    df = pd.read_sql('SELECT * FROM finacial_report', con)
    con.close()
    print(df)



    exit(0)
    bs_rs = bs.query_all_stock('2020-01-02')
    df = bs_rs.get_data()
    df = df[df['code_name'].str.contains("指数") == False][200:210]
    for i in range(0, len(df)):
        print(bs.query_stock_industry(df.iloc[i]['code']).get_data())



get_data()