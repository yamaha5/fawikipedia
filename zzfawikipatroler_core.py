﻿#!/usr/bin/python
# -*- coding: utf-8 -*-
# Reza (User:yamaha5) 
# Distributed under the terms of MIT License (MIT)
import fa_cosmetic_changes_core
import pywikibot,codecs,string,re,sys
from pywikibot.compat import query
from pywikibot import login 
from pywikibot import pagegenerators
from pywikibot import config
from datetime import timedelta,datetime
import MySQLdb as mysqldb
pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0
faSite = pywikibot.Site('fa')
enSite = pywikibot.Site('en')
tags = ur'b|big|blockquote|charinsert|code|comment|del|div|em|gallery|hyperlink|i|includeonly|imagemap|inputbox|link|math|noinclude|nowiki|pre|ref|s|small|source|startspace|strong|sub|sup|template|timeline'
faChrs = u'ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیيك'
langs = u'انگلیسی|آلمانی|اسپانیایی|فرانسوی|روسی|ایتالیایی|لاتین|اسکاتلندی|هلندی|هندی|اردو|پشتو|مصری|تاجیکستانی|قرقیزستانی|ازبکستانی|ترکی|یونانی|چینی|ژاپنی|کره‌ای|تایلندی|[فپ]ارسی'
zaed = ur"''متن مورب''|'''متن ضخیم'''|\[\[پرونده:مثال\.jpg]]|=+ متن عنوان =+|:خط تو رفته\n?|<nowiki>اینجا متن قالب‌بندی‌نشده وارد شود</nowiki>|\# مورد فهرست شماره‌ای\n?|\* مورد فهرست گلوله‌ای|<sub>متن زیرنویس</sub>|<sup>متن بالانویس</sup>|<small>متن کوچک</small>|<big>متن بزرگ</big>|#(؟:تغییرمسیر|REDIRECT) \[\[(?:نام صفحه مقصد|نام صفحه)]]|\{\| class=\.wikitable\.\n\|-\n! متن عنوان !! متن عنوان !! متن عنوان\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|-\n\| مثال \|\| مثال \|\| مثال\n\|}|<gallery>\nپرونده:مثال\.jpg\|عنوان ۱\nپرونده:مثال.jpg\|عنوان ۲\n</gallery>|<ref>{{یادکرد\|نویسنده = \|عنوان = \| ناشر = \|صفحه = \|تاریخ = }}</ref>|<ref>{{یادکرد وب\|نویسنده = \|نشانی = \|عنوان = \| ناشر = \|تاریخ = \|تاریخ بازدید = }}</ref>|<ref>{{یادکرد خبر\|نام = \|نام خانوادگی = \|همکاران = \|پیوند = \|عنوان = \|اثر = \| ناشر = \|صفحه = \|تاریخ = \|بازیابی = }}</ref>|\[\[رده:]]|\[\[en:]]|\[\[fa:.*?]]|\[\[عنوان پیوند]]|\{\{\s*}}|\[\[\s*\|?\s*]]|<!-- *?-->"
msg=u' '
version='5.7'
_cache={}
def login_fa(bot):    
    if bot==u'FawikiPatroller':
        try:
            password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
        except:
            password_fa = open("/home/reza/compat/passfile2", 'r')
    else:
        try:
            password_fa = open("/data/project/rezabot/pywikipedia/passfile", 'r')
        except:
            password_fa = open("/home/reza/compat/passfile", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    usernames=password_fa.split('(')[1].split(',')[0].split(')')[0].strip()
    #-------------------------------------------
    botlog=pywikibot.data.api.LoginManager(password=passwords, sysop=False, site=faSite, user=usernames)
    botlog.login()
def not_redirect(page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, faSite, 'not_redirect'])):
        return _cache[tuple([page_link, faSite, 'not_redirect'])]
    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link
    }
    query_page = pywikibot.data.api.Request(site=faSite, **params).submit() 
    try:
        redirect_link=query_page[u'query'][u'redirects'][0]['to']
        _cache[tuple([page_link, faSite, 'not_redirect'])]=False
        return False
    except:
        if 'missing=""' in str(query_page):
            _cache[tuple([page_link, faSite, 'not_redirect'])]=False
            return False
        else:
            _cache[tuple([page_link, faSite, 'not_redirect'])]=True
            return True

