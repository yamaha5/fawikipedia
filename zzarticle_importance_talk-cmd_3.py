# version 3.00
import pywikibot, re,sys
from pywikibot import pagegenerators
import json,codecs,login
import MySQLdb as mysqldb
import time
import urllib.request, urllib.error, urllib.parse,urllib.request,urllib.parse,urllib.error,math
from bs4 import BeautifulSoup
from datetime import timedelta,datetime
faSite = pywikibot.getSite('fa')
enSite=pywikibot.getSite('en')
#pywikibot.config.put_throttle = 0
#pywikibot.put_throttle.setDelay()

def login_wiki():
    try:
        password_wiki = open("/data/project/rezabot/pypywikibot/passfile", 'r')
    except:
        password_wiki = open(pywikibot.config.datafilepath(pywikibot.config.password_file), 'r')
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
    today_date=the_day+' '+the_moth+' '+the_year
    return today_date

def Enmonth (txt):
    if txt=='01':
       return 'ژانویه'
    elif txt=='02':
       return 'فوریه'
    elif txt=='03':
       return 'مارس'
    elif txt=='04':
       return 'آوریل'
    elif txt=='05':
       return 'مه'
    elif txt=='06':
       return 'ژوئن'
    elif txt=='07':
       return 'ژوئیه'
    elif txt=='08':
       return 'اوت'
    elif txt=='09':
       return 'سپتامبر'
    elif txt=='10':
       return 'اکتبر'
    elif txt=='11':
       return 'نوامبر'
    elif txt=='12':
       return 'دسامبر'
    else:
       return ''

def En2Fa_num (txt):
    try:
       txt=str(txt)
    except:
       pass
    count=0
    for i in '۰۱۲۳۴۵۶۷۸۹':
       txt=txt.replace(str(count),i)
       count+=1
    txt=txt.replace(',','،')
    return txt

def data2fa(number):
    data=pywikibot.DataPage(int(number))
    try:
        items=data.get()
    except:
        return ""
    if isinstance(items['links'],list):
        items['links']={}
    if 'fawiki' in items['links']:
        return items['links']['fawiki']['name']
    if 'fa' in items['label']:
        return items['label']['fa']
    try:
        return items['label']['en']
    except:
        return ""

def ClaimFinder(our_Site,page_title,claim_num):
    fa_result=''
    
    page = pywikibot.Page(our_Site,page_title)

    en_wdata = pywikibot.DataPage(page)



    #en_wdata=pywikibot.DataPage()
    try:
        items=en_wdata.get()
        if items['claims']:
            case=items['claims']
            for i in case:
                if i['m'][1]==claim_num:
                    fa_result=data2fa(i['m'][3]['numeric-id'])
                    break
    except:
        return ''
    if fa_result:
        fa_result=fa_result.strip()
    return fa_result

def templatequery(link):
    temps=[]
    if link=='':
        return []    
    link=link.replace(' ','_')
    params = {
            'action': 'query',
            'prop':'templates',
            'titles': link,
            'redirects': 1,
            'tllimit':500,
    }
    try:
        #categoryname = query.GetData(params,faSite)
        categoryname = pywikibot.data.api.Request(site=faSite, **params).submit()
        
        for item in categoryname['query']['pages']:
            templateha=categoryname['query']['pages'][item]['templates']
            break
        for temp in templateha:
            temps.append(temp['title'].replace('_',' '))         
        return temps
    except: 
        return []

def EnDictionary(enlink,firstsite,secondsite):
    try:
        enlink=str(str(enlink),'UTF-8').replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    except:
        enlink=enlink.replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    if enlink.find('#')!=-1:
        return ''
    if enlink=='':
        return ''    
    enlink=enlink.replace(' ','_')
    site = pywikibot.getSite(firstsite)
    sitesecond= pywikibot.getSite(secondsite)
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': enlink,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        #queryresult = query.GetData(params,site)  
        queryresult = pywikibot.data.api.Request(site=site, **params).submit()
        
        for item in queryresult['query']['pages']:
            case=queryresult['query']['pages'][item]['langlinks']
        for item in case:
            if item['lang']==secondsite:
                intersec=item['*']
                break
        result=intersec
        if result.find('#')!=-1:
            return ''
        return result
    except: 
        return ''

