#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza (User:yamaha5) , 2011
#
# Distributed under the terms of MIT License (MIT)
# for more information see https://fa.wikipedia.org/wiki/کاربر:Fatranslator/ترجمه_همسنگ
#
from pywikibot.compat import query
import re
import pywikibot
import ref_link_correction_core
import codecs
from pywikibot import config
import time
import MySQLdb as mysqldb
ensite = pywikibot.Site('en', 'wikipedia')
fasite = pywikibot.Site('fa', 'wikipedia')

BotVersion=u'۱۰.۱ core'
_cache={}

def Check_Page_Exists(page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'Check_Page_Exists'])):
        return _cache[tuple([page_link, 'Check_Page_Exists'])]
    site = pywikibot.Site('fa')
    params = {
        'action': 'query',
        'prop':'info',
        'titles': page_link
    }

    query_page =pywikibot.data.api.Request(site=site, **params).submit()
    try:
        for i in query_page[u'query'][u'pages']:    
            redirect_link=query_page[u'query'][u'pages'][i]['pageid']  
            _cache[tuple([page_link, 'Check_Page_Exists'])]=True
            return True# page existed
    except:
        _cache[tuple([page_link, 'Check_Page_Exists'])]=False
        return False# page not existed

def namespacefinder( enlink ,firstsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'') 
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink,firstsite, 'namespacefinder'])):
        return _cache[tuple([enlink,firstsite, 'namespacefinder'])]
    site = pywikibot.Site(firstsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    a=1    
    if a:
        categoryname =pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname[u'query'][u'pages']:
            fanamespace=categoryname[u'query'][u'pages'][item]['ns']
        _cache[tuple([enlink,firstsite, 'namespacefinder'])]=fanamespace
        return fanamespace
    else: 
        _cache[tuple([enlink,firstsite, 'namespacefinder'])]=False
        return False

def clean_word (word):
  word=word.lower()
  word=word.replace(u"'",u"").replace(u'"',u"").replace(u'_',u" ")
  word=re.sub(ur'[\-\.\:,;@#\$\*\+\!\?%\^\/\\\<\>ʻ”“‘’‚’”\(\)\}\{–—−ـ_]',u'',word)
  word=re.sub(ur'\s{2,}',u'',word)
  return word

def Compairing(s1,s2):
    s1=s1.lower()
    s2=s2.lower()
    # Make sorted arrays of string chars
    s1c = [x for x in s1]
    s1c.sort()
    s2c = [x for x in s2]
    s2c.sort()
    i1 = 0
    i2 = 0
    same = 0
    # "merge" strings, counting matches
    while ( i1<len(s1c) and i2<len(s2c) ):
        if s1c[i1]==s2c[i2]:
            same += 2
            i1 += 1
            i2 += 1
        elif s1c[i1] < s2c[i2]:
            i1 += 1
        else:
            i2 += 1
    # Return ratio of # of matching chars to total chars
    return same/float(len(s1c)+len(s2c))

def is_equal (s1,s2):
    s1=s1.strip()
    s2=s2.strip()
    CleanComp=Compairing(clean_word(s1),clean_word(s2))
    Comp=Compairing(s1,s2)
    if s1.lower() in s2.lower() or s2.lower() in s1.lower():
      return True, 100
    elif CleanComp > 0.5:
      return True, CleanComp
    elif  Comp > 0.5:
      return True, Comp
    else:
      return False, CleanComp

def redirect_find( page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'redirect_find'])):
        return _cache[tuple([page_link, 'redirect_find'])], 0
    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link
    }
    query_page =pywikibot.data.api.Request(site=pywikibot.Site('en'), **params).submit()
    try:
        redirect_link=query_page[u'query'][u'redirects'][0]['to']
        is_equal_result,Comp=is_equal (page_link,redirect_link)
        if is_equal_result:
            #It is redirect but it seems ok to replace
            _cache[tuple([page_link, 'redirect_find'])]=True
            return True, Comp
        else:
            _cache[tuple([page_link, 'redirect_find'])]=False
            return False, Comp
    except:
        if 'missing=""' in str(query_page):
            _cache[tuple([page_link, 'redirect_find'])]=False
            return False, 0
        else:
            _cache[tuple([page_link, 'redirect_find'])]=True
            return True, 0