def purgquery(falink):
    if _cache.get(tuple([falink, faSite, 'purgquery'])):
        return _cache[tuple([falink, faSite, 'purgquery'])]
    if falink:
        falink=falink.replace(u' ',u'_')
        params = {
                'action': 'purge',
                'titles': falink,
                'forcelinkupdate': 1
        }

        try:
            categoryname = pywikibot.data.api.Request(site=faSite, **params).submit()
            for item in categoryname[u'purge']:
                templateha=item[u'title']
                break
        except: 
            pass
    enlink=englishdictionry(falink ,'fa','en')
    if enlink:
        enlink=enlink.replace(u' ',u'_')
        params = {
                    'action': 'purge',
                    'titles': enlink,
                    'forcelinkupdate': 1
        }
        try:
            categoryname = pywikibot.data.api.Request(site=enSite, **params).submit()
            for item in categoryname[u'purge']:
                templateha=item[u'title']
                break
        except: 
            pass
    _cache[tuple([falink, faSite, 'purgquery'])]=True

def englishdictionry(link ,firstsite,secondsite):
    link=link.replace(u' ',u'_')
    if _cache.get(tuple([link, firstsite, 'englishdictionry'])):
        return _cache[tuple([link, firstsite, 'englishdictionry'])]
    if link==u'':
        _cache[tuple([link, firstsite, 'englishdictionry'])] = u''
        return u''    

    site = pywikibot.Site(firstsite)
    sitesecond= pywikibot.Site(secondsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': link,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname[u'query'][u'pages']:
            case=categoryname[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==secondsite:
                intersec=item[u'*']
                break
        result=intersec
        if result.find('#')!=-1:
            _cache[tuple([link, firstsite, 'englishdictionry'])] = u''
            return u''
        _cache[tuple([link, firstsite, 'englishdictionry'])] = result
        return result
    except: 
        _cache[tuple([link, firstsite, 'englishdictionry'])] = u''
        return u''

def check_user_editnum(username,editnum):
    username=username.replace(u' ',u'_').replace(u'کاربر:',u'').replace(u'user:',u'').replace(u'User:',u'')
    if _cache.get(tuple([username, faSite, 'check_user_editnum'])):
        return _cache[tuple([username, faSite, 'check_user_editnum'])]
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'editcount'    
    }
    try:
        usernamequery = pywikibot.data.api.Request(site=faSite, **params).submit()
        if usernamequery[u'query'][u'users'][0][u'editcount']>editnum:
            _cache[tuple([username, faSite, 'check_user_editnum'])]=True
            return True
        else:
            _cache[tuple([username, faSite, 'check_user_editnum'])]=False
            return False
    except:
        _cache[tuple([username, faSite, 'check_user_editnum'])]=False
        return False

def get_interwikis(link):
    link=link.replace(u' ',u'_')
    if _cache.get(tuple([link, faSite, 'get_interwikis'])):
        return _cache[tuple([link, faSite, 'get_interwikis'])]
    if link.find('#')!=-1:
        _cache[tuple([link, faSite, 'get_interwikis'])]=[]
        return []
    if link==u'':
        _cache[tuple([link, faSite, 'get_interwikis'])]=[]
        return []    
    case=[]
    try:
        params = {
            'action': 'query',
            'prop': 'langlinks',
            'titles': link,
            'redirects': 1,
            'lllimit':500,
        }
        pagename = pywikibot.data.api.Request(site=faSite, **params).submit()
        for item in pagename[u'query'][u'pages']:
            case=pagename[u'query'][u'pages'][item][u'langlinks']
            _cache[tuple([link, faSite, 'get_interwikis'])]=case
            return case
    except: 
        _cache[tuple([link, faSite, 'get_interwikis'])]=[]
        return []

def get_cat(link):
    link=link.replace(u' ',u'_')
    if _cache.get(tuple([link, faSite, 'get_cat'])):
        return _cache[tuple([link, faSite, 'get_cat'])]
    if link.find('#')!=-1:
        _cache[tuple([link, faSite, 'get_cat'])]=[]
        return []
    if link==u'':
        _cache[tuple([link, faSite, 'get_cat'])]=[]
        return []    
    case=[]
    params = {
        'action': 'query',
        'prop': 'categories',
        'titles': link,
        'clshow': '!hidden',
        'cllimit': 500,
    }
    try:
        pagename = pywikibot.data.api.Request(site=faSite, **params).submit()
        for item in pagename[u'query'][u'pages']:
            case=pagename[u'query'][u'pages'][item][u'langlinks']
            _cache[tuple([link, faSite, 'get_cat'])]=case
            return case
    except: 
        _cache[tuple([link, faSite, 'get_cat'])]=[]
        return []

def check_links(workpage):
    workpage=workpage.replace(u' ',u'_')
    if _cache.get(tuple([workpage, faSite, 'check_links'])):
        return _cache[tuple([workpage, faSite, 'check_links'])]
    params = {
        'action': 'query',
        'prop': 'extlinks',
        'titles': workpage
    }
    try:
        usernamequery = pywikibot.data.api.Request(site=faSite, **params).submit()
        links=usernamequery[u'query'][u'pages'][0][u'extlinks']
        if len(links)>0:
            _cache[tuple([workpage, faSite, 'check_links'])]=False
            return False
        else:
            _cache[tuple([workpage, faSite, 'check_links'])]=True
            return True
    except:
        _cache[tuple([workpage, faSite, 'check_links'])]=True
        return True

def check_user_admin(username):
    username=username.replace(u' ',u'_')
    if _cache.get(tuple([username, faSite, 'check_user_admin'])):
        return _cache[tuple([username, faSite, 'check_user_admin'])]
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'groups'
    }
    try:
        usernamequery = pywikibot.data.api.Request(site=faSite, **params).submit()
        if not 'sysop' in usernamequery[u'query'][u'users'][0][u'groups']:
            _cache[tuple([username, faSite, 'check_user_admin'])]=True
            return True
        else:
            if not check_user(username):# if user is syso-bot like user:rezabot it dosen't care
                _cache[tuple([username, faSite, 'check_user_admin'])]=True
                return True
            _cache[tuple([username, faSite, 'check_user_admin'])]=False
            return False
    except:
        _cache[tuple([username, faSite, 'check_user_admin'])]=True
        return True
        