def Interwiki_count(link):
    link=link.replace(' ','_')
    params = {
        'action': 'query',
        'prop': 'langlinks',
        'titles': link,
        'redirects': 1,
        'lllimit':500,
    }
    try:
        #queryresult = query.GetData(params,faSite)  
        queryresult = pywikibot.data.api.Request(site=faSite, **params).submit()
        for item in queryresult['query']['pages']:
            case=queryresult['query']['pages'][item]['langlinks']
        return len(case)
    except: 
        return 0

def Page_size(link):
    link=link.replace(' ','_')
    params = {
        'action': 'query',
        'prop': 'info',
        'titles': link,
    }
        
    try:
        #queryresult = query.GetData(params,faSite)  
        queryresult = pywikibot.data.api.Request(site=faSite, **params).submit()
        for item in queryresult['query']['pages']:
            length=queryresult['query']['pages'][item]['length']
            if 'فهرست' in link and length>30000:
                length=30001
            if length>200000:
                length=200000
        return length
    except: 
        return 1

def get_ref_to(link):
    if link=='':
        return 1    
    link=link.replace(' ','_')
    params = {
                'action': 'query',
                'list': 'backlinks',
                'bltitle': link,
                'bllimit':500,
            }
    try:
        #back_link = query.GetData(params,faSite)
        back_link = pywikibot.data.api.Request(site=faSite, **params).submit()
        case_number=back_link['query']['backlinks']
        return  len(case_number)
    except: 
        return 1

def catquery(enlink,firstsite):
    cats=[]
    try:
        enlink=str(str(enlink),'UTF-8').replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    except:
        enlink=enlink.replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    enlink=enlink.split('#')[0].strip()
    if enlink=='':
        return False    
    enlink=enlink.replace(' ','_')
    site = pywikibot.getSite(firstsite)
    params = {
                'action': 'query',
                'prop': 'categories',
                'titles': enlink,
                'redirects': 1,
                'clshow':'!hidden',
                'cllimit':500,
            }
    try:
        #categoryname = query.GetData(params,site)
        categoryname = pywikibot.data.api.Request(site=site, **params).submit()
        for item in categoryname['query']['pages']:
            categoryha=categoryname['query']['pages'][item]['categories']
            break
        for cat in categoryha:
            cats.append(cat['title'])         
        return cats
    except: 
        return []

