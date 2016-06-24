#!/usr/bin/python
# -*- coding: utf-8 -*-
'''


@author: kazimir
'''
from TagCrawler import * 
from  CategoryCrawler import *
import time
import codecs

if __name__ == '__main__':
    tc = TagCrawler('https://tw.bid.yahoo.com/tw/0-all.html?.r=1465414707')
    rootDir = tc.allsubCraw()
    leafUrl=[]
    result=''
    resultCount = 0                         
    id = 2944                               #改變爬取品項的起點
    endId = -1                              #爬取品項停止點     
    for url in rootDir:
        leafUrl.extend(tc.leafCraw(rootDir[url]))
        print url ,'complete'
        time.sleep(1)
    print len(leafUrl)
    urlList = []
    
    for url in leafUrl[id:endId]:
        
        index =1
        urlList = [] 
        cc = CategoryCrawler(url)
        actualPage = cc.firstCraw()        
            
        while cc.hasNext:       
            # pg改成 .format形式在塞回成網址             
             actualPage=cc.getThisCate(actualPage,index)
             
             urlList.extend(cc.urlGather(actualPage))
             
             time.sleep(1)
             #如果沒有下一頁 停止程式 po 出搜集到的url個數
             if cc.hasNext ==False:
                index =1            
                print '沒有下一頁 {}完成'.format(cc.targetTag)
                print len(urlList)  
             else:
                    index+=1
                    
        addr = 'E:/result'+'/'+str(id)+'.txt'
        addr.encode('utf-8')
        f = open(addr ,'w')
        id += 1
                
        for i in urlList :            
            try:
                
                result += cc.contentCraw(i)
                resultCount += 1 
                if resultCount ==10:                    #改變 resultCount可以加快寫進速度，注意被ban
                    f.write(result+'\n')
                    resultCount =0
                    result = ''            
                
            except:
                print '發生錯誤'
                addre = 'E:/result/error.txt'
                error = open(addre ,'a')
                error.write(i+'\n')
                continue
        f.close()

        
            