def check_user(username):
    username=username.replace(u' ',u'_')
    if _cache.get(tuple([username, faSite, 'check_user'])):
        return _cache[tuple([username, faSite, 'check_user'])]
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'groups'
    }
    try:
        usernamequery = pywikibot.data.api.Request(site=faSite, **params).submit()
        if not 'bot' in usernamequery[u'query'][u'users'][0][u'groups']:
            _cache[tuple([username, faSite, 'check_user'])]=True
            return True
        else:
            _cache[tuple([username, faSite, 'check_user'])]=False
            return False
    except:
        _cache[tuple([username, faSite, 'check_user'])]=False
        return False

def templatequery(enlink,site):
    temps=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.replace(u' ',u'_')
    enlink=enlink.split(u'#')[0].strip()
    if _cache.get(tuple([enlink, site, 'templatequery'])):
        return _cache[tuple([enlink, site, 'templatequery'])]
    if enlink==u'':
        _cache[tuple([enlink, site, 'templatequery'])]=[]
        return []    
    params = {
            'action': 'query',
            'prop':'templates',
            'titles': enlink,
            'redirects': 1,
            'tllimit':500,
    }

    try:
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' '))
        _cache[tuple([enlink, site, 'templatequery'])]=temps
        return temps
    except:
        _cache[tuple([enlink, site, 'templatequery'])]=[]
        return []

def Page_size(link):
    link=link.replace(u' ',u'_')
    if _cache.get(tuple([link, faSite, 'Page_size'])):
        return _cache[tuple([link, faSite, 'Page_size'])]
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': link,
    }
    try:
        queryresult = pywikibot.data.api.Request(site=faSite, **params).submit()  
        for item in queryresult[u'query'][u'pages']:
            length=queryresult[u'query'][u'pages'][item][u'length']
        _cache[tuple([link, faSite, 'Page_size'])]=length
        return length
    except:
        _cache[tuple([link, faSite, 'Page_size'])]=1
        return 1

def check_admin(page_history):
    users=[]
    for revistion in page_history:
        if not revistion[2] in users:
            users.append(revistion[2])
            if not check_user_admin(revistion[2]):#if bot found syso user in article's history it will escape adding delete tag
                return False
    return True
def check_page(workpage):
        try:
            page = pywikibot.Page(faSite,workpage)
            text=page.get()
            page_history=page.getVersionHistory()
            first_user=page_history[-1][2]
            time_stamp=page_history[-1][1]
            #pywikibot.output(first_user)
            #pywikibot.output(time_stamp)
        except pywikibot.IsRedirectPage:
            page = page.getRedirectTarget()
            try:
                text=page.get()
                page_history=page.getVersionHistory()
                first_user=page_history[-1][2]
                time_stamp=page_history[-1][1]
            except:
                return False,False,False,False
        except:
            return False,False,False,False
        date=time_stamp.split('T')[0].strip()
        year=int(date.split('-')[0].strip())-2000
        month=int(date.split('-')[1].strip())
        day=int(date.split('-')[2].strip())
        timestamp=year*365+month*30+day
        return text,first_user,timestamp,page_history

def addlable (workpage,resion,user):
        msg=u'ربات-کاربر:[[ویکی‌پدیا:حذف زمان‌دار|حذف زمان‌دار]] > '+resion
        try:
             page = pywikibot.Page(faSite,workpage)
             text=page.get()
             page.put(u'{{جا:حذف زمان‌دار|'+resion+u'}}\n'+text.strip(), msg)
        except:
            pywikibot.output(u'an error is accured!')
            pass
        try:
            try:
                 pageuser = pywikibot.Page(faSite,u'بحث کاربر:'+user)    
                 text_user=pageuser.get()
            except pywikibot.IsRedirectPage:
                pageuser = pageuser.getRedirectTarget()
                try:
                    text_user=pageuser.get()
                except:
                    pywikibot.output(u"couldn't open user page")    
            pageuser.put(text_user+u'\n{{subst:هشدار حذف زمان‌دار|'+workpage+u'|اهمیت='+resion+u'}} ~~~~', msg)
        except:
            pywikibot.output(u"couldn't open user page")

