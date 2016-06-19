# -*- coding: utf-8 -*-
'''
Created on 2016�N6��10��

@author: kazimir
'''

import requests
from bs4 import BeautifulSoup
import time
class Requester(object):
    headers = {
        'Accept':'*/*' ,
        'Accept-Encoding':'gzip, deflate, sdch, br' ,
        'Accept-Language':'zh-TW,zh;q=0.8,ja;q=0.6,en-US;q=0.4,en;q=0.2,zh-CN;q=0.2' ,
        'Connection':'keep-alive',    
        'Host':'tw.bid.yahoo.com' ,     
        
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
        'X-PJAX':'true',
        'X-Requested-With':'XMLHttpRequest' 
    }
    global rs
    def req(self,url):
        connection = True
        soup=''
        rs = requests.session()
        while connection == True:           
            try:                
                res = rs.get(url,headers=self.headers)                
                soup = BeautifulSoup(res.text)                
                connection = False
                
                return soup
            except:
                print 'connection error , sleep 1 min'                          
                time.sleep(60)
                

    
                    