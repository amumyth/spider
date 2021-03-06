# -*- coding:UTF-8 -*-
import requests, random, time, io, xlsxwriter
from lxml import etree
from retrying import retry
from PIL import Image



#生成随机头
def randHeader():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection': head_connection[0],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[1],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
        'cookie': 'session-id=144-0875527-0711417; session-id-time=2082787201l; ubid-main=132-3065853-5842354; x-wl-uid=1AhLMZEinBycdlI1tlb7FGdiZPIkCHGrEaQZ6yUeZA8OsAwsAvKPjk32vn6UoYk55VGVQbNAVOZw=; session-token=YBj6Fu7RdQPKDU/pbF+Rktxm4E3qjlj9oZOAKYJ+XySzr3b+akT8LsFD1engX+6JSZ54VvFbO/5IpbL0IdqaHUqe4KGEA8lhzQr4hPQjgvRfqKChynb4LCdQpIhmh6EF+DASRUzov7LPrrkOLdQRHxkgGkl0J+ZvmpOQC+uhaMXqSuNIre9sD4OL57ERbwNBiPNDONFw+pSUnCITMnKI2y7p8fNOSG5IYIN2G2r/r9JskIt9CQBnXYlqHj+mP3jD; lc-main=en_US; csm-hit=tb:s-29WDXRCAMXNRCPA3DNS7|1541419275777&adb:adblk_yes'
    }
    return header

class Amazon(object):
    def __init__(self, product, count):
        self.header = randHeader()
        self.product = product
        self.search_count = count

    def get_Product_URL_By_Page_Number(self, pageNumber):
        try:
            if pageNumber == 1:
                return 'https://www.amazon.com/s?k=' + self.product + '&i=electronics-intl-ship&ref=nb_sb_noss'
            else:
                return 'https://www.amazon.com/s?k='\
                       + self.product\
                       + '&i=electronics-intl-ship&page='\
                       + str(pageNumber)\
                       + '&qid='\
                       + str(int(time.time()))\
                       + '&ref=sr_pg_'\
                       + str(pageNumber)
        except Exception as e:
            print(str(e))
        return None

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        r = requests.get(url, headers=randHeader(),timeout=3)
        print(r.status_code)
        assert r.status_code == 200
        return r

    def parse_url(self, url):
        try:
            html = self._parse_url(url)
        except:
            html = None
        return html

    def find_product_node(self, html, number):
        root = etree.HTML(html.content)
        path = '//li[@data-result-rank="%s"]' % number
        print(path)
        result = root.xpath(path)
        print(result[0].xpath('.//@data-result-rank'))
        product_price = result[0].xpath('.//span[@class="a-offscreen"]/text()')
        print(product_price)
        product_title = result[0].xpath('.//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@title')
        print(product_title)
        product_reviews = result[0].xpath('.//div[@class="a-row a-spacing-none"]/a[@class="a-size-small a-link-normal a-text-normal"]/text()')
        print(product_reviews)
        product_img = result[0].xpath('.//div[@class="s-card s-card-group-rot-B01NAJGGA2 s-active"]/img/@src')
        print(product_img)
        return 'OK'

    def go(self):
        for i in range(self.search_count):
            url = self.get_Product_URL_By_Page_Number(i + 1)
            print('url: ' + url)
            html = self.parse_url(url)
            if html == None:
                print('parse url error')
                return
            txt = self.find_product_node(html , i)
            #f = open('G://amazon_items_%s.html' % i, 'w', encoding='utf-8')
            #f.write(txt)
            #f.close()
            #print(txt)
            time.sleep(2)

if __name__ == '__main__':
    count = 1 # how many pages you wanna to seach
    Amazon('headphone', count).go()