def user_alarm (userdict,user_article_dict):
        for user in userdict:
            text_user=u''
            articles='|'.join(user_article_dict[user])
            articles=u'[['+articles.replace(u'|',u']]، [[')+u']]'
            alarms=u'{{جا:کاربر:FawikiPatroller/هشدار۱|'+articles+u'$'+'$'.join(userdict[user])+u'}}'
            alarms=alarms.replace(u'$',u'|\n::::*')    
            msg=u'ربات-کاربر:ارسال پیام دربارهٔ نحوهٔ ویرایش '+articles 
            try:
                pageuser = pywikibot.Page(faSite,u'بحث کاربر:'+user)
                text_user=pageuser.get()
            except pywikibot.NoPage:
                text_user=u'\n'
            except pywikibot.IsRedirectPage:
                pageuser = pageuser.getRedirectTarget()
                try:
                    text_user=pageuser.get()
                except pywikibot.NoPage:
                    text_user=u'\n'
                except:
                    pywikibot.output(u"couldn't open user page")
                    text_user=u''               
            except:
                pywikibot.output(u"couldn't open user page")

            if text_user and text_user.find(articles.replace(u' ',u'_'))==-1 and text_user.find(articles.replace(u'_',u' '))==-1:
                    pageuser.put(text_user+u'\n'+alarms, msg)
            else:
                if not text_user:
                     pywikibot.output(u"\03{lightred}Bot could'nt add alarm for User:"+user+u'\03{default}')
                else:
                     pywikibot.output(u"\03{lightred}User page had this alarm so alarming to User:"+user+u' is stopped\03{default}')
            
def findsection(text):
    text=text.replace(u'\r',u'').replace(u'\n==',u'@@@@\n==')
    sections=text.split(u'@@@@')
    toppage=sections[0].strip()
    return sections,toppage

def data2fa(number, strict=False):
    data=pywikibot.DataPage(int(number))
    try:
        items=data.get()
    except:
        return ""
    if isinstance(items['links'],list):
        items['links']={}
    if items['links'].has_key('fawiki'):
        return items['links']['fawiki']['name']
    if strict:
        return ""
    if items['label'].has_key('fa'):
        return items['label']['fa']
    try:
        return items['label']['en']
    except:
        return ""

def ClaimFinder(page_title,claim_num):
    fa_result=False
    fa_result_more=[]
    en_wdata=pywikibot.DataPage(pywikibot.Page(faSite,page_title))
    try:
        items=en_wdata.get()
    except:
        return False
    if items['claims']:
        case=items['claims']
        for i in case:
            if i['m'][1]==claim_num:
                fa_result=data2fa(i[u'm'][3][u'numeric-id'])
                break
    if fa_result:
        fa_result=fa_result.strip()
    return fa_result

def senario_D(text,page_title):
        text=text.replace(u'\n\n',u'\n')
        pagesize1=sys.getsizeof (text)
        fa_text2=re.sub(u'\{\{([iI]nfo|جعبه)(?:\{\{.*?\}\}|[^\}])*\}\}',u'',text, re.S)
        fa_text2=re.sub(u'\[\[رده\:.*?\]\]',u'',fa_text2)
        pagesize2=sys.getsizeof (fa_text2)
        main_page_size=Page_size(page_title)
        rasio=(float(pagesize2)/float(pagesize1))
        if (u'<ref' in text or u'{{یادکرد' in text or u'{{Citation' in text or u'{{citation' in text):
            if not (u'pywikibot.org' in text or u'* ویکی' in text or u'*ویکی' in text):
                return False
        if rasio*main_page_size<300 and ClaimFinder(page_title,31)==u'انسان':
                return u'مقالهٔ کوتاه دربارهٔ انسان و نبود مطلب کافی برای مرتفع کردن شرایط [[وپ:سرشناسی]]'
        return False

def senario_A(text,page_history,page_title,interwiki_list):
        text=text.replace(u'[[رده:مقاله‌های ایجاد شده توسط ایجادگر]]',u'').replace(u'\n\n',u'\n')
        if not interwiki_list:
            if Page_size(page_title)<700:
                if check_admin(page_history):
                    return u'مقالهٔ کوتاه و بدون میان‌ویکی'    
                else:
                    pywikibot.output(u'Admin has checked it!')    
                    return False
        return False

