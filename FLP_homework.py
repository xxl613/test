# main.py
# company_name,CIK,industry,TICKER
import requests
from bs4 import BeautifulSoup
import xlwt

# get website data
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.106 Safari/537.36 '
}
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url, headers=headers)
html = response.text

# create an excel
cnt = 1
wb = xlwt.Workbook(encoding='utf-8')
worksheet = wb.add_sheet('data')
worksheet.write(0, 0, 'company_name')
worksheet.write(0, 1, 'CIK')
worksheet.write(0, 2, 'industry')
worksheet.write(0, 3, 'TICKER')

# deal with website data and write data in excel
soup = BeautifulSoup(html, 'lxml')
ls_company = soup.find_all(name='tr')
try:
    for company_detail in ls_company[1:]:
        data_ls = company_detail.find_all(name='td')

        company_name = data_ls[0].a.string.strip()
        CIK = data_ls[7].string.strip()
        industry = data_ls[3].string.strip()
        TICKER = data_ls[0].a.string.strip()
        worksheet.write(cnt, 0, company_name)
        worksheet.write(cnt, 1, CIK)
        worksheet.write(cnt, 2, industry)
        worksheet.write(cnt, 3, TICKER)
        cnt += 1
except:
    wb.save("data.xls")