def englishdictionry(enlink, firstsite, secondsite):
    if _cache.get(tuple([enlink, firstsite, secondsite, 'en_dic'])):
        return _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])]
    try:
        enlink = unicode(str(enlink), 'UTF-8').replace(u'[[', u'').replace(u']]', u'').replace(u'en:', u'').replace(u'fa:', u'').replace(u' ',u'_')
    except:
        enlink = enlink.replace(u'[[', u'').replace(u']]', u'').replace(u'en:', u'').replace(u'fa:', u'').replace(u' ',u'_')
    if enlink.find(u'#') != -1:
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
        return False
    if enlink == u'':
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
        return False
    enlink = enlink.replace(u' ', u'_')
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit': 500,
    }
    try:
        categoryname = pywikibot.data.api.Request(site=firstsite, **params).submit()
        for item in categoryname['query']['pages']:
            case = categoryname['query']['pages'][item]['langlinks']
        for item in case:
            if item['lang'] == secondsite.code:
                intersec = item['*']
                break
        result = intersec
        if result.find('#') != -1:
            _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
            return False
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = result
        return result
    except:
        _cache[tuple([enlink, firstsite, secondsite, 'en_dic'])] = False
        return False


def switchnamespace(namespace):
    if namespace==0:
       return u' '
    if namespace==4:
       return u'wikipedia:'
    if namespace==10:
       return u'template:'
    if namespace==12:
       return u'help:'
    if namespace==14:
       return u'category:'
    return False

def revert(text2,text):
    Regexs=re.compile(ur'\{\{\s*(?:[Cc]ite|[Cc]itation)(?:\{\{.*?\}\}|.)*?\}\}') 
    citebase = Regexs.findall(text)
    citetarget = Regexs.findall(text2)
    i=-1
    for m in citebase:
           i+=1
           text2=text2.replace(citetarget[i],citebase[i])
    return text2

