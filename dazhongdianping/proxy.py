import requests


class proxy(object):
    def update_proxy(self):
        proxy_url=''
        proxies = requests.get(url=proxy_url).text
        return proxies