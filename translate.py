#coding:UTF-8

import httplib
import md5
import urllib
import random

class Youdao_translate:
    def __init__(self):
        self.appKey = '399a8a54201006a0'
        self.secretKey = '1eL9juzLQZecIGwEPsi4I9l6RA50U0pl'

    def get_translation(self,words):
        httpClient = None
        myurl = '/api'
        q = words
        fromLang = 'EN'
        toLang = 'zh-CHS'
        salt = random.randint(1, 65536)

        sign = self.appKey + q + str(salt) + self.secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl + '?appKey=' + self.appKey + '&q=' + urllib.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        try:
            httpClient = httplib.HTTPConnection('openapi.youdao.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            res_str = response.read()
            #print res_str
            l1 = []
            for i in range(len(res_str)):
                if res_str[i] == '"':
                    l1.append(i)
            res = res_str[l1[4]+1:l1[5]].decode('utf8')
            if res == 'translation':
                res = res_str[l1[6]+1:l1[7]].decode('utf8')
            return res
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()

#youdao = Youdao_translate()
#msg = 'good'
#print youdao.get_translation(msg)