def getlinks(enlink,falink,NotArticle):

    site = pywikibot.Site('fa')
    enlink_2=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', enlink).strip()
    falink_2=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', falink).strip()
    if not enlink_2:
        # It is date linke like [[1999]] which is [[1999]] != [[۱۹۹۹]]
        return
    if not falink_2:
        # It is date linke like [[۱۹۹۹]] which is [[1999]] != [[۱۹۹۹]]
        return
    try:
        page = pywikibot.Page(site,enlink)
        linktos=page.getReferences()
    except:
        return False
    for page in linktos:
        namespacefa=page.namespace()
        if namespacefa in [1,2,3,5,7,8,9,11,13,15,101]:
            continue
        if NotArticle:
            #At the first it should replace at none article
            if namespacefa==0:    
                continue
        try:
            text=page.get()
        except :
            continue
        if _cache.get(tuple([page.title(),enlink,'getlinks'])):
            continue
        else:
            _cache[tuple([page.title(),enlink,'getlinks'])]=1
        time.sleep(2)    
        pywikibot.output(u'checking '+page.title()+u' .....')    
        enlink=enlink.strip()
        text2=text
        fanum=enlink.replace(u'1',u'۱').replace(u'2',u'۲').replace(u'3',u'۳').replace(u'4',u'۴').replace(u'5',u'۵')
        fanum=fanum.replace(u'6',u'۶').replace(u'7',u'۷').replace(u'8',u'۸').replace(u'9',u'۹').replace(u'0',u'۰')    
        fanum_text=re.sub(ur'[1234567890۱۲۳۴۵۶۷۸۹۰\(\)\,\،\.]',ur'', fanum).strip()
        search_list=[]

        if  fanum_text and fanum!=enlink:
            for i in [enlink,enlink.replace(u',',u'،'),enlink.replace(u' ',u'_'),enlink.replace(u' ',u'_').replace(u',',u'،')]:
                if not i in search_list:
                    search_list.append(i)
        else:
            for i in [enlink,enlink.replace(u',',u'،'),fanum,enlink.replace(u' ',u'_'),enlink.replace(u' ',u'_').replace(u',',u'،')]:
                if not i in search_list:
                    search_list.append(i)

        text2=text2.replace(u'\r',u'')
        for enlink in search_list:
            pywikibot.output(enlink)
            text2=re.sub(ur'\[\[ *(:|) *'+enlink+ur' *\]\]',ur'[[\1'+falink+ur']]',text2, re.DOTALL| re.IGNORECASE)
            text2=re.sub(u'\| *link *\= *'+enlink+u'\n',u'|link='+falink+u'\n',text2)
            Link_list = re.findall(ur'\[\[ *(:|) *([^\]\|]+) *\| *([^\]\|]+) *\]\]',text2, re.DOTALL| re.IGNORECASE)
            if Link_list:
                for mylink in Link_list:
                    if enlink.lower().replace(u'_',u' ').replace(u'،',u',').strip()==mylink[1].lower().replace(u'_',u' ').replace(u'،',u',').strip():
                        pywikibot.output(u'link >'+mylink[1]+u' '+ mylink[2])
                        #phase 1
                        Replace_list = re.findall(ur'\[\[ *(:|) *('+enlink+ur') *\| *([^\]\|]+) *\]\]',text2, re.IGNORECASE)
                        #pywikibot.output(Replace_list[0])
                        if Replace_list:
                            for replace_link in Replace_list:
                                if len(replace_link[2]) <4 and len (enlink)>3:
                                    text2=text2.replace(u'[['+replace_link[0]+replace_link[1]+u'|'+replace_link[2]+u']]',ur'[['+replace_link[0]+falink+ur'|'+replace_link[2]+u']]')                                               
                                else:
                                    if replace_link[2]==re.sub(u'[ابضصثقفغعهخحجچشسیلتنمکگظطزرذدپو]',u'',replace_link[2]):
                                        text2=text2.replace(u'[['+replace_link[0]+replace_link[1]+u'|'+replace_link[2]+u']]',ur'[['+replace_link[0]+falink+u']]')
                                    else:
                                        text2=text2.replace(u'[['+replace_link[0]+replace_link[1]+u'|'+replace_link[2]+u']]',ur'[['+replace_link[0]+falink+ur'|'+replace_link[2]+u']]') 
                        #hase 2
                        
                        if len(mylink[2]) <4 and len (mylink[1])>3:
                            text2=text2.replace(u'[['+mylink[1]+u'|'+mylink[2]+u']]',ur'[['+falink+ur'|'+mylink[2]+u']]')                                               
                        else:
                            if mylink[2]==re.sub(u'[ابضصثقفغعهخحجچشسیلتنمکگظطزرذدپو]',u'',mylink[2]):
                                text2=text2.replace(u'[['+mylink[1]+u'|'+mylink[2]+u']]',ur'[['+falink+u']]')
                            else:
                                text2=text2.replace(u'[['+mylink[1]+u'|'+mylink[2]+u']]',ur'[['+falink+ur'|'+mylink[2]+u']]')

        if text2.find(falink)==-1:
            pywikibot.output(u'\03{lightblue}could not find any link\03{default}')
        text2=revert(text2,text)
        msg=u''
        if text!=text2:
            text2,msg=ref_link_correction_core.main(text2,u'')
            if msg:
               msg=u'+'+msg
            try:
                page.put(text2,u'ربات :[[وپ:پقا|جایگزینی پیوند قرمز]] [['+enlink+u']] > [['+falink+u']] ('+BotVersion+')'+msg)
                pywikibot.output(u'\03{lightgreen}the page '+page.title()+u' had replcae item [['+enlink+u']] > [['+falink+u']]\03{default}')
            except:
                pywikibot.output(u'\03{lightred}the page '+page.title()+u' could not replaced so it passed\03{default}')
                continue
       
    return True
        
