#!/usr/bin/python
# -*- coding: utf-8 -*-
'''


@author: kazimir
'''
from TagCrawler import * 
from  CategoryCrawler import *
import time

if __name__ == '__main__':
    tc = TagCrawler('https://tw.bid.yahoo.com/tw/0-all.html?.r=1465414707')
    rootDir = tc.allsubCraw()
    leafUrl=[]    
    for url in rootDir:
        leafUrl.extend(tc.leafCraw(rootDir[url]))
        print url ,'完成'
        time.sleep(1)
    print len(leafUrl)
    urlList = []
    
    for url in leafUrl[0:1]:
        index =1 
        cc = CategoryCrawler(url)
        actualPage = cc.firstCraw()        
        while cc.hasNext:
            actualPage=cc.getThisCate(actualPage,index)            
            page = cc.domainUrl+actualPage
            urlList.extend(cc.urlGather(page))
            print index
            time.sleep(1)
            if cc.hasNext ==False:                          
                print '沒有下一頁 {}完成'.format(cc.targetTag)
                print len(urlList)  
            else:
                index+=1
            