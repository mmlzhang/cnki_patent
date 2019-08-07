

import requests
from lxml import etree
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from urllib3 import Retry

from settings import DRIVER_PATH
from utils.dingtalk import Colors, send_dingding
from utils import get_bloom, save_bloom_to_file, request_url, DataException, ResponseException
from utils.log import generate_logger
from dao import save_data


domain = "http://www.soopat.com"

common_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'advu1=; advu2=; advu3=; advu4=; patentids=; Hm_lvt_2b103433893a8cf930605886844fd95b=1564714722; ASP.NET_SessionId=rh5egq3lk5pr44aomhsmf4a2; __utma=135424883.943237040.1564716078.1564716078.1564716078.1; __utmb=135424883; __utmc=135424883; __utmz=135424883.1564716078.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); Hm_lpvt_2b103433893a8cf930605886844fd95b=1564716452',
    'Host': "www.soopat.com",
    'Referer': 'http://www.soopat.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}


def get_request_session():
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


s = get_request_session()


def get_etree_html(url, headers=None):
    h = headers if headers else common_header
    resp = s.get(url, headers=h)
    return etree.HTML(resp.content)


def get_category():
    url = "http://www.soopat.com/IPC/Index"
    headers = common_header.update({"Referer": url})
    html = get_etree_html(url, headers=headers)
    categories = html.xpath('//li[@class="ll"]')
    for c in categories:
        tag_a = c.xpath("./a")
        for a in tag_a:
            href = a.xpath("./@href")
            if href:
                yield urljoin(domain, href[0]), url


def get_patent_url():

    for url, referer in get_category():
        headers = common_header.update({"Referer": referer})

        html = get_etree_html(url, headers=headers)
        hrefs = html.xpath("//td[@class='IPCControl']/a[1]/@href")  # a[2]为世界专利,直接是完整url，不需要家domain
        for href in hrefs:
            yield urljoin(domain, href), url


def get_patent():

    for url, referer in get_patent_url():
        headers = common_header.update({"Referer": referer})
        html = get_etree_html(url, headers=headers)

        patents = html.xpath('//*[@id="PageContent"]/div/div[2]')
        print("patents: ", len(patents))
        for patent in patents:
            href = patent.xpath('./h2/a/@href')[0]
            category = patent.xpath('./h2/font/text()')[-1]
            category = category[1:-1]
            print(href, category)
            headers = common_header.update({"Referer": url})
            detail_html = get_etree_html(urljoin(domain, href), headers=headers)

            title = detail_html.xpath("//span[class='detailtitle']/h1/text()")
            print(title)


def main():
    get_patent()


    # url = "http://www.soopat.com/Home/Result?SearchWord=%E5%8D%97%E5%B1%B1%E9%93%9D%E4%B8%9A&FMZL=Y&SYXX=Y&WGZL=Y&FMSQ=Y&PatentIndex=60"
    # response = requests.get(url)
    #
    # html = etree.HTML(response.content)
    # titles = html.xpath('//*[@id="PageContent"]/div/div[2]/h2/a/text()')
    # for t in titles:
    #     print(t)
    # pass


if __name__ == '__main__':
    main()