def get_quality_main(fatitle,page_size,fa_text):
    fa_text=fa_text.replace("{{citation","{{یادکرد").replace("{{Citation","{{یادکرد").replace("<ref name","<ref>").replace("\r","")
    fa_text=fa_text.replace("====","==").replace("===","==").replace("file:","پرونده:").replace("File:","پرونده:").replace("تصویر:","پرونده:")
    templates=templatequery(fatitle)
    totaltemplates=' - '.join(templates)
    totaltemplates=totaltemplates.lower()
    if re.sub(r'\.(tiff|tif|png|gif|jpg|jpeg)[ \n\r]','',fa_text)!=fa_text:
        hasImage=True
    else:
        hasImage=False
    if 'الگو:مقاله برگزیده' in templates and page_size>20001:
        return 'برگزیده','دارای [[الگو:مقاله برگزیده]]'
    elif 'الگو:مقاله خوب' in templates and page_size>20001:
        return 'خوب','دارای [[الگو:مقاله خوب]]'
    elif 'الگو:فهرست برگزیده' in templates and page_size>10001:
        return 'فهرست برگزیده','دارای [[الگو:فهرست برگزیده]]'
    elif fatitle[:6]=='فهرست ':
        return 'فهرست','ابتدای نامش «فهرست» است.'
    elif 'الگو:جعبه ابهام‌زدایی' in templates:
        return 'ابهام‌زدائی','دارای [[الگو:ابهام‌زدائی]]'
    elif page_size<3001:
        return 'خرد','حجم مؤثر کمتر از ۳ کیلوبایت'
    elif page_size>3000 and page_size<7001:
        if (fa_text.count("<ref>")>5 or fa_text.count( "{{یادکرد")>5) and page_size>6001:
            article_alarm="'''استثنا:''' تعداد ارجاع="+str(fa_text.count("<ref>"))+' تعداد یادکرد='+str(fa_text.count("{{یادکرد"))+' حجم='+str(page_size)
            return 'ضعیف',article_alarm
        if fa_text.count("== ")>0:
            return 'ابتدائی','همهٔ [[وپ:مکنآ|شرایط مقالهٔ ابتدائی]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
        else:
            return 'خرد','باوجود حجم بالا زیربخش ندارد.'
    elif page_size>7000 and page_size<15001:
        if (fa_text.count("<ref>")>5 or fa_text.count("{{یادکرد")>5) and fa_text.count("==\n")>2 and fa_text.count("[[رده:")>0 and fa_text.count("]]")-fa_text.count("[[رده:")>5:
            return 'ضعیف','همهٔ [[وپ:مکنآ|شرایط مقالهٔ ضعیف]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
        else:
            article_alarm='تعداد ارجاع='+str(fa_text.count("<ref>"))+' تعداد یادکرد='+str(fa_text.count("{{یادکرد"))+' تعداد بخش‌بندی='+str(fa_text.count("==\n"))+' تعداد رده='+str(fa_text.count("[[رده:"))+' تعداد پیوند='+str(fa_text.count("]]")-fa_text.count("[[رده:"))
            return 'ابتدائی',article_alarm
    elif page_size>15000:
        if 'الگو:Ambox' in templates:
            #pywikibot.output('\03{lightred}It has alarm box!\03{default}')
            return 'ضعیف','باوجود حجم بالا دارای الگوی هشدار در مقاله'
        if 'الگو:درجه' in templates and page_size>17000:
            #pywikibot.output('\03{lightred}It has degree template!\03{default}')
            return 'متوسط','حجم بالای ۱۷ کیلوبایت و دارای الگو:درجه'
        if (fa_text.count("<ref>")>10 or fa_text.count("{{یادکرد")>10) and fa_text.count("==\n")>4 and fa_text.count("[[رده:")>0:
            #pywikibot.output('\03{lightblue}It has 10 refs and more than 5 subsection and more than 1 category!\03{default}')
            if ('الگو:Navbox' in templates or '{{جعبه' in fa_text or 'الگو:Infobox' in templates or 'الگو:داده‌های کتابخانه‌ای' in templates or 'الگو:infobox' in totaltemplates) and ('پرونده:' in fa_text or '<gallery>' in fa_text or hasImage) and fa_text.count("]]")-fa_text.count("[[رده:")>20:
                #pywikibot.output('\03{lightblue}It has box and Image and more than 20 links!\03{default}')
                return 'متوسط','همهٔ [[وپ:مکنآ|شرایط مقالهٔ متوسط]] ویکی‌پروژه نسخهٔ آفلاین را دارد.'
            else:
                if 'الگو:Infobox' in templates:
                    boxnum='True'
                elif 'الگو:infobox' in totaltemplates:
                    boxnum='True'
                elif '{{جعبه' in fa_text:
                    boxnum='True'
                else:
                    boxnum='False'
                article_alarm='ناوباکس='+str('الگو:Navbox' in templates)+' الگو:داده کتابخانه‌ای='+str('الگو:داده‌های کتابخانه‌ای' in templates)+' جعبه اطلاعات='+boxnum+' پرونده ='+str('پرونده:' in fa_text or hasImage)+' نگارخانه='+str('<gallery>' in fa_text)+' پیوند درونی='+str(fa_text.count("]]")-fa_text.count("[[رده:"))
                #pywikibot.output(article_alarm)
                return 'ضعیف',article_alarm
        else:
            article_alarm='تعداد ارجاع='+str(fa_text.count("<ref>"))+'/10 تعداد یادکرد='+str(fa_text.count("{{یادکرد"))+'/10 زیربخش='+str(fa_text.count("==\n"))+'/4 رده='+str(fa_text.count("[[رده:"))+'/1'
            #pywikibot.output(article_alarm)
            return 'ضعیف',article_alarm
    else:
        return 'نامشخص','نامشخص'

