#!/usr/bin/python
# -*- coding: utf-8 -*-
import catlib ,pagegenerators,sys,query
import wikipedia,urllib,gzip,codecs,re
import MySQLdb as mysqldb
import config,json
line_items,rowi,rowr,text,count=' ',' ',' ',' ',0
language='en'
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
result={}
page_namespace={u'0':u'',u'1':u'Talk:',
                u'2':u'User:',u'3':u'User talk:',
                u'4':u'Wikipedia:',u'5':u'Wikipedia talk:',
                u'6':u':File:',u'7':u'File talk:',#Should has : at the first of NS 6
                u'8':u'Mediawiki:',u'9':u'Mediawiki talk:',
                u'10':u'Template:',u'11':u'Template talk:',
                u'12':u'Help:',u'13':u'Help talk:',
                u'14':u':Category:',u'15':u'Category talk:',#Should has : at the first of NS 14
                u'100':u'Portal:',u'101':u'Portal Talk:',
                u'102':u'Book:',u'103':u'Book talk:',
                u'828':u'Module:',u'829':u'Module talk:'
}
page_namespace2={u'0':u'مقاله',u'1':u'بحث',
                u'2':u'کاربر',u'3':u'بحث کاربر',
                u'4':u'ویکی‌پدیا',u'5':u'بحث ویکی‌پدیا',
                u'6':u'پرونده',u'7':u'بحث پرونده',#Should has : at the first of NS 6
                u'8':u'مدیاویکی',u'9':u'بحث مدیاویکی',
                u'10':u'الگو',u'11':u'بحث الگو',
                u'12':u'راهنما:',u'13':u'بحث راهنما',
                u'14':u'رده',u'15':u'بحث رده',#Should has : at the first of NS 14
                u'100':u'درگاه',u'101':u'بحث درگاه',
                u'102':u'کتاب',u'103':u'بحث کتاب',
                u'118':u'پیش‌نویس',u'119':u'بحث پیش‌نویس',
                u'828':u'پودمان',u'829':u'بحث پودمان'
}
def Persian_Num(text):
    en_num=u'0123456789'
    fa_num=u'۰۱۲۳۴۵۶۷۸۹'
    a=0
    for i in en_num:
        text=text.replace(en_num[a],fa_num[a])
        a+=1
    return text

def endictionry( enlink,first,second):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    if enlink.find('#')!=-1:
        return False
    if enlink==u'':
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = wikipedia.getSite(first)
    sitesecond= wikipedia.getSite(second)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        categoryname = query.GetData(params,site)  
        for item in categoryname[u'query'][u'pages']:
            case=categoryname[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==second:
                intersec=item[u'*']
                break
        result=intersec
        if result.find('#')!=-1:
            return False
        return result
    except: 
        return False

def categorydown(listacategory,level_down):
    listacategory=[listacategory]
    count=1
    for catname in listacategory:
        count+=1
        if count==200:
            break
        gencat = pagegenerators.SubCategoriesPageGenerator(catname, recurse=False)
        for subcat in gencat:
            try:
               wikipedia.output(str(subcat))
            except:    
                wikipedia.output(subcat)
            if subcat in listacategory:
                continue
            else:
                listacategory.append(subcat)
        break
    return listacategory

PageTitle_fa=u'رده:'+unicode(sys.argv[1],'UTF-8')
PageTitle=endictionry(PageTitle_fa,'fa','en')
username=unicode(sys.argv[2],'UTF-8')
username=username.replace(u'کاربر:',u'').replace(u'user:',u'').replace(u'User:',u'')
level_down =1
more_than_3=True

language='en'
wiki = wikipedia.getSite(language)
PageTitle=PageTitle.replace(u'[[',u'').replace(u']]',u'').replace(u' ',u'_').replace(u'Category:',u'').replace(u'category:',u'').strip()

encat = catlib.Category( wiki,PageTitle )
cat_list=categorydown(encat,level_down)
fa_text=u'در زیر مجموعه‌ای از صفحاتی که در ویکی‌پدیای انگلیسی در ردهٔ [[:en:Category:'+PageTitle+u']] موجود است ولی در ویکی‌پدیای فارسی موجود نیستند بر پایه تعداد میان‌ویکی و حجم مقاله فهرست شده‌اند. لطفا در ساخت این صفحات همکاری کنید.'
fa_text+=u'\n\n{{توضیح|تعداد میان‌ویکی، نشان‌دهندهٔ تعداد زبان‌هایی است که مقاله در آن‌ها موجود است.}}'
fa_text+=u'\n\n{{توضیح|حجم صفحه، حجم صفحهٔ مقاله را بر حسب بایت نمایش می‌دهد.}}'
fa_text+=u'\n\n{{توضیح|برای افزودن نام خود به عنوان کاربر سازنده، به جای «نام سازنده»، <code><nowiki>~~~</nowiki></code> را قرار دهید تا نامتان به صورت خودکار جایگزین شود.}}'
fa_text+=u'\n'
page_list=[]
wikipedia.output(u'--------------------------------------')
wikipedia.output(u'Getting query from wikipedia database')
for cat in cat_list:
    wikipedia.output(u'Query > Category:'+cat.title())
    try:
        cat=cat.title().replace(u'[[',u'').replace(u']]',u'').replace(u' ',u'_').replace(u'Category:',u'').strip()
        if '_stubs' in cat:
            continue
        conn = mysqldb.connect(language+"wiki.labsdb", db = wiki.dbName(),
                               user = config.db_username,
                               passwd = config.db_password)
        cursor = conn.cursor()
        cursor.execute('SELECT CONCAT(":",page_namespace,":",page_title,"]]||", count(*),"||",page_len,"||",page_namespace) FROM langlinks JOIN categorylinks ON ll_from = cl_from AND cl_to="'+cat+'"JOIN page on ll_from = page_id   WHERE page_is_redirect = 0 AND NOT EXISTS (SELECT * FROM langlinks as t WHERE t.ll_lang="fa" and t.ll_from = langlinks.ll_from) GROUP BY ll_from   ORDER BY count(*) DESC,page_title;')
        results = cursor.fetchall()
        count=0
        rowr='\n'
        for row in results:
                count+=1
                rowi=unicode(str(row[0]),'UTF-8')
                
                if not rowi in page_list:
                    page_list.append(rowi)
                    if more_than_3:
                       if int(rowi.split(u'||')[1].strip())<1 and len(results)> 30:
                            continue
                    rowr+=u'|'+str(count)+u'||[[:'+language+rowi+u'||\n|-\n'
        if not rowr.strip():
            continue
        catfa=endictionry(u'Category:'+cat,'en','fa')
        if not catfa:
            catfa=u'en:Category:'+cat
        pagetop=u"\n==[[:"+catfa+"]]==\n"
        pagetop+=u'\n{| class="wikitable sortable"\n!رديف!!صفحه!!تعداد میان‌ویکی‌ها!!حجم صفحه!!فضای نام صفحه!!کاربر سازنده\n|-\n'
        pagedown=u'\n|}\n'
        #rowr=Persian_Num(rowr)
        fa_text+=pagetop+rowr.strip()+pagedown
    except:
        continue
adress=u"User:"+username+u"/صفحات مورد نیاز در "+PageTitle_fa
message=u"[[وپ:ابزارک|ابزارهای کاربردی]] > فهرست صفحات ناموجود بر پایه رده (به درخواست [[کاربر:"+username+u']])'
result['msg']=adress
print json.dumps(result)
wiki = wikipedia.getSite('fa')
page = wikipedia.Page(wiki,adress)
for ns in page_namespace:
    fa_text=fa_text.replace(u'[[:en:'+ns+u':',u'[[:en:'+page_namespace[ns])
for ns in page_namespace2:
    fa_text=fa_text.replace(u'||'+ns+u'\n',u'||'+page_namespace2[ns]+u'\n')
page.put(fa_text,message)


