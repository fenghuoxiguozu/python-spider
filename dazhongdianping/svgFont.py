url='http://www.dianping.com/shop/95352390'

import requests
import re
import os
from urllib.parse import urljoin
from fontTools.ttLib import TTFont
from font.fontWord import FONT_LIST


class Font(object):
    def __init__(self):
        self.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie':'showNav=#nav-tab|0|1; navCtgScroll=0; navCtgScroll=171; showNav=#nav-tab|0|1; __guid=169583271.1192118947553049600.1548259899249.8318; _lxsdk_cuid=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _lxsdk=1687b7b3906c8-0bbb4f91871844-454c092b-1fa400-1687b7b39069f; _hc.v=f881bf49-e5cb-7108-4360-018d19f00345.1548259900; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; aburl=1; cy=6; cye=suzhou; monitor_count=85; _lxsdk_s=16cc39aa26d-680-9e0-209%7C%7C943',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Host':'www.dianping.com',
        'Upgrade-Insecure-Requests':'1',
        }

    def get_font(self):
        response=requests.get(url,headers=self.headers)
        svg=re.findall(r'} </script> <link rel="stylesheet" type="text/css" href="(.*?)"> <link rel="stylesheet',response.text,re.S)
        svg_url=urljoin('http://',svg[0])
        css=requests.get(url=svg_url)
        fonts=re.findall(r'font-family: "(.*?)";src:url.*?format\("embedded-opentype"\),url\("(.*?)"\);} .',css.text,re.S)
        return fonts

    def parse_font(self,woff):
        fontUrl=os.path.join(os.getcwd(),'font',woff)
        # 解析字体库
        font = TTFont(fontUrl)
        # 读取字体的映射关系['GlyphOrder', 'head', 'hhea', 'maxp', 'OS/2', 'hmtx', 'cmap', 'loca', 'glyf', 'name', 'post', 'GSUB']
        GlyphID = font.getGlyphOrder()
        uniList={}
        for i in range(2,len(GlyphID)):
            key=GlyphID[i].replace('uni', '')
            uniList[key]=FONT_LIST[i]
        return uniList


