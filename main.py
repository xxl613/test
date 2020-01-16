# main.py
import requests
import re
from bs4 import BeautifulSoup


def get_one_page(page_no):
    url = "http://www.mafengwo.cn/sales/ajax_2017.php?act=GetContentList&s_dept_time%5B%5D=all&price%5B%5D=all" \
          "&tag_group%5B9779%5D%5B%5D=all&tag_group%5B9365%5D%5B%5D=all&from=10208&kw=&to=M16209&salesType=NaN&page=" \
          + str(page_no) + "&group=1&sort=smart&sort_type=desc&limit=100 "
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.117 Safari/537.36 "
    }
    response = requests.get(url, headers=headers)
    html = response.json()['html']
    soup = BeautifulSoup(html, 'lxml')
    return soup.find_all(name='a', class_='item clearfix')


def main():
    base_url = "www.mafengwo.cn"
    for i in range(1, 100):  # 1到100页内获取页面,直到没有了为止
        product_list = get_one_page(i)

        if len(product_list) != 0:
            for product in product_list:
                href = base_url + product['href']
                title = product.find("h3").string.strip(" \n")
                store = re.findall("店铺:(.*)", product.find(class_='t').string)[0]
                try:
                    sold = re.findall("已售(\d*)", product.find(name='div', class_='detail').p.string)[0]
                except:
                    sold = 0
                print(href, title, store, sold)
        else:
            break


main()
