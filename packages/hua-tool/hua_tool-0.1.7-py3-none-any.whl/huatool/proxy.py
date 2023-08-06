import huatool as HT

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

class Proxy(object):
    def __init__(self, **kwargs):
        self.country = kwargs['country'] if 'country' in kwargs else None
        self.ip = kwargs['ip'] if 'ip' in kwargs else None
        self.host = kwargs['host'] if 'host' in kwargs else None
        self.area = kwargs['area'] if 'area' in kwargs else None
        self.anony = kwargs['anony'] if 'anony' in kwargs else None
        self.httptype = kwargs['httptype'] if 'httptype' in kwargs else None
        self.speed = kwargs['speed'] if 'speed' in kwargs else None
        self.connecttime = kwargs['connecttime'] if 'connecttime' in kwargs else None
        self.lifetime = kwargs['lifetime'] if 'lifetime' in kwargs else None
        self.checktime = kwargs['checktime'] if 'checktime' in kwargs else None

    def __str__(self):
        return '%s:%s' % (self.ip, self.host)

    def toDict(self):
        return {
            'http': 'http://%s' % self.__str__(),
            'https': 'https://%s' % self.__str__()
        }

class XiCi(object):
    def __init__(self, timeout=3):
        self.nnPool = []
        self.ntPool = []
        self.timeout = timeout

        self._crawl(1)
        self._crawl(2)

    def _crawl(self, page=1):

        req = HT.Request.get('https://www.xicidaili.com/nn/%s' % (page), headers=HEADERS)
        bs = HT.BeautifulSoup(req.text, 'html.parser')

        ip_list_table = bs.find('table', attrs={
            'id': 'ip_list'
        })

        trs = ip_list_table.find_all('tr')[1:]

        for tr in trs:
            tds = tr.find_all('td')
            dicts = {
                'country': tds[0].find('img').attrs['alt'] if tds[0].find('img') is not None else None,
                'ip': tds[1].text.strip(),
                'host': tds[2].text.strip(),
                'area': tds[3].text.strip(),
                'anony': tds[4].text.strip(),
                'httptype': tds[5].text.strip(),
                'speed': float(tds[6].find('div', attrs={'class': 'bar'}).attrs['title'][:-1]) if tds[6].find('div') is not None else None,
                'connecttime': float(tds[7].find('div', attrs={'class': 'bar'}).attrs['title'][:-1]) if tds[7].find('div') is not None else None,
                'lifetime': tds[8].text.strip(),
                'checktime': tds[9].text.strip()
            }
            if dicts['speed'] <= self.timeout:
                self.nnPool.append(Proxy(**dicts))

    def get(self):
        rd_proxy = HT.Random.choice(self.nnPool)
        return rd_proxy