def senario_B(text,page_title,interwiki_list):
        text=text.replace(u'[[رده:مقاله‌های ایجاد شده توسط ایجادگر]]',u'').replace(u'\n\n',u'\n')
        textfa=text
        if interwiki_list:    
            if Page_size(page_title)<500:
                 return u'میان‌ویکی دارد ولی کوتاه است!'
        else:
            if Page_size(page_title)<200:
                 return u'مقالهٔ خیلی کوتاه'
            if Page_size(page_title)<300:
                if not (u'<ref' in text or u'{{یادکرد' in text or u'{{Citation' in text or u'{{citation' in text):
                    return u'مقالهٔ کوتاه و بدون منبع'
        return False

def senario_C(text,page_title,interwiki_list):
        if not check_links(page_title):
            return False
        text=text.replace(u'[[رده:مقاله‌های ایجاد شده توسط ایجادگر]]',u'').replace(u'\n\n',u'\n')
        if not interwiki_list and text.find(u'[[')==-1 and text.find(u'منبع')==-1 and text.find(u'منابع')==-1 and text.find(u'<ref')==-1 and text.find(u'{{یادکرد')==-1 and text.find(u'{{Citation')==-1 and text.find(u'{{citation')==-1:    
            return u'کپی‌کاری، بدون میان‌ویکی و رده'
        return False

def update_page(text,user,workpage_page,msg):    
    try:
        page = pywikibot.Page(faSite,workpage_page)
        msg=msg.replace(u'+ +',u'+')
        page.put(text,msg)
        pywikibot.output(u'\03{lightblue}update is done!\03{default}')
    except:
        pywikibot.output(u'\03{lightred}---------it does not updated!\03{default}')