def get_quality(fatitle,page_size):
    templates=templatequery(fatitle)
    if 'الگو:مقاله برگزیده' in templates:
        return 500
    elif 'الگو:مقاله خوب' in templates:
        return 500
    elif 'الگو:فهرست برگزیده' in templates:
        return 500
    elif page_size>30000:
        return 400
    elif 'الگو:درجه' in templates and page_size>10000 and page_size<30000:
        return 300
    elif page_size>10000 and page_size<30000:
        return 200
    elif page_size>5000 and page_size<10000:
        return 100
    elif 'الگو:خرد' in templates:
        return 50
    else:
        return 50

def get_importance(fatitle,is_one_2):
    en_topice=''
    topice_list=[]
    EnTitle=EnDictionary(fatitle,'fa','en')
    EnCatList_main=catquery('Talk:'+EnTitle,'en')
    EnCatList='\n'.join(EnCatList_main)
    numi,scores=0,0
    if 'Top-importance' in EnCatList:
        scores=400
        numi+=1
    elif 'High-importance' in EnCatList:
        scores+=300
        numi+=1
    elif 'Mid-importance' in EnCatList:
        scores+=200
        numi+=1
    elif 'Low-importance' in EnCatList:
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
       if '-importance' in encat:
            en_topice=encat.split('-importance')[1].strip()
            en_topice=en_topice.replace('articles','').strip()
            en_topice=EnDictionary(en_topice,'en','fa').strip()
            if en_topice:
                if not en_topice in topice_list:
                    topice_list.append(en_topice)
    if not topice_list:
        for encat in EnCatList_main:
           if '-Class' in encat:
                en_topice=encat.split('-Class')[1].strip()
                en_topice=en_topice.replace('articles','').strip()
                en_topice=EnDictionary(en_topice,'en','fa').strip()
                if en_topice:
                    if not en_topice in topice_list:
                        topice_list.append(en_topice)
    num=0
    topic_txt=' '
    if is_one_2:
        cat_fapage=pywikibot.Page(faSite,'رده:مقاله‌های ویکی‌پروژه نسخه آفلاین درباره '+is_one_2)
        if not cat_fapage.exists():
            cat_fapage.put('{{رده پنهان}}\n[[رده:مقاله‌های ویکی‌پروژه نسخه آفلاین بر پایه موضوع|'+is_one_2+']]','ربات:ساخت رده مورد نیاز ویکی‌پروژه نسخهٔ آفلاین')

    for topic in topice_list:
        num+=1
        topic_txt+='|موضوع جزئی'+En2Fa_num(num)+'='+topic
        cat_fapage=pywikibot.Page(faSite,'رده:مقاله‌های ویکی‌پروژه نسخه آفلاین درباره '+topic)
        if not cat_fapage.exists():
            cat_fapage.put('{{رده پنهان}}\n[[رده:مقاله‌های ویکی‌پروژه نسخه آفلاین بر پایه موضوع|'+topic+']]','ربات:ساخت رده مورد نیاز ویکی‌پروژه نسخهٔ آفلاین')
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
        if sum2==0:
            sum2=1
        return  sum2      
    else:
        return 1

