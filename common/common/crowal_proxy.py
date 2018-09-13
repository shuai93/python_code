import requests
from lxml import etree

"""
爬取 cn-proxy 的代理，并测试代理是否可用
代码用到shadowsocks 的scoket 代理 需要 requests 支持 socket
sudo pip install -U requests[socks]
"""

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
 
def get_page(url: str) -> str:
    headers = dict(base_headers)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers, proxies=proxies)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


def parser_html(html: str) -> dict:
    tree = etree.HTML(html)
    # print(html)
    ips = tree.xpath('//tbody/tr/td[1]/text()')
    ports = tree.xpath('//tbody/tr/td[2]/text()')
    ip_port = dict(zip(ips,ports))
    return ip_port


def verify_proxy(proxy: str) -> bool:
    url = "http://www.baidu.com"
    res = requests.get(url)
    if res.status_code == 200:
        return True
    else:
        return False

def main():
    start_url = 'http://cn-proxy.com/'
    print('Crawling', start_url)
    html = get_page(start_url)
    if html:
        ip_ports = parser_html(html)
    else:
        return 0

    for k,v in ip_ports.items():
        proxy = {"http": "http://" + k + ":" + v}
        success = verify_proxy(proxy)
        if success:
            print(proxy)
if(__name__ == '__main__'):
    main()