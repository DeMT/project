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
    for url in rootDir:
        leafUrl.extend(tc.leafCraw(rootDir[url]))
        print url ,'完成'
        time.sleep(1)
    print len(leafUrl)
    urlList = []
    
    for url in leafUrl[25:26]:
        index =1
        urlList = [] 
        cc = CategoryCrawler(url)
        actualPage = cc.firstCraw()        
            
        while cc.hasNext:       
            # pg改成 .format形式在塞回成網址             
             actualPage=cc.getThisCate(actualPage,index)
             page = cc.domainUrl+actualPage
             urlList.extend(cc.urlGather(page))
             print page
             time.sleep(1)
             #如果沒有下一頁 停止程式 po 出搜集到的url個數
             if cc.hasNext ==False:
                index =1            
                print '沒有下一頁 {}完成'.format(cc.targetTag)
                print len(urlList)  
             else:
                    index+=1
        f = codecs.open('e:\result\{}.txt'.format(cc.targetTag),'w')        
        for i in urlList :
            result=cc.contentCraw(i)
            f.write(result+'\n')        
            