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
    leafUrl=[]
    result=''
    resultCount = 0                         
   
    def __init__(self , url) :          #設定CategoryCrawler建構子
        self.url = url
        self.hasNext = True                      
    def firstCraw(self):                #爬第一次，目的是取回下一頁連結
        soup = super(CategoryCrawler,self).req(self.url)
        nextpage = soup.select('.next-page a')[0]['href']
        self.targetTag=(soup.select('#srp_bc span')[-1].text).encode('utf-8')   #這裡python內(unicode環境)->編碼為utf-8(str)
        self.categoryTag=(soup.select('#srp_bc span')[-2].text).encode('utf-8')    
        print self.targetTag,self.categoryTag                   #抓一下這個最小類別的名稱作檔案名，類別名稱作為資料夾
        instantBuy=soup.select('.yui3-u.hasbuyp a')[0]['href']                              
        return instantBuy
        
    def urlGather(self,url):                                #把一頁的網址收集起來 回傳一個List
        soup = super(CategoryCrawler,self).req(url)
        urlList =list()
        for title in soup.select('.srp-pdtitle'):
           
            #print title.text
            urlList.append(title.select('a')[0]['href'])
            
            
        try:   
            self.next =soup.select('.next-page.yui3-u a')[0]['href']               #如果現在爬取的這頁是最後一頁
        except:
            self.hasNext = False             
        return urlList     
    def contentCraw(self,url):
        soup = super(CategoryCrawler,self).req(url)
        content =''
        title = soup.select('.title')[0].text
        price = soup.select('.number')[0].text
        salCount = self.numberCleaner(soup.select('.has-sold')[0].text)
        remark = self.numberCleaner(soup.select('.remark')[0].text)                
        sallerName = soup.select('.seller-name a')[0].text   
        question = self.numberCleaner(soup.select('.total-item-count ')[0].text)         
        qicUrl = soup.select('.main-image')[0]['src']
        for font in soup.select('font'):         
            if font.text !='':
                tempC=re.sub('[\s+]', '', font.text)
                tempC = tempC.strip(' \t\n\r')             
                content += tempC
        result =title+'_|'+url+'_|'+salCount+'_|'+price+'_|'+sallerName+'_|'+remark+'_|'+question+'_|'+qicUrl+'_|'+content+'$& \n'
                #標題, 商品網址, 已賣數量, 價格, 賣家名稱 , 賣家評價 , 問與答數量 , 圖片網址 , 內文
        return result.encode('utf-8')
             
    def getThisCate(self,actualPage,index):
        #組合網址，先拆出pg 
        address=actualPage.split('&')
        #塞入第n頁
        pg = re.sub(r'pg=[\d]+', 'pg={}'.format(index),actualPage)
        aoffest = re.sub(r'aoffset=[\d]+', 'aoffset={}'.format((index-1)*60),pg)       
        #address[-6]= 'pg={}'.format(index)
        #address[-8]= 'aoffset={}'.format((index-1)*60)
        #放回actualPage
        actualPage = '&'.join(address)
        if index==1 :
            aoffest = self.domainUrl+aoffest+'&pjax=1' 
        
        return aoffest 
    def numberCleaner(self,st):
        match = re.search(r'[\d,]+',st)
        num = match.group().encode('utf-8')
        return  num            
    # if main 裡面是單獨測試碼，直接執行可以得到測試結果         
if __name__ == '__main__':
    addr = 'https://tw.bid.yahoo.com/tw/2092109949-category-leaf.html?.r=1465376779?hpp=23336_cat_category'  
    #^^^^^^^^在這裡需要輸入從標籤進來以後的第一個頁面 ^^^^^^  
    cc = CategoryCrawler(addr)
    fileName = '在這裡輸入檔名'  #^^^輸入儲存檔名^^^               
    actualPage = cc.firstCraw()     
    urlList = []
    index =1
    #如果物件的hasNext=True 則執行迴圈
     
    while cc.hasNext:       
    # pg改成 .format形式在塞回成網址
             
        actualPage=cc.getThisCate(actualPage,index)
                
        urlList.extend(cc.urlGather(actualPage))
        cc.headers['Referer']=actualPage
        
        print  
        
        
     
          
        time.sleep(3)
     #如果沒有下一頁 停止程式 po 出搜集到的url個數
        if cc.hasNext ==False:
            index =1            
            print '沒有下一頁 {}完成'.format(cc.targetTag)
            print len(urlList)  
        else:
                index+=1
        f = open( addr,'w')        
        for i in urlList :            
            try:
                
                cc.result += cc.contentCraw(i)
                cc.resultCount += 1 
                if cc.resultCount ==10:                    #改變 resultCount可以加快寫進速度，注意被ban
                    f.write(cc.result+'\n')
                    resultCount =0
                    result = ''            
                
            except:
                print '發生錯誤'
                addre = 'E:/result/error.txt'
                error = open(addre ,'a')
                error.write(i+'\n')
                continue
        f.close()        