def remove_wikify (enlink,Status,Comp):
    try:
        page = pywikibot.Page(pywikibot.Site('fa'),enlink)
        linktos=page.getReferences()
        for page in linktos:
            namespacefa=page.namespace()
            if namespacefa != 0:
                continue
            try:
                text=page.get()
            except:
                continue
            text=re.sub(ur'\[\[( *'+enlink+ur' *)\|([^\]\|]+ *)\]\]',ur' \2 ',text)
            if Status=='R':
                text=re.sub(ur'\[\[ *('+enlink+ur') *\]\]',ur' \1 ',text)
            
            try:
                if Status=='R':
                    page.put(text,u'[[وپ:پقا|برداشتن ویکی‌سازی]] [['+enlink+u']] > تغییرمسیر نامشابه است ('+BotVersion+') '+str(Comp))
                else:
                    page.put(text,u'[[وپ:پقا|برداشتن ویکی‌سازی]] [['+enlink+u']]> بخشی از یک مقاله است (در ویکی‌انگلیسی# دارد) ('+BotVersion+') '+str(Comp))
                pywikibot.output(u'\03{lightblue}the page '+page.title()+u' remove wikifay [['+enlink+u']]\03{default}')
            except:
                pywikibot.output(u'\03{lightred}the page '+page.title()+u' could not replaced so it passed\03{default}')
                continue
    except:
        return
        
def get_query():
    querys='SELECT /* SLOW_OK */ DISTINCT pl_title,pl_namespace FROM pagelinks INNER JOIN page ON pl_from = page_id WHERE pl_title NOT IN(SELECT page_title FROM page WHERE page_namespace = 0) AND pl_namespace = 0 AND page_namespace = 0;'
    pywikibot.output(querys)
    site  = pywikibot.Site('fa')
    conn = mysqldb.connect("fawiki.labsdb", db = site.dbName()+ '_p',
                           user = config.db_username,
                           passwd = config.db_password)
    cursor = conn.cursor()
    cursor.execute(querys)
    results = cursor.fetchall()
    return results
    
def run(results, NotArticle):
    for enlink in results:
        if switchnamespace(enlink[1]):# if the link is from permited namespaces 
            enlink=switchnamespace(enlink[1])+unicode(enlink[0],'UTF-8').strip()
            pywikibot.output(enlink)
            enlink=enlink.replace(u'_',u' ').strip()
            enlink2=re.sub(u'[ابضصثقفغعهخحجچشسیلتنمکگظطزرذدپو]',ur'', enlink)
            if enlink2==enlink:
                count=-1
                for i in u'۰۱۲۳۴۵۶۷۸۹':
                    count+=1
                    enlink=enlink.replace(i,str(count))
                #unwikify the redirect links
                redirect_find_result, Comp =redirect_find(enlink)
                if not redirect_find_result:
                    pywikibot.output(u'It was redirect so lets remove the wikify!')
                    remove_wikify (enlink,'R',Comp)
                    continue
                falink=englishdictionry(enlink ,'en','fa')
                pywikibot.output(falink)
                if falink:
                    if namespacefinder(enlink ,'en')!=namespacefinder(falink ,'fa'):
                        continue    
                    pywikibot.output(u'---------------------------------------------')
                    pywikibot.output(enlink+u' > '+falink)
                    a=getlinks(enlink,falink,NotArticle)
                else:
                    #unwikify the # links
                    if u'#' in enlink:
                        remove_wikify (enlink,'#',Comp)
            else:
                pywikibot.output(u'it has farsi char')
    del results,enlink

#At the first it should do replacing at none article
run(get_query(),True)
#Now do replacing at the articles
run(get_query(),False)
'''
#for test
results=[['Let the Right One In (film)',0]]
run(results,True)
run(results,False)
'''