def get_hitcount(fatitle):
    #urlr=u'https://tools.wmflabs.org/pageviews/?project=fa.pywikibot.org&platform=all-access&agent=user&range=latest-30&pages='+fatitle
    last_month=(datetime.now() - timedelta(days=30)).date().isoformat().replace('-','')+'00'
    today=datetime.now().date().isoformat().replace('-','').replace('-','')+'00'
    fatitle=urllib.parse.quote(fatitle.encode('utf-8'))
    urlr='https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/fa.wikipedia/all-access/user/'+fatitle+'/daily/'+last_month+'/'+today
    #if urlr:
    m_counter=[]
    try:
        page = urllib.request.urlopen(urlr)
        soup = BeautifulSoup(page, 'html.parser')
        newDictionary=json.loads(str(soup))
        newDictionary_list=newDictionary["items"]
        for i in newDictionary_list:
            m_counter.append(i['views'])
        return m_counter
    except:
        print('problmeeeeeeeeeeeeeeeem')
        return m_counter

def show_sizeof(x, level=0):

    return "\t" * level, x.__class__, sys.getsizeof(x), x

    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in list(x.items()):
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)

def run(fapage,result):
    fatitle=fapage.title()
    Overall_score=0
    for_print=''
    fa_text,fa_text2='',''
    is_one_2,en_topice='',''
    del fa_text,fa_text2
    try:
       fa_text=fapage.get()
       fa_text=fa_text.replace('\r','')
    except:
       return False,False,False,False,False,False,False
    pagesize1=sys.getsizeof (fa_text)
    fa_text2=re.sub('\{\{(?:\{\{.*?\}\}|[^\}])*\}\}','',fa_text, re.S)
    fa_text2=re.sub('\[\[رده\:.*?\]\]','',fa_text2)
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
        is_one_2='نامعلوم'
        #is_one_2=ClaimFinder(faSite,fatitle,31)
        if not is_one_2:
            is_one_2=ClaimFinder(faSite,fatitle,279)
            if not is_one_2:
                is_one_2=''
        ref_number=get_ref_to(fatitle)
        Interwiki_num=Interwiki_count(fatitle)
        page_sizes=Page_size(fatitle)
        quality_num=get_quality(fatitle,pagesize)
        quality_variable,article_alarm=get_quality_main(fatitle,pagesize,fa_text)
        article_alarm=article_alarm.replace('True','دارد').replace('False','ندارد')
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

        for_put='{{ویکی‌پروژه نسخه آفلاین|امتیاز='+str(Overall_score)+'|درجه اهمیت ویکی‌انگلیسی='+str(int(EnImportance))
        for_put+='|تعداد بازدید='+str(hitcount_result)+'|درجه کیفیت='+quality_variable+'|تاریخ بازدید='+today_date
        for_put+='|توضیح کیفیت='+article_alarm+en_topice+'|موضوع کلی='+is_one_2+'}}\n'
    return for_put,str(Overall_score),quality_variable,str(pagesize),str(main_page_size),str(hitcount_result),str(Interwiki_num),result

def errors(fapage):
    with codecs.open('article_importance_error.txt' ,mode = 'a',encoding = 'utf8' ) as f:
                    f.write(fapage.title()+'\n')
                    
