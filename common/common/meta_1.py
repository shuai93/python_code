from pyquery import PyQuery as pq

import requests

base_headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding':
    'gzip, deflate, sdch',
    'Accept-Language':
    'zh-CN,zh;q=0.8'
}


def get_page(url):
    headers = dict(base_headers)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers)
        # print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.content.decode('gb2312')
    except ConnectionError:
        print('Crawling Failed', url)
        return None


# 道生一：创建抽取代理的metaclass
class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        attrs['__CrawlName__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlName__'].append(k)
                attrs['__CrawlFunc__'].append(v)
                count += 1
        for k in attrs['__CrawlName__']:
            attrs.pop(k)
        attrs['__CrawlFuncCount__'] = count
        print("attrs['__CrawlFunc__'] ", attrs['__CrawlFunc__'])
        print("attrs['__CrawlName__'] ", attrs['__CrawlName__'])
        return type.__new__(cls, name, bases, attrs)


# 一生二：创建代理获取类


class ProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, site):
        proxies = []
        print('Site', site)
        for func in self.__CrawlFunc__:
            if func.__name__ == site:
                this_page_proxies = func(self)
                for proxy in this_page_proxies:
                    # print('Getting', proxy, 'from', site)
                    proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            # print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    site = tr.find('td:nth-child(3)').text()
                    
                    yield ':'.join([ip, port]), site

    # def crawl_proxy360(self):
    #     start_url = 'http://www.proxy360.cn/Region/China'
    #     print('Crawling', start_url)
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         lines = doc('div[name="list_proxy_ip"]').items()
    #         for line in lines:
    #             ip = line.find('.tbBottomLine:nth-child(1)').text()
    #             port = line.find('.tbBottomLine:nth-child(2)').text()
    #             yield ':'.join([ip, port])

    # def crawl_goubanjia(self):
    #     start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         tds = doc('td.ip').items()
    #         for td in tds:
    #             td.find('p').remove()
    #             yield td.text().replace(' ', '')


def verify_proxy(proxy: str) -> bool:
    url = "http://www.baidu.com"
    proxy = {"http": "http://" + proxy}
    try:
        res = requests.get(url, proxies=proxy)

        if res.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    # 二生三：实例化ProxyGetter
    crawler = ProxyGetter()
    print(crawler.__CrawlName__, crawler.__CrawlFuncCount__)
    # 三生万物
    for site_label in range(crawler.__CrawlFuncCount__):
        site = crawler.__CrawlName__[site_label]
        print("> sit ---",site)
        myProxies = crawler.get_raw_proxies(site)
    
    for proxy in myProxies:
        if verify_proxy(proxy[0]):
            print('Success ', proxy)
        else:
            print('Faild ', proxy)