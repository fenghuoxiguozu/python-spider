import requests
import re
from lxml import etree
from params.location import china
from svgFont import Font
from config import *

class DianPing(object):
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
        self.cn=china()
        self.fo=Font()

    def parse(self,location,params):
        URL = 'http://www.dianping.com/{}/ch10/{}'
        url=URL.format(location,params)
        response = requests.get(url=url, headers=self.headers)
        html = etree.HTML(response.text)
        contents = html.xpath('//div[@id="shop-all-list"]/ul/li')
        values=[]
        for content in contents:
            shopUrl=content.xpath('.//div[@class="txt"]/div[@class="tit"]/a/@href')[0]
            value=self.parse_shop(shopUrl)
            values.append(value)
        return values
            # break

        # next_url=html.xpath('//a[@class="next"]/@href')
        # if next_url:
        #     self.parse(location,params,next_url)


    def parse_shop(self,shopUrl):
        response = requests.get(url=shopUrl, headers=self.headers)

        shopUrl = shopUrl
        shopName = re.findall(r'<h1 class="shop-name">(.*?)<a', response.text, re.S)
        stars= re.findall(r'mid-rank-stars mid-str(\d+)"></span>',response.text,re.S)

        Telephone=re.findall(r'电话：(.*?)</p>',response.text,re.S)
        Telephone=re.findall(r'>(.*?)<',Telephone[0],re.S)

        Address =re.findall(r'地址：(.*?)class="addressIcon', response.text, re.S)
        Address = re.findall(r'>(.*?)<', Address[0], re.S)

        all=re.findall(r'span id="reviewCount"(.*?)地址',response.text,re.S)
        all = re.findall(r'>(.*?)<', all[0], re.S)

        shopTelephone=self.parse_num(Telephone,NUM_FONT)         #不写死 (Telephone,fontNUM)
        shopaddress=self.parse_address(Address,ADDRESS_FONT)     #不写死 (Address,fontADDRESS)
        all = self.parse_num(all, NUM_FONT)
        all_info=''.join(all)


        v={
            "shopName": shopName[0].strip(),
            "shopTelephone":''.join(shopTelephone).replace('&nbsp','').lstrip(),
            "shopComment": re.findall(r' (.*?) 条评论',all_info,re.S)[0],
            "shopUrl": shopUrl,
            "shopAvg": re.findall(r'人均:(.*?)  口味',all_info,re.S)[0].replace('元','').strip(),
            "shopAddress": ''.join(shopaddress).split()[0],
            "shopEnviro": re.findall(r'环境: (.*?)  服务',all_info,re.S)[0],
            "shopTasty": re.findall(r'口味: (.*?)  环境',all_info,re.S)[0],
            "shopService": re.findall(r'服务: (.*?)     ', all_info, re.S)[0],
            "stars": int(stars[0]) / 10
           }
        return v


    def parse_num(self,key,NUM_FONT):   #(self,key,fontType):
        # values = self.fo.parse_font(fontType)   #values = self.fo.parse_font(fontType)
        result = []
        for x in key:
            x = x.replace('&#x', '').replace(';', '')
            try:
                value = NUM_FONT[x]
                result.append(value)
            except:
                result.append(x)
        return result

    def parse_address(self,key,ADDRESS_FONT):       #(self,key,fontType):
        # values = self.fo.parse_font(fontType)   #values = self.fo.parse_font(fontType)   #
        result = []
        for x in key:
            if ';' in x:
                x = x.replace('&#x', '').replace(';', '')
                try:
                    value = ADDRESS_FONT[x]
                    result.append(value)
                except:
                    value=self.parse_num([x],NUM_FONT)
                    result.append(value[0])
            else:
                result.append(x)
        return result


if __name__ == '__main__':
    dp=DianPing()
    s=dp.parse('shanghai','r802')
    print(s)
