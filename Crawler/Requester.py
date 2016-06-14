# -*- coding: utf-8 -*-
'''
Created on 2016�N6��10��

@author: kazimir
'''

import requests
from bs4 import BeautifulSoup
class Requester(object):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.\
    94 Safari/537.36'
    }
    def req(self,url):
        rs = requests.session()
        res = rs.get(url,headers=self.headers)
        soup = BeautifulSoup(res.text)
        return soup
        



    

        