def senario_E(text,user,workpage_page,userdict,user_article_dict,interwiki_list):
    #pywikibot.output(u'*******////****')
    page= pywikibot.Page(faSite,workpage_page)
    msg=u' '
    new_text,cleaning_version,msg_clean=fa_cosmetic_changes_core.fa_cosmetic_changes(text,page,msg)
    msg=u'ربات:مرتب‌سازی عنوان‌ها'+msg_clean
    msg=msg.replace(u'+ +',u'+')
    fapage_title=workpage_page.title()
    enpage_title=englishdictionry(fapage_title,'fa','en')
    entemps=templatequery(enpage_title,enSite)
    fatemps=templatequery(fapage_title,faSite)
    At_faArticle=u'در مقالهٔ [['+fapage_title+u']] > '
    if text!=new_text:
        update_page(new_text,user,workpage_page,msg)    
        text=new_text
    sections,toppage=findsection(text)
    if len(sections)<2:
        pywikibot.output(u'\03{lightred}The article does not have any section!\03{default}')
        sections,toppage=[text],text
        
    alarm_text=u'{{جا:کاربر:FawikiPatroller/هشدار۱|'+workpage_page+u'|'
    alarmtup=[]
    alarmnum=0
    mytext=toppage+u'\n'
    after_source=False
    after_source_text=u'\n'
    for section in sections:
        if section.find(u'== منابع ==')!=-1 or section.find(u'==منابع==')!=-1 or section.find(u'== منبع‌ها ==')!=-1 or section.find(u'==منبع‌ها==')!=-1:
           after_source=True
           continue
        else:
            if not after_source:
                mytext+=section
        if after_source:
            after_source_text+=section

    mytext=re.sub(ur'\[\[رده\:.*?\]\]',u'',mytext)
    #-----------------------------------------------------------------
    force=False
    enchar=u'QWERTYUIOPASDFGHJKLZXCVBNM'
    if mytext.strip() and mytext.find(u'خرد}}')!=-1 and after_source_text.find(u'خرد}}')==-1 and len(sections)>1:#1
        pywikibot.output(after_source_text)
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u"طبق [[وپ:بخش‌بندی|شیوهٔ ویرایش مرسوم در ویکی‌پدیا]] '''[[الگو:خرد]]''' باید بعد از بخش منابع قرار داده شود."
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'

    if Page_size(workpage_page)<4000 and text.find(u'خرد}}')==-1:#2
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u'با توجه به حجم کم [[:رده:الگو:مقاله‌های خرد|الگوی خرد مناسب]] را در انتهای مقاله قرار دهید.'
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'

    if mytext.find(u'[[')==-1 and sections:#3    
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u'[[وپ:ویکی‌سازی|ویکی‌سازی]] نمائید.'
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
        
    if text.find(u'==')==-1 and workpage_page.find(u'فهرست')==-1:#4
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u'[[وپ:بخش‌بندی|بخش‌بندی]] نمائید.'
        force=True
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'

    if (u'Template:Infobox' in entemps) and enpage_title:
        checkinfo=True
    else:
        checkinfo=False

    if checkinfo and (not u'الگو:Infobox' in fatemps) and text.find(u'{{جعبه')==-1 and text.find(u'{|')==-1 and workpage_page.find(u'فهرست')==-1:#5
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u'[[وپ:جعبه اطلاعات|جعبه اطلاعات]] مناسب بیافزائید.'
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
        
    if mytext.strip() and text.find(u'== منابع ==')==-1 and text.find(u'== پانویس ==')==-1 and text.find(u'==پانویس==')==-1 and text.find(u'==منابع==')==-1:#6
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u'منبع مناسب بیافزائید و همچنین [[وپ:بخش‌بندی|زیربخش منابع]] را در پائین مقاله بیافزائید.'
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
        
    if mytext.strip() and not toppage.strip() and workpage_page.find(u'فهرست')==-1:#7
        alarmnum+=1
        force=True
        alarm_message=At_faArticle
        alarm_message+=u'طبق [[وپ:بخش‌بندی|شیوهٔ نگارش]] در ویکی‌پدیا باید در بخش ابتدایی مقاله چند خط مطلب به عنوان مقدمه وجود داشته باشد.'
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'

    if toppage.find(u"'''")==-1 and toppage and workpage_page.find(u'فهرست')==-1:#8
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u"طبق [[وپ:بخش‌بندی|شیوهٔ نگارش]] در ویکی‌پدیا باید عنوان مقاله در بخش مقدمه با <nowiki>'''</nowiki> پررنگ شود."
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
    
    textcat=text.replace(u'[[رده:مقاله‌های ایجاد شده توسط ایجادگر]]',u'').replace(u'\n\n',u'\n')#9
    if textcat.find(u'[[رده:')==-1 and textcat.find(u'[[category:')==-1 and textcat.find(u'[[Category:')==-1 and not get_cat(link):
        alarmnum+=1
        force=True
        alarm_message=At_faArticle
        alarm_message+=u"[[وپ:رده‌بندی|رده‌بندی]] انجام نشده‌است و به علت نبود [[وپ:میان‌ویکی|میان‌ویکی]] ربات‌های ردهٔ همسنگ نمی‌تواند به مقالهٔ شما رده بیافزایند در صورت امکان ردهٔ مناسب یا میان‌ویکی را به مقاله بیافزائید."
        if len(interwiki_list)>0 and enpage_title:#اگر میان‌ویکی نداشت
            encats=getEnCat(enpage_title)
            encats_Text=u'، '.join(encats)
            alarm_message=At_faArticle
            alarm_message+=u"[[وپ:رده‌بندی|رده‌بندی]] انجام نشده‌است و به علت نبود [[ویکی‌پدیا:رده همسنگ|ردهٔ همسنگ با ویکی‌پدیای انگلیسی]] ربات‌های ردهٔ همسنگ نتوانستند به مقالهٔ شما رده بیافزایند در صورت امکان رده‌های زیر را همراه با میان‌ویکی ایجاد نمائید تا ربات‌های ردهٔ همسنگ آن را به این مقاله و مقالات مشابه بیافزایند."
            if len(encats)==1:
                alarm_message+=u"\n::::***"+encats_Text+u" ردهٔ همسنگ '''مورد نیاز''' برای مقالهٔ [["+fapage_title+u"]] است؛ لطفاً در ساخت آن کمک کنید."
            else:
                alarm_message+=u"\n::::***"+encats_Text+u" رده‌های همسنگ '''مورد نیاز''' برای مقالهٔ [["+fapage_title+u"]] است؛ لطفاً در ساخت آنها کمک کنید."
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
        
    if toppage.strip() and workpage_page.find(u'فهرست')==-1 :#10
        passport=False
        if toppage.find(u'(')<250 and toppage.find(u'(')!=-1 and toppage.find(u')')!=-1:
            for i in enchar:
                entext=toppage.split(u'(')[1].split(u')')[0].strip()
                if entext.find(i)!=-1 or entext.find(i.lower())!=-1:
                    if fatemps:
                        if not u'الگو:Lang' in fatemps:
                            passport=True
                    else:
                        passport=True        
                    break
        if not check_user_editnum(user,3000):
            if passport:
                alarmnum+=1
                alarm_message=At_faArticle
                alarm_message+=u"برای نوشتن معادل‌های غیر فارسی از {{الگو|به زبان}} استفاده نمائید."
                pywikibot.output(alarm_message)
                alarmtup.append(alarm_message)
                alarm_text+=alarm_message+u'|'
    
        if (text.find(u'.wikipedia.org')!=-1 or text.find(u'*ویکی')!=-1 or text.find(u'* ویکی')!=-1):
            if len(interwiki_list)<1:#11
                alarmnum+=1
                alarm_message=At_faArticle
                alarm_message+=u"ویکی‌پدیا به زبان دیگر به عنوان منبع ذکر شده‌است یا پیوند به آن وجود دارد ولی مقاله [[وپ:میان‌ویکی|میان‌ویکی]] ندارد. میان‌ویکی مناسب را به مقاله بیافزائید یا اگر مقاله معادلی در ویکی‌های دیگر ندارد پیوند به ویکی‌پدیا را از مقاله بزدائید؛ توجه داشته باشید که نمی‌توان از ویکی‌پدیا به عنوان منبع استفاده کرد."
                force=True
                pywikibot.output(alarm_message)    
                alarmtup.append(alarm_message)
                alarm_text+=alarm_message+u'|'
    if not check_user_editnum(user,2000):
        for i in enchar+u',0123456789'+u"'":#12
            if workpage_page.find(i)!=-1 or workpage_page.find(i.lower())!=-1:
                alarmnum+=1
                alarm_message=At_faArticle
                alarm_message+=u"عنوان را با حروف فارسی ترجمه یا آوانگاری نمائید؛ در ویکی‌پدیای فارسی [[وپ:عنوان|عنوان مقاله‌ها]] باید با حروف فارسی نوشته شوند."
                force=True
                pywikibot.output(alarm_message)    
                alarmtup.append(alarm_message)
                alarm_text+=alarm_message+u'|'
                break
    
    textdash=text.replace(u'۱',u'1').replace(u'۲',u'2').replace(u' :',u'').replace(u': ',u'').replace(u':',u'').replace(u'\r',u'')
    textdash=re.sub(r'\[\[.(?:\[\[.*?\]\]|[^\]])*\]\]','',textdash, re.S)
    if textdash.find(u'\n1')!=-1 and textdash.find(u'\n2')!=-1:#13 
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u"به جای استفاده از اعداد شمارنده در سرخطوط مانند''' ۱- ۲-''' و... یا''' ۱) ۲)''' و... از علامت # استفاده نمائید.(برای اطلاعات بیشتر [[ویکی‌پدیا:آموزش سریع|آموزش سریع]] را مطالعه نمائید.)"
        pywikibot.output(alarm_message)    
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
    
    if string.count(text,u'{{سخ}}')>3 and workpage_page.find(u'فهرست')==-1 and len(interwiki_list)<0:#14  
        alarmnum+=1
        alarm_message=At_faArticle
        alarm_message+=u"استفاده بیش از حد از الگوی {{الگو|سخ}} یا <nowiki><br></nowiki> در متن درست نیست به جای آن دوبار دکمهٔ {{key press|Enter}} بزنید."
        pywikibot.output(alarm_message)
        alarmtup.append(alarm_message)
        alarm_text+=alarm_message+u'|'
    if alarmnum > 3 or force:
        pywikibot.output(u'\03{lightgreen}'+workpage_page+u' is added to bad edituin list!\03{default}')
        alarm_text=alarm_text[:-1]+u'}}'
        #-------------------------------------alarms------------
        if user in userdict:
            for item in alarmtup:
                userdict[user].append(item)
        else:
            userdict[user]=alarmtup
        #---------------------------------------articles------------------
        if user in user_article_dict:
            user_article_dict[user].append(workpage_page)
        else:
            user_article_dict[user]=[workpage_page]
        #------------------------------------------------------------------
    return user_article_dict,userdict
    