def main(faname,username):
    PageTitles = []
    result={}
    faPages=[pywikibot.Page(faSite,faname)]
    for fapage in faPages:
        if fapage.namespace()!=0:
            result['msg']='ربات فقط در فضای نام اصل (مقاله) کار می کند.'
            print(json.dumps(result))
            continue
        Overall_score,score_num,quality_variable,pagesize,main_page_size,hitcount_result,Interwiki_num,result=run(fapage,result)
        try:
            if not Overall_score:
                fapage=fapage.getRedirectTarget()
                Overall_score,score_num,quality_variable,pagesize,main_page_size,hitcount_result,Interwiki_num,result=run(fapage,result)
        except:
            pass
        if Overall_score:
            bot_msg=score_num+'؛کیفیت='+quality_variable+'؛حجم مؤثر='+pagesize+'؛حجم مقاله='+main_page_size+'؛بازدید='+hitcount_result+'؛میانویکی='+Interwiki_num
            bot_msg='ربات:درجه‌بندی [[وپ:آفلاین|ویکی‌پروژه آفلاین]] ('+username+') > امتیاز='+En2Fa_num(bot_msg)

            Talk_fapage=pywikibot.Page(faSite,'بحث:'+fapage.title())
            try:
                talk_text=Talk_fapage.get()+'\n'
                if Overall_score in talk_text:
                    result['msg']='رتبه‌بندی به‌روز است و نیاز نیست از نو به‌روز شود.'
                    print(json.dumps(result))
                    continue
                if '{{ویکی‌پروژه نسخه آفلاین' in talk_text:
                    talk_text=re.sub(r'\{\{ویکی‌پروژه نسخه آفلاین.*?\}\}\n',Overall_score,talk_text)
                    try:
                       #login_fa()
                       Talk_fapage.put(talk_text.strip(),bot_msg)
                       result['msg']='مقاله ارزشیابی شد. بحث مقاله را بررسی کنید.'
                       print(json.dumps(result))
                       continue
                    except:
                        result['msg']='خطائی رخ داد!۱'
                        print(json.dumps(result))
                        continue

            except pywikibot.IsRedirectPage:
                Talk_fapage=Talk_fapage.getRedirectTarget()
                if Talk_fapage.namespace()!=1:
                    Talk_fapage=pywikibot.Page(faSite,'بحث:'+Talk_fapage.title())
                if not 'بحث:' in Talk_fapage.title():
                    Talk_fapage=pywikibot.Page(faSite,'بحث:'+Talk_fapage.title())
                try:
                    talk_text=Talk_fapage.get()+'\n'
                    if Overall_score in talk_text:
                        result['msg']='رتبه‌بندی به‌روز است و نیاز نیست از نو به‌روز شود.'
                        print(json.dumps(result))
                        continue
                    if '{{ویکی‌پروژه نسخه آفلاین' in talk_text:
                        talk_text=re.sub(r'\{\{ویکی‌پروژه نسخه آفلاین.*?\}\}\n',Overall_score,talk_text)
                        
                        try:
                           #login_fa()
                           Talk_fapage.put(talk_text.strip(),bot_msg)
                           result['msg']='مقاله ارزشیابی شد. بحث مقاله را بررسی کنید.'
                           print(json.dumps(result))
                           continue
                        except:
                            result['msg']='خطائی رخ داد!۲'
                            print(json.dumps(result))
                            continue
                except:
                    result['msg']='خطائی رخ داد!۳'
                    print(json.dumps(result))
                    continue
            except:
                talk_text='\n'

            talk_text=talk_text.replace('\r','')+'\n'
            talk_text=talk_text.replace('{{بصب}}','{{بصب}}\n').replace('{{بصب}}\n\n','{{بصب}}\n')
            talk_text=talk_text.replace('{{رتب}}','{{رتب}}\n').replace('{{رتب}}\n\n','{{رتب}}\n')
            if '{{بصب}}' in talk_text or '{{صفحه بحث}}' in talk_text:
                talk_text=talk_text.replace('{{بصب}}\n','{{بصب}}\n'+Overall_score,1)
                talk_text=talk_text.replace('{{صفحه بحث}}\n','{{صفحه بحث}}\n'+Overall_score,1)
            elif '{{رتب}}' in talk_text or '{{ردکردن تا بحث‌ها}}' in talk_text:
                talk_text=talk_text.replace('{{رتب}}\n','{{رتب}}\n'+Overall_score,1)
                talk_text=talk_text.replace('{{ردکردن تا بحث‌ها}}\n','{{ردکردن تا بحث‌ها}}\n'+Overall_score,1)
            else:
                talk_text='{{رتب}}\n{{بصب}}\n'+Overall_score+talk_text
            
            try:
                #login_fa()
                Talk_fapage.put(talk_text.strip(),bot_msg)
                result['msg']='مقاله ارزشیابی شد. بحث مقاله را بررسی کنید.'
                print(json.dumps(result))
                continue
            except:
                result['msg']='خطائی رخ داد!۴'
                print(json.dumps(result))
                continue
                
faname=sys.argv[1]
username=sys.argv[2]
main(faname.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'),username.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace'))