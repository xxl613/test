# FLP_homework.py
# 获取SP500公司信息后，根据company_name获取2008年的财报信息
import yahoofinance
import pandas as pd
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import sqlite3


# get balance sheet data
def get_BalanceSheet_data(code):
    try:
        BS_list = yahoofinance.BalanceSheet(code).BalanceSheet
    except:
        return -1
    print('Received BalanceSheet')

    totalAssets = BS_list[1]['totalAssets']['raw']  # totalAssets
    PPE = BS_list[1]['propertyPlantEquipment']['raw']  # PPEnt???
    totalLiabilities = BS_list[1]['totalLiab']['raw']

    return list(map(float, [totalAssets, PPE, totalLiabilities]))


# get income statement data
def get_IncomeStatement_data(code):
    IS_list = yahoofinance.IncomeStatement(code).IncomeStatement
    print("Received IncomeStatement")

    incomeBeforeTax = IS_list[1]['incomeBeforeTax']['raw']
    grossProfit = IS_list[1]['grossProfit']['raw']
    totalRevenue = IS_list[1]['totalRevenue']['raw']
    ib = IS_list[1].get('netIncome', 0)['raw']  # ib

    return list(map(float, [incomeBeforeTax, grossProfit, totalRevenue]))


# get company info, especially company symbol
def get_company_info():
    # get company_info from website
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.106 Safari/537.36 '
    }
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url, headers=headers)
    html = response.text
    print('Received Company info')

    # get data we need from all company_info
    soup = BeautifulSoup(html, 'lxml')
    company_ls = soup.find_all(name='tr')
    company_info = []  # save data
    try:
        for company_detail in company_ls[1:]:
            data_ls = company_detail.find_all(name='td')
            industry = data_ls[3].string.strip()
            # filter information technology and consumer staples
            if industry in ['Information Technology', 'Consumer Staples']:
                symbol = data_ls[0].a.string.strip()  # symbol
                company_name = data_ls[1].a.string.strip()  # company_name
                CIK = data_ls[7].string.strip()  # cik
                company_info.append([CIK, symbol, company_name, industry])
    except:
        return company_info


# write all data into dabatase
def generate_data():
    # get all cik and company_name
    company_list = get_company_info()
    cnt = len(company_list)  # the length of data
    con = sqlite3.connect('sp500_mafa2020.db')

    # get finacial data from balancesheet and incomestatement, then save data in df
    for i, info in enumerate(company_list):
        bs_data = get_BalanceSheet_data(info[1])
        if bs_data != -1: # 如果获取失败就将数据写1
            is_data = get_IncomeStatement_data(info[1])
            # get data[totalAssets,PPE,totalLiabilities, incomeBeforeTax, grossProfit, totalRevenue, cik, symbol,
            # company_name]
            data = bs_data + is_data + info
        else:
            data = [-1, -1, -1, -1, -1, -1] + info

        # calculate
        roa = data[3] / data[0]  # income before tax / total assets
        profit_margin = data[4] / data[5]  # gross profit / total revenue
        ppe_to_at = data[1] / data[0]  # ppe / total assets
        debt_to_at = data[2] / data[0]  # total liabilities / total assets

        # create a DataFrame to save data
        df = pd.DataFrame(columns=['cik', 'conm', 'industry', 'roa', 'profit_margin', 'ppe_to_at', 'debt_to_at'])

        df.loc[0] = [info[0], info[2], info[3], roa, profit_margin, ppe_to_at, debt_to_at]
        df.set_index('cik').to_sql('sp_finacial', con, if_exists='append')
        print(i + 1, "/", cnt)  # show how much left
    con.close()


def picture():
    con = sqlite3.connect('sp500_mafa2020.db')
    df = pd.read_sql('SELECT * FROM sp_finacial', con, index_col='cik')
    con.close()

    tech_data = df[df['industry'] == 'Information Technology']
    consumer_data = df[df['industry'] == 'Consumer Staples']
    tech_data.hist(bins=30)
    plt.savefig('tech_ind.png')

    consumer_data.hist(bins=30)
    plt.savefig('con_ind.png')


generate_data()
picture()