def pagecondition(text,page_history,user,page_title,userdict,user_article_dict):
        interwiki_list=get_interwikis(page_title)
        workpageok=senario_D(text,page_title)
        if workpageok:
            return workpageok,False,False
        workpageok=senario_A(text,page_history,page_title,interwiki_list)
        if workpageok:
            return workpageok,False,False
        workpageok=senario_B(text,page_title,interwiki_list)    
        if workpageok:
            return workpageok,False,False
        workpageok=senario_C(text,page_title,interwiki_list)
        if workpageok:
            return workpageok,False,False
        user_article_dict,userdict=senario_E(text,user,page_title,userdict,user_article_dict,interwiki_list)
        return False,user_article_dict,userdict

def new_page():
    titles=[]
    query="select /* SLOW_OK */ rc_title from recentchanges join page on rc_cur_id=page_id where rc_new=1 and rc_namespace=0 and page_is_redirect=0 and page.page_len>70 and rc_deleted=0 and DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 3 DAY)>rc_timestamp GROUP BY rc_timestamp DESC LIMIT 2020;"
    conn = mysqldb.connect("fawiki.labsdb", db = faSite.dbName(),user = config.db_username,passwd = config.db_password)
    cursor = conn.cursor()
    query = query.encode(faSite.site.encoding())
    cursor.execute(query)
    results = cursor.fetchall()
    for raw in results:
       titles.append(unicode(raw[0],'UTF-8'))
    return titles

