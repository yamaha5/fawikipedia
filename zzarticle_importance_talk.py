# -*- coding: utf-8 -*-
# version 3.00
import wikipedia, re,sys,query,string
import pagegenerators,json,codecs,login
import MySQLdb as mysqldb
import time
import urllib2,urllib,math
from BeautifulSoup import BeautifulSoup
from datetime import timedelta,datetime
faSite = wikipedia.getSite('fa')
enSite=wikipedia.getSite('en')
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()

def login_wiki():
    try:
        password_wiki = open("/data/project/rezabot/pywikipedia/passfile", 'r')
    except:
        password_wiki = open(wikipedia.config.datafilepath(config.password_file), 'r')
    password_wiki=password_wiki.read().replace('"','').strip()    
    passwords=password_wiki.split(',')[1].split(')')[0].strip()
    usernames=password_wiki.split('(')[1].split(',')[0].strip()
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

def find_date():
    today=str(datetime.now()).replace('-','').split(' ')[0].strip()
    the_year=En2Fa_num(today[:4])
    the_moth=Enmonth(today[4:6])
    the_day=En2Fa_num(today[6:9])
    today_date=the_day+u' '+the_moth+u' '+the_year
    return today_date

def Enmonth (txt):
    if txt==u'01':
       return u'ژانویه'
    elif txt==u'02':
       return u'فوریه'
    elif txt==u'03':
       return u'مارس'
    elif txt==u'04':
       return u'آوریل'
    elif txt==u'05':
       return u'مه'
    elif txt==u'06':
       return u'ژوئن'
    elif txt==u'07':
       return u'ژوئیه'
    elif txt==u'08':
       return u'اوت'
    elif txt==u'09':
       return u'سپتامبر'
    elif txt==u'10':
       return u'اکتبر'
    elif txt==u'11':
       return u'نوامبر'
    elif txt==u'12':
       return u'دسامبر'
    else:
       return u''

def En2Fa_num (txt):
    try:
       txt=str(txt)
    except:
       pass
    count=0
    for i in u'۰۱۲۳۴۵۶۷۸۹':
       txt=txt.replace(str(count),i)
       count+=1
    txt=txt.replace(u',',u'،')
    return txt

def data2fa(number):
    data=wikipedia.DataPage(int(number))
    try:
        items=data.get()
    except:
        return ""
    if isinstance(items['links'],list):
        items['links']={}
    if items['links'].has_key('fawiki'):
        return items['links']['fawiki']['name']
    if items['label'].has_key('fa'):
        return items['label']['fa']
    try:
        return items['label']['en']
    except:
        return ""

def ClaimFinder(our_Site,page_title,claim_num):
    fa_result=u''
    en_wdata=wikipedia.DataPage(wikipedia.Page(our_Site,page_title))
    try:
        items=en_wdata.get()
        if items['claims']:
            case=items['claims']
            for i in case:
                if i['m'][1]==claim_num:
                    fa_result=data2fa(i[u'm'][3][u'numeric-id'])
                    break
    except:
        return u''
    if fa_result:
        fa_result=fa_result.strip()
    return fa_result

def templatequery(link):
    temps=[]
    if link==u'':
        return []    
    link=link.replace(u' ',u'_')
    params = {
            'action': 'query',
            'prop':'templates',
            'titles': link,
            'redirects': 1,
            'tllimit':500,
    }
    try:
        categoryname = query.GetData(params,faSite)
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' '))         
        return temps
    except: 
        return []

