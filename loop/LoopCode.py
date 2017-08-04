import requests
import json
trending_api = 'https://python.0x2048.com/v1/trending?since=daily'
detail_api = 'https://python.0x2048.com/v1/repos?github=%s'
import SendSMS


class Loop(object):
    def __init__(self):
        self.s = requests.Session()

    def trending(self):
        tr = self.s.get(trending_api)
        if tr.status_code is not 200:
            SendSMS.send_sms()
        else:
            trending_result = tr.json()
            for item in trending_result:
                url = item['url']
                yield url

    def detail(self, url):
        de = self.s.get(detail_api % url)
        print de.text


if __name__ == '__main__':
    
    loop = Loop()
    urls = loop.trending()
    for url in urls:
        loop.detail(url)