def english_num(text):
    counti=-1
    for i in u'۰۱۲۳۴۵۶۷۸۹':
        counti+=1
        text=text.replace(i,str(counti))
        
    return text

def getEnCat(enpage_title):
    our_cats=[]
    try:
        page = pywikibot.Page(enSite,enpage_title)
        cats=page.categories()
        for cat in cats:
            cat=cat.title().replace(u'_',u' ').replace(u'category:',u'').replace(u'Category:',u'')
            cat=u"'''[[:en:Category:"+cat+u"]]'''"
            our_cats.append(cat)
        return our_cats
    except pywikibot.IsRedirectPage:
        return []
    except:
        return []

def main():
    login_fa(u'Rezabot')
    '''
    genfa = pagegenerators.NewpagesPageGenerator(3000,False, None,0)
    genfa = pagegenerators.PreloadingGenerator( genfa,60)
    for workpage in genfa:
        pagescounter+=1
        #print pagescounter
        #if pagescounter>600:
        pagelist.append(workpage)
    '''
    userdict,user_article_dict={},{}
    #------------------------date now-------------------------
    now = datetime.now()
    now = str(now)
    todaynum=int(now.split('-')[2].split(' ')[0])+int(now.split('-')[1])*30+(int(now.split('-')[0])-2000)*365
    #-----------------------------------------------------
    pagelist=new_page()
    counter,pagescounter=0,0
    #pagelist=[u'AZERTY',u'QWERTZ']
    for workpage in pagelist:
        if not not_redirect(workpage):
            pywikibot.output(u'>> \03{lightred}The Page '+workpage+u' was Redirect so it is passed!\03{default}')
            continue
        purgquery(workpage)
        workpage=workpage.replace(u'_',u' ')
        pagescounter+=1
        pywikibot.output(u'\03{lightred}N '+str(pagescounter)+u'\03{default}-------------- '+workpage+u' --------------')
        text,user,timestamp,page_history=check_page(workpage)    
        if not user:
            pywikibot.output(u'User was bot')
            continue
        if timestamp<todaynum-10:
            pywikibot.output(u'The article is earlier than \03{lightblue}10 days ago\03{default}')
            break
        if timestamp<todaynum-2:
        #if timestamp:    
            if check_user(user):# if the first user is not bot and article is from 2 days ago it will continue

                counter+=1
                if counter>1000:#number of check for each time
                   break
                if  text.find(u'{{نام کوچک}}')!=-1 or text.find(u'{{نام خانوادگی}}')!=-1 or text.find(u'ابهام‌زدائی')!=-1 or text.find(u'ابهام زدائی')!=-1 or text.find(u'حذف سریع')!=-1 or text.find(u'{{انتقال به')!=-1 or text.find(u'ادغام تاریخچه')!=-1 or text.find(u'ادغامت')!=-1 or text.find(u'disambig')!=-1 or text.find(u'Disambig')!=-1 or text.find(u'ابهام زدایی')!=-1 or text.find(u'ابهام‌زدایی')!=-1 or text.find(u'حذف زمان‌دار/پیغام')!=-1 or text.find(u'در دست ویرایش ۲')!=-1 or text.find(u'{{پیشنهاد حذف۲')!=-1:
                    continue
                resion,user_article_dict,userdict=pagecondition(text,page_history,user,workpage,userdict,user_article_dict)
                if resion:
                    login_fa(u'FawikiPatroller')
                    addlable(workpage,resion,user)
                    login_fa(u'Rezabot')    
            else:
                pywikibot.output(u'User was bot')
                continue
        else:
            pywikibot.output(u'The article is later than \03{lightpurple}2 days\03{default}')
    #------------alarm start---------
    pywikibot.output(u'\03{lightpurple}******** Starting alarm to users***************\03{default}')
    login_fa(u'FawikiPatroller')
    article_list_msg=[]
    for userx in userdict:
        msgcount=-1
        pywikibot.output(u'\03{lightred}>>>>>> Alarm to User:'+userx+u'\03{default}')
        for my_msg in userdict[userx]:
            msgcount+=1
            first_part_msg=my_msg.split(u' > ')[0]
            if not first_part_msg in article_list_msg:
                article_list_msg.append(first_part_msg)
                userdict[userx][msgcount]=u"'''"+my_msg.replace(u' > ',u" :'''\n::::**").strip()
            else:
                userdict[userx][msgcount]=my_msg.replace(first_part_msg+u' > ',u'* ').strip()
            pywikibot.output(my_msg)
    user_alarm (userdict,user_article_dict) 
    
if __name__ == '__main__':
        pywikibot.output(u'\03{lightpurple}      *******************************\03{default}')  
        pywikibot.output(u'\03{lightpurple}      *     Code version is '+version+u'    *\03{default}')
        pywikibot.output(u'\03{lightpurple}      *******************************\03{default}') 
        main()