def EnDictionary(enlink,firstsite,secondsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    if enlink.find('#')!=-1:
        return u''
    if enlink==u'':
        return u''    
    enlink=enlink.replace(u' ',u'_')
    site = wikipedia.getSite(firstsite)
    sitesecond= wikipedia.getSite(secondsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        queryresult = query.GetData(params,site)  
        for item in queryresult[u'query'][u'pages']:
            case=queryresult[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==secondsite:
                intersec=item[u'*']
                break
        result=intersec
        if result.find('#')!=-1:
            return u''
        return result
    except: 
        return u''

def Interwiki_count(link):
    link=link.replace(u' ',u'_')
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': link,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        queryresult = query.GetData(params,faSite)  
        for item in queryresult[u'query'][u'pages']:
            case=queryresult[u'query'][u'pages'][item][u'langlinks']
        return len(case)
    except: 
        return 0

def Page_size(link):
    link=link.replace(u' ',u'_')
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': link,
    }
    try:
        queryresult = query.GetData(params,faSite)  
        for item in queryresult[u'query'][u'pages']:
            length=queryresult[u'query'][u'pages'][item][u'length']
            if u'فهرست' in link and length>30000:
                length=30001
            if length>200000:
                length=200000
        return length
    except: 
        return 1

def get_ref_to(link):
    if link==u'':
        return 1    
    link=link.replace(u' ',u'_')
    params = {
                'action': 'query',
                'list': 'backlinks',
                'bltitle': link,
                'bllimit':500,
            }
    try:
        back_link = query.GetData(params,faSite)
        case_number=back_link[u'query'][u'backlinks']
        return  len(case_number)
    except: 
        return 1

def catquery(enlink,firstsite):
    cats=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    if enlink==u'':
        return False    
    enlink=enlink.replace(u' ',u'_')
    site = wikipedia.getSite(firstsite)
    params = {
                'action': 'query',
                'prop': 'categories',
                'titles': enlink,
                'redirects': 1,
                'clshow':'!hidden',
                'cllimit':500,
            }
    try:
        categoryname = query.GetData(params,site)
        for item in categoryname[u'query'][u'pages']:
            categoryha=categoryname[u'query'][u'pages'][item][u'categories']
            break
        for cat in categoryha:
            cats.append(cat[u'title'])         
        return cats
    except: 
        return []

def get_quality_main(fatitle,page_size,fa_text):
    fa_text=fa_text.replace(u"{{citation",u"{{یادکرد").replace(u"{{Citation",u"{{یادکرد").replace(u"<ref name",u"<ref>").replace(u"\r",u"")
    fa_text=fa_text.replace(u"====",u"==").replace(u"===",u"==").replace(u"file:",u"پرونده:").replace(u"File:",u"پرونده:").replace(u"تصویر:",u"پرونده:")
    templates=templatequery(fatitle)
    totaltemplates=u' - '.join(templates)
    totaltemplates=totaltemplates.lower()
    if re.sub(ur'\.(tiff|tif|png|gif|jpg|jpeg)[ \n\r]','',fa_text)!=fa_text:
        hasImage=True
    else:
        hasImage=False
    if u'الگو:مقاله برگزیده' in templates and page_size>20001:
        return u'برگزیده',u'دارای [[الگو:مقاله برگزیده]]'
    elif u'الگو:مقاله خوب' in templates and page_size>20001:
        return u'خوب',u'دارای [[الگو:مقاله خوب]]'
    elif u'الگو:فهرست برگزیده' in templates and page_size>10001:
        return u'فهرست برگزیده',u'دارای [[الگو:فهرست برگزیده]]'
    elif fatitle[:6]==u'فهرست ':
        return u'فهرست',u'ابتدای نامش «فهرست» است.'
    elif u'الگو:جعبه ابهام‌زدایی' in templates:
        return u'ابهام‌زدائی',u'دارای [[الگو:ابهام‌زدائی]]'
    elif page_size<3001:
        return u'خرد',u'حجم مؤثر کمتر از ۳ کیلوبایت'
    elif page_size>3000 and page_size<7001:
        if (string.count(fa_text,u"<ref>")>5 or string.count( fa_text,u"{{یادکرد")>5) and page_size>6001:
            article_alarm=u"'''استثنا:''' تعداد ارجاع="+str(string.count(fa_text,u"<ref>"))+u' تعداد یادکرد='+str(string.count( fa_text,u"{{یادکرد"))+u' حجم='+str(page_size)
            return u'ضعیف',article_alarm
        if string.count(fa_text,"== ")>0:
            return u'ابتدائی',u'همهٔ [[وپ:مکنآ|شرایط مقالهٔ ابتدائی]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
        else:
            return u'خرد',u'باوجود حجم بالا زیربخش ندارد.'
    elif page_size>7000 and page_size<15001:
        if (string.count(fa_text,u"<ref>")>5 or string.count( fa_text,u"{{یادکرد")>5) and string.count(fa_text,"==\n")>2 and string.count(fa_text,u"[[رده:")>0 and string.count(fa_text,"]]")-string.count(fa_text,u"[[رده:")>5:
            return u'ضعیف',u'همهٔ [[وپ:مکنآ|شرایط مقالهٔ ضعیف]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
        else:
            article_alarm=u'تعداد ارجاع='+str(string.count(fa_text,u"<ref>"))+u' تعداد یادکرد='+str(string.count( fa_text,u"{{یادکرد"))+u' تعداد بخش‌بندی='+str(string.count(fa_text,"==\n"))+u' تعداد رده='+str(string.count(fa_text,u"[[رده:"))+u' تعداد پیوند='+str(string.count(fa_text,"]]")-string.count(fa_text,u"[[رده:"))
            return u'ابتدائی',article_alarm
    elif page_size>15000:
        if u'الگو:Ambox' in templates:
            wikipedia.output(u'\03{lightred}It has alarm box!\03{default}')
            return u'ضعیف',u'باوجود حجم بالا دارای الگوی هشدار در مقاله'
        if u'الگو:درجه' in templates and page_size>17000:
            wikipedia.output(u'\03{lightred}It has degree template!\03{default}')
            return u'متوسط',u'حجم بالای ۱۷ کیلوبایت و دارای الگو:درجه'
        if (string.count(fa_text,u"<ref>")>10 or string.count( fa_text,u"{{یادکرد")>10) and string.count(fa_text,u"==\n")>4 and string.count(fa_text,u"[[رده:")>0:
            wikipedia.output(u'\03{lightblue}It has 10 refs and more than 5 subsection and more than 1 category!\03{default}')
            if (u'الگو:Navbox' in templates or u'{{جعبه' in fa_text or u'الگو:Infobox' in templates or u'الگو:داده‌های کتابخانه‌ای' in templates or u'الگو:infobox' in totaltemplates) and (u'پرونده:' in fa_text or u'<gallery>' in fa_text or hasImage) and string.count(fa_text,u"]]")-string.count(fa_text,u"[[رده:")>20:
                wikipedia.output(u'\03{lightblue}It has box and Image and more than 20 links!\03{default}')
                return u'متوسط',u'همهٔ [[وپ:مکنآ|شرایط مقالهٔ متوسط]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
            else:
                if u'الگو:Infobox' in templates:
                    boxnum=u'True'
                elif u'الگو:infobox' in totaltemplates:
                    boxnum=u'True'
                elif u'{{جعبه' in fa_text:
                    boxnum=u'True'
                else:
                    boxnum=u'False'
                article_alarm=u'ناوباکس='+str(u'الگو:Navbox' in templates)+u' الگو:داده کتابخانه‌ای='+str(u'الگو:داده‌های کتابخانه‌ای' in templates)+u' جعبه اطلاعات='+boxnum+u' پرونده ='+str(u'پرونده:' in fa_text or hasImage)+u' نگارخانه='+str(u'<gallery>' in fa_text)+u' پیوند درونی='+str(string.count(fa_text,u"]]")-string.count(fa_text,u"[[رده:"))
                wikipedia.output(article_alarm)
                return u'ضعیف',article_alarm
        else:
            article_alarm=u'تعداد ارجاع='+str(string.count(fa_text,u"<ref>"))+u'/10 تعداد یادکرد='+str(string.count( fa_text,u"{{یادکرد"))+u'/10 زیربخش='+str(string.count(fa_text,u"==\n"))+u'/4 رده='+str(string.count(fa_text,u"[[رده:"))+u'/1'
            wikipedia.output(article_alarm)
            return u'ضعیف',article_alarm
    else:
        return u'نامشخص',u'نامشخص'

def get_quality(fatitle,page_size):
    templates=templatequery(fatitle)
    if u'الگو:مقاله برگزیده' in templates:
        return 500
    elif u'الگو:مقاله خوب' in templates:
        return 500
    elif u'الگو:فهرست برگزیده' in templates:
        return 500
    elif page_size>30000:
        return 400
    elif u'الگو:درجه' in templates and page_size>10000 and page_size<30000:
        return 300
    elif page_size>10000 and page_size<30000:
        return 200
    elif page_size>5000 and page_size<10000:
        return 100
    elif u'الگو:خرد' in templates:
        return 50
    else:
        return 50

def get_importance(fatitle,is_one_2):
    en_topice=u''
    topice_list=[]
    EnTitle=EnDictionary(fatitle,'fa','en')
    EnCatList_main=catquery(u'Talk:'+EnTitle,'en')
    EnCatList=u'\n'.join(EnCatList_main)
    numi,scores=0,0
    if u'Top-importance' in EnCatList:
        scores=400
        numi+=1
    elif u'High-importance' in EnCatList:
        scores+=300
        numi+=1
    elif u'Mid-importance' in EnCatList:
        scores+=200
        numi+=1
    elif u'Low-importance' in EnCatList:
        scores+=100
        numi+=1
    else:
        pass
    if numi==0:
       numi=1
    scores=scores/numi
    if scores<100:
       scores=100
    for encat in EnCatList_main:
       if u'-importance' in encat:
            en_topice=encat.split(u'-importance')[1].strip()
            en_topice=en_topice.replace(u'articles',u'').strip()
            en_topice=EnDictionary(en_topice,'en','fa').strip()
            if en_topice:
                if not en_topice in topice_list:
                    topice_list.append(en_topice)
    if not topice_list:
        for encat in EnCatList_main:
           if u'-Class' in encat:
                en_topice=encat.split(u'-Class')[1].strip()
                en_topice=en_topice.replace(u'articles',u'').strip()
                en_topice=EnDictionary(en_topice,'en','fa').strip()
                if en_topice:
                    if not en_topice in topice_list:
                        topice_list.append(en_topice)
    num=0
    topic_txt=u' '
    if is_one_2:
        cat_fapage=wikipedia.Page(faSite,u'رده:مقاله‌های ویکی‌پروژه نسخه آفلاین درباره '+is_one_2)
        if not cat_fapage.exists():
            cat_fapage.put(u'{{رده پنهان}}\n[[رده:مقاله‌های ویکی‌پروژه نسخه آفلاین بر پایه موضوع|'+is_one_2+u']]',u'ربات:ساخت رده مورد نیاز ویکی‌پروژه نسخهٔ آفلاین')

    for topic in topice_list:
        num+=1
        topic_txt+=u'|موضوع جزئی'+En2Fa_num(num)+u'='+topic
        cat_fapage=wikipedia.Page(faSite,u'رده:مقاله‌های ویکی‌پروژه نسخه آفلاین درباره '+topic)
        if not cat_fapage.exists():
            cat_fapage.put(u'{{رده پنهان}}\n[[رده:مقاله‌های ویکی‌پروژه نسخه آفلاین بر پایه موضوع|'+topic+u']]',u'ربات:ساخت رده مورد نیاز ویکی‌پروژه نسخهٔ آفلاین')
        if num>6:
           break

    return scores,topic_txt.strip()

def compile_hits(hitcount_result):
    sum1,sum2,max,min=0,0,0,100000000000
    numbers=len(hitcount_result)
    num_list=[]
    if hitcount_result:
        for my_num in hitcount_result:
            num_list.append(my_num)
            sum1+=my_num
            if my_num>max:
                max=my_num
                continue
            if my_num<min:
                min=my_num
        num_list.sort()
        avrage=sum1/numbers
        try:
            bottom= int(0.2*numbers)
        except:
            bottom= (0.2*numbers)
        try:
            top= int(0.8*numbers)
        except:
            top= (0.8*numbers)
        for my_num in range(bottom,top):
            sum2+=num_list[my_num]
        return  sum2      
    else:
        return 1

def get_hitcount(fatitle):
    #urlr=u'https://tools.wmflabs.org/pageviews/?project=fa.wikipedia.org&platform=all-access&agent=user&range=latest-30&pages='+fatitle
    last_month=(datetime.now() - timedelta(days=30)).date().isoformat().replace('-','')+'00'
    today=datetime.now().date().isoformat().replace('-','').replace('-','')+'00'
    fatitle=urllib.quote(fatitle.encode('utf-8'))
    urlr=u'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/fa.wikipedia/all-access/user/'+fatitle+'/daily/'+last_month+'/'+today
    #if urlr:
    m_counter=[]
    try:
        page = urllib2.urlopen(urlr)
        soup = BeautifulSoup(page)
        newDictionary=json.loads(str(soup))
        newDictionary_list=newDictionary["items"]

        for i in newDictionary_list:
            m_counter.append(i['views'])
        return m_counter
    except:
        print 'problmeeeeeeeeeeeeeeeem'
        return m_counter

def show_sizeof(x, level=0):

    return "\t" * level, x.__class__, sys.getsizeof(x), x

    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in x.items():
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)

def run(fapage):
    fatitle=fapage.title()
    Overall_score=0
    for_print=u''
    fa_text,fa_text2=u'',u''
    is_one_2,en_topice=u'',u''
    del fa_text,fa_text2
    try:
       fa_text=fapage.get()
       fa_text=fa_text.replace(u'\r',u'')
    except:
       return False,False,False,False,False,False,False
    pagesize1=sys.getsizeof (fa_text)
    fa_text2=re.sub(u'\{\{(?:\{\{.*?\}\}|[^\}])*\}\}',u'',fa_text, re.S)
    fa_text2=re.sub(u'\[\[رده\:.*?\]\]',u'',fa_text2)
    pagesize2=sys.getsizeof (fa_text2)
    main_page_size=Page_size(fatitle)
    rasio=(float(pagesize1-pagesize2)/float(pagesize1))
    if rasio>0.4:
        if rasio*main_page_size>900:
            pagesize=int(main_page_size*(float(pagesize2)/float(pagesize1)))+900
        else:
            pagesize=int(main_page_size*(float(pagesize2)/float(pagesize1)))
    else:
       pagesize=main_page_size
    if fatitle:
        is_one_2=ClaimFinder(faSite,fatitle,31)
        if not is_one_2:
            is_one_2=ClaimFinder(faSite,fatitle,279)
            if not is_one_2:
                is_one_2=u''
        ref_number=get_ref_to(fatitle)
        Interwiki_num=Interwiki_count(fatitle)
        page_sizes=Page_size(fatitle)
        quality_num=get_quality(fatitle,pagesize)
        quality_variable,article_alarm=get_quality_main(fatitle,pagesize,fa_text)
        article_alarm=article_alarm.replace(u'True',u'دارد').replace(u'False',u'ندارد')
        article_alarm=En2Fa_num(article_alarm)
        hitcount_result=get_hitcount(fatitle)
        hitcount_result=compile_hits(hitcount_result)
        EnImportance,en_topice=get_importance(fatitle,is_one_2)
        today_date=find_date()
        if not hitcount_result:
            hitcount_result=1
        if not ref_number:
            ref_number=1
        if not Interwiki_num:
            Interwiki_num2=1
            Interwiki_num=0
        else:
            Interwiki_num2=Interwiki_num
        Importance_score=120 * math.log10(hitcount_result) + 20 * math.log10(ref_number) + 150 * math.log10(Interwiki_num2)+ 100*math.log10(pagesize)
        if EnImportance>0:
            Importance_score=Importance_score+EnImportance*0.8
        else:
            Importance_score=Importance_score*1.33333
        Overall_score = Importance_score + quality_num
        try:
           Overall_score=int(Overall_score)
        except:
           Overall_score=Overall_score

        for_put=u'{{ویکی‌پروژه نسخه آفلاین|امتیاز='+str(Overall_score)+u'|درجه اهمیت ویکی‌انگلیسی='+str(EnImportance)
        for_put+=u'|تعداد بازدید='+str(hitcount_result)+u'|درجه کیفیت='+quality_variable+u'|تاریخ بازدید='+today_date
        for_put+=u'|توضیح کیفیت='+article_alarm+en_topice+u'|موضوع کلی='+is_one_2+u'}}\n'
    return for_put,str(Overall_score),quality_variable,str(pagesize),str(main_page_size),str(hitcount_result),str(Interwiki_num)

def errors(fapage):
    with codecs.open(u'article_importance_error.txt' ,mode = 'a',encoding = 'utf8' ) as f:
                    f.write(fapage.title()+u'\n')
def main():
    login_wiki()
    PageTitles = []
    gen=None
    genFactory = pagegenerators.GeneratorFactory()
    for arg in wikipedia.handleArgs():
        if arg.startswith( '-page' ):
            if len( arg ) == 5:
                PageTitles.append( wikipedia.input( u'Which page do you want to chage?' ) )    
            else:
                PageTitles.append( arg[6:] )
            break
        else:
            generator = genFactory.handleArg( arg )
            if generator:
                gen = generator
    if PageTitles:
        pages = [wikipedia.Page(faSite,PageTitle ) for PageTitle in PageTitles]
        gen = iter( pages )
    preloadingGen = pagegenerators.PreloadingGenerator( gen,pageNumber = 60)
    for fapage in preloadingGen:
        if fapage.namespace()==1:
            fapage=wikipedia.Page(faSite,fapage.title().replace(u'بحث:',u''))
        wikipedia.output(u'------------'+fapage.title()+u'------------')
        if fapage.namespace()!=0:
            wikipedia.output(u'\03{lightred}Bot only works on article namespace! so it is passed!\03{default}')
            continue
        try:
            Overall_score,score_num,quality_variable,pagesize,main_page_size,hitcount_result,Interwiki_num=run(fapage)
        except:
            continue
        try:
            if not Overall_score:
                fapage=fapage.getRedirectTarget()
                Overall_score,score_num,quality_variable,pagesize,main_page_size,hitcount_result,Interwiki_num=run(fapage)
        except:
            pass
        if Overall_score:
            bot_msg=u'ربات:درجه‌بندی [[وپ:آفلاین|ویکی‌پروژه آفلاین]]> امتیاز='+score_num+u'؛کیفیت='+quality_variable+u'؛حجم مؤثر='+pagesize+u'؛حجم مقاله='+main_page_size+u'؛بازدید='+hitcount_result+u'؛میانویکی='+Interwiki_num
            bot_msg=En2Fa_num(bot_msg)
            Talk_fapage=wikipedia.Page(faSite,u'بحث:'+fapage.title())
            try:
                talk_text=Talk_fapage.get()+u'\n'
                if Overall_score in talk_text:
                    continue
                if u'{{ویکی‌پروژه نسخه آفلاین' in talk_text:
                    talk_text=re.sub(ur'\{\{ویکی‌پروژه نسخه آفلاین.*?\}\}\n',Overall_score,talk_text)
                    wikipedia.output(u'\03{lightgreen}The template is replaced\03{default}')
                    try:
                       wikipedia.output(u'\03{lightgreen}+'+Overall_score+u'\03{default}')
                       Talk_fapage.put(talk_text.strip(),bot_msg)
                       continue
                    except:
                        errors(fapage)
                        wikipedia.output(u'\03{lightred}An error happened so it will be pass!\03{default}')
                        continue

            except wikipedia.IsRedirectPage:
                wikipedia.output(u"\03{lightyellow}The page %s is a redirect, going to get target page.\03{default}" % fapage.title())    
                Talk_fapage=Talk_fapage.getRedirectTarget()
                if Talk_fapage.namespace()!=1:
                    Talk_fapage=wikipedia.Page(faSite,u'بحث:'+Talk_fapage.title())
                if not 'بحث:' in Talk_fapage.title():
                    Talk_fapage=wikipedia.Page(faSite,u'بحث:'+Talk_fapage.title())
                try:
                    talk_text=Talk_fapage.get()+u'\n'
                    if Overall_score in talk_text:
                        continue
                    if u'{{ویکی‌پروژه نسخه آفلاین' in talk_text:
                        talk_text=re.sub(ur'\{\{ویکی‌پروژه نسخه آفلاین.*?\}\}\n',Overall_score,talk_text)
                        wikipedia.output(u'\03{lightgreen}The template is replaced\03{default}')
                        try:
                           wikipedia.output(u'\03{lightgreen}+'+Overall_score+u'\03{default}')
                           Talk_fapage.put(talk_text.strip(),bot_msg)
                           continue
                        except:
                            errors(fapage)
                            wikipedia.output(u'\03{lightred}An error happened so it will be pass!\03{default}')
                            continue
                except:
                    wikipedia.output(u"\03{lightblue}The page %s doesn't exist, skip!\03{default}" % Talk_fapage.title())
                    errors(Talk_fapage)
                    continue
            except:
                talk_text=u'\n'

            talk_text=talk_text.replace(u'\r',u'')+u'\n'
            talk_text=talk_text.replace(u'{{بصب}}',u'{{بصب}}\n').replace(u'{{بصب}}\n\n',u'{{بصب}}\n')
            talk_text=talk_text.replace(u'{{رتب}}',u'{{رتب}}\n').replace(u'{{رتب}}\n\n',u'{{رتب}}\n')

            if u'{{بصب}}' in talk_text or u'{{صفحه بحث}}' in talk_text:
                talk_text=talk_text.replace(u'{{بصب}}\n',u'{{بصب}}\n'+Overall_score,1)
                talk_text=talk_text.replace(u'{{صفحه بحث}}\n',u'{{صفحه بحث}}\n'+Overall_score,1)
            elif u'{{رتب}}' in talk_text or u'{{ردکردن تا بحث‌ها}}' in talk_text:
                talk_text=talk_text.replace(u'{{رتب}}\n',u'{{رتب}}\n'+Overall_score,1)
                talk_text=talk_text.replace(u'{{ردکردن تا بحث‌ها}}\n',u'{{ردکردن تا بحث‌ها}}\n'+Overall_score,1)
            else:
                talk_text=u'{{رتب}}\n{{بصب}}\n'+Overall_score+talk_text

            try:
               wikipedia.output(u'\03{lightgreen}+'+Overall_score+u'\03{default}')
               Talk_fapage.put(talk_text.strip(),bot_msg)
               continue
            except:
                errors(fapage)
                wikipedia.output(u'\03{lightred}An error happened so it will be pass!\03{default}')

if __name__ == '__main__':
        main()