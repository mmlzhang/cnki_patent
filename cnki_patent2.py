# coding=utf-8

# 知网专利爬虫
import datetime
import re
import time
# from lxml import etree
import traceback

import requests
from dateutil.rrule import rrule, DAILY

from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib.parse import urlencode

# from settings import DRIVER_PATH
# from utils.dingtalk import Colors, send_dingding
# from utils import get_bloom, save_bloom_to_file, request_url, DataException, ResponseException
from settings import DRIVER_PATH
from utils.log import logger
# from dao import save_data
from utils.driver import Chrome

from bs4 import BeautifulSoup

DAY_FORMAT = "%Y-%m-%d"


def get_request_session():
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


s = get_request_session()

cookie = {
    'Ecp_ClientId': '8190803112400683814',
    'Ecp_IpLoginFail': '190803222.212.80.192',
    'cnkiUserKey': '78a8a93b-d8ab-93a1-e250-d6fac7afa41f',
    'ASP.NET_SessionId': 'sxsg52rdbs5jhw32js4iqbuh',
    'SID_epub': '1201055',
    'RsPerPage': '50',
    'AutoIpLogin': '',
    'LID': '',
    'SID_grid': '120101',
    '_pk_ref': '%5B%22%22%2C%22%22%2C1564818330%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DdD8UXlU2K2s4YP8r29xtSpB4PqjD-C9r2dopwcnPXPxuLSQ9_LzDhAcuTN8ZOFArtEF3YiBOVzBzD_59I5bl9K%26wd%3D%26eqid%3Da282e0b60003af1a000000045d4501db%22%5D',
    '_pk_ses': '*'}

s.cookies.update(cookie)


def get_patent_info(url):
    resp = s.get(url)

    soup = BeautifulSoup(resp.text)

    title = soup.title.text.split("--")[0]
    if title == "信息提示":
        print("没有此项!")
        return None
    # print(title)

    tds = soup.find_all(name='td',attrs={"class": "checkItem"})
    result = {"标题": title}
    for td in tds:
        name = td.find_previous_sibling("td").text
        name = re.findall("【(.*?)】", name)[0]
        value = td.text.replace("\xa0", "")
        result[name] = value
    logger.info("data: {}".format(str(result)))
    with open("cnki_data.txt", "a", encoding='utf-8') as f:
        f.write(str(result) + "\n")


def handler_page(page_source):
    soup = BeautifulSoup(page_source, "lxml")
    table = soup.find(name='table', attrs={"class": "s_table"})
    if not table:
        print("没有专利展示!")
        return
    patents = table.find_all("td")
    titles = []
    href_set = set()
    for p in patents:
        a = p.find("a")
        if a:
            href = a.attrs.get("href")
            href_set.add(href)
            # test
            title = a.text
            if not title.isdigit():
                titles.append(title)
                # print(href, title)
    print("perpage: {}, titels: {}".format(len(titles), titles))

    with open("href_set.txt", "a", encoding="utf-8") as f:
        f.write(", ".join(href_set))
    for h in list(href_set):
        url = "http://dbpub.cnki.net/Grid2008/Dbpub/{}".format(h)
        get_patent_info(url)


def get_pages(driver, category, start_date, end_date, start_page=0):
    if not start_page:
        begin_page = 2
        end_page = 8
    else:
        begin_page = start_page
        end_page = begin_page + 7
    # 第一页
    url = "http://dbpub.cnki.net/Grid2008/Dbpub/Brief.aspx?ID=SCPD&subBase=all"

    driver.get(url)
    # 取消选择全部分类
    driver.find_element_by_xpath(
        '//*[@id="navitree"]/tbody/tr[5]/td/table[2]/tbody/tr[3]/td/table/tbody/tr/td/a[2]').click()
    # 选择单一分类
    driver.find_element_by_xpath(
        '//*[@id="navitree"]/tbody/tr[5]/td/table[2]/tbody/tr[{}]/td/input'.format(category)).click()
    # 每页50条
    driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr/td/select[3]/option[5]').click()

    # 开始日期
    driver.execute_script('document.querySelector("#MM_fieldValue_1_1").value=""')
    driver.find_element_by_xpath('//*[@id="MM_fieldValue_1_1"]').send_keys(start_date.strftime(DAY_FORMAT))
    # 结束日期
    driver.execute_script('document.querySelector("#MM_fieldValue_1_2").value=""')
    driver.find_element_by_xpath('//*[@id="MM_fieldValue_1_2"]').send_keys(end_date.strftime(DAY_FORMAT))

    # 检索信息
    driver.find_element_by_xpath('//*[@id="Table6"]/tbody/tr[1]/td[3]/table/tbody/tr/td/input').click()

    # 跳转到对应的页码
    if start_page:
        driver.execute_script(
            'document.querySelector("#id_grid_turnpage > input[type=text]").value={}'.format(start_page))
        driver.execute_script("check1('ttt')")

    patents = driver.find_elements_by_xpath('//*[@id="contentBox"]/table/tbody/tr/td[1]')
    if patents:
        handler_page(driver.page_source)

    # 获取页码
    turnpage = driver.find_element_by_xpath('//*[@id="id_grid_turnpage"]').text
    pages_num = turnpage.strip().split()[-2]
    pages_num = int(pages_num.replace("/", "")) if "/" in pages_num else 0
    if pages_num <= 1:
        return None
    else:
        for page in range(begin_page, min(pages_num, end_page)):
            # 下一页
            next_page = driver.find_elements_by_xpath('//div[@id="id_grid_turnpage"]/a')
            next_page = next_page[-2]
            next_page.click()
            handler_page(driver.page_source)
# print("end page: ", end_page)
# end_date = end_date + datetime.timedelta(days=1)
# return get_7_pages(driver, category_map, start_date, end_date, start_page=end_page)


def driver_get_patent(start_page=2):
    chrome = Chrome(DRIVER_PATH)
    driver = chrome.driver
    category_map = {
        "4": "基础科学",
        "5": "工程科技1辑",
        "6": "工程科技2辑",
        "7": "农业科技",
        "8": "医药卫生科技",
        "9": "哲学与人文科学",
        "10": "社会科学2辑",
        "11": "信息科技",
    }
    start_date = "1988-02-27"
    end_date = "2019-08-06"
    date_list = [dt for dt in rrule(
        DAILY, dtstart=datetime.datetime.strptime(start_date, DAY_FORMAT).date(),
        until=datetime.datetime.strptime(end_date, DAY_FORMAT).date())]

    for date in date_list[::100]:
        start_date = date + datetime.timedelta(days=-100)
        # end_date = datetime.datetime(year=2000, month=11, day=11)
        end_date = date + datetime.timedelta(days=2)
        try:
            for category, category_name in category_map.items():
                get_pages(driver, category, start_date, end_date)
        except Exception as e:
            err = traceback.format_exc()
            print(err)
            logger.error(str(err))


if __name__ == '__main__':
    driver_get_patent()
