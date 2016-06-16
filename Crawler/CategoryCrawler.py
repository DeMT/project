#!/usr/bin/python
# -*- coding: utf-8 -*-
'''


@author: kazimir
'''
from Requester import Requester
import requests
from bs4 import BeautifulSoup
import time
import re

class CategoryCrawler(Requester):
    next =''
    domainUrl = 'https://tw.bid.yahoo.com/tw/'
    def __init__(self , url) :          #設定CategoryCrawler建構子
        self.url = url
        self.hasNext = True                      
    def firstCraw(self):                #爬第一次，目的是取回下一頁連結
        soup = super(CategoryCrawler,self).req(self.url)
        nextpage = soup.select('.next-page a')[0]['href']
        self.targetTag=(soup.select('#srp_bc span')[-1].text).encode('utf-8')    #這裡python內(unicode環境)->編碼為utf-8(str)
        print self.targetTag  
        instantBuy=soup.select('.yui3-u.hasbuyp a')[0]['href']                              #抓一下這個最小類別的名稱
        return instantBuy
        
    def urlGather(self,url):                                #把一頁的網址收集起來 回傳一個List
        soup = super(CategoryCrawler,self).req(self.url)
        urlList =list()
        for title in soup.select('.srp-pdtitle'):
            print title.text
            #print title.text
            urlList.append(title.select('a')[0]['href'])
            
        try:   
            self.next =soup.select('.next-page.yui3-u a')[0]['href']               #如果現在爬取的這頁是最後一頁
        except:
            self.hasNext = False             
        return urlList     
    def contentCraw(self,url):
        soup = super(CategoryCrawler,self).req(self.url)
        content =''
        title = soup.select('.title')[0].text
        price = soup.select('.number')[0].text
        salCount = self.numberCleaner(soup.select('.has-sold')[0].text)
        remark = self.numberCleaner(soup.select('.remark')[0].text)                
        sallerName = soup.select('.seller-name a')[0].text   
        question = self.numberCleaner(soup.select('.total-item-count ')[0].text)         
        qicUrl = soup.select('.main-image')[0]['src']
        result =title+'_|'+url+'_|'+salCount+'_|'+price+'_|'+sallerName+'_|'+remark+'_|'+question+'_|'+qicUrl+'_|'+content
                #標題, 商品網址, 已賣數量, 價格, 賣家名稱 , 賣家評價 , 問與答數量 , 圖片網址 , 內文
        return result
             
    def getThisCate(self,actualPage,index):
        #組合網址，先拆出pg 
        address=actualPage.split('&')
        #塞入第n頁        
        address[-5]= 'pg={}'.format(index)
        address[-7]= 'aoffset={}'.format((index-1)*60)
        #放回actualPage
        actualPage = '&'.join(address)
        
        return actualPage 
    def numberCleaner(self,st):
        match = re.search(r'[\d,]+',st)
        num = match.group().encode('utf-8')
        return  num            
    # if main 裡面是單獨測試碼，直接執行可以得到測試結果         
if __name__ == '__main__':
    #在這裡需要輸入從標籤進來以後的第一個頁面   
    cc = CategoryCrawler('https://tw.bid.yahoo.com/tw/2092109949-category-leaf.html?.r=1465376779?hpp=23336_cat_category')
    #爬第一次  
                                                                                  # ^^^^^^^^^^^^ 似乎只需要改這裡就能換標籤
    actualPage = cc.firstCraw()     
    urlList = []
    index =1
    #如果物件的hasNext=True 則執行迴圈
     
    while cc.hasNext:       
    # pg改成 .format形式在塞回成網址        
        #actualPage=cc.getThisCate(actualPage,index)
        
        
        print actualPage    
        urlList.extend(cc.urlGather(actualPage))
        actualPage = cc.domainUrl+cc.next
     
          
        time.sleep(3)
     #如果沒有下一頁 停止程式 po 出搜集到的url個數
        if cc.hasNext ==False:
            index =1            
            print '沒有下一頁 {}完成'.format(cc.targetTag)
            print len(urlList)  
        else:
                index+=1
        