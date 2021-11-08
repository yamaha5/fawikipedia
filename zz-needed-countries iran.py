#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza (User:yamaha5) , 2016
#
# Distributed under the terms of MIT License (MIT)
#coding:utf8
import requests,codecs,urllib,urllib2,BeautifulSoup
import pywikibot,re,string,json
faSite = pywikibot.Site('fa')
enSite= pywikibot.Site('en')
#u"Q30":u"ایالات متحده آمریکا",u"Q159":u"روسیه",u"Q183":u"آلمان",u"Q142":u"فرانسه"
Qery_list={"Q40":u"اتریش","Q115":u"اتیوپی","Q810":u"اردن","Q399":u"ارمنستان","Q77":u"اروگوئه","Q986":u"اریتره","Q265":u"ازبکستان",
        "Q29":u"اسپانیا","Q408":u"استرالیا","Q191":u"استونی","Q801":u"اسرائیل","Q214":u"اسلواکی","Q215":u"اسلوونی","Q889":u"افغانستان",
        "Q736":u"اکوادور","Q262":u"الجزایر","Q792":u"السالوادور","Q878":u"امارات متحده عربی","Q252":u"اندونزی","Q212":u"اوکراین","Q1036":u"اوگاندا",
        "Q702":u"ایالات فدرال میکرونزی","Q30":u"ایالات متحده آمریکا","Q38":u"ایتالیا","Q794":u"ایران","Q27":u"ایرلند","Q189":u"ایسلند","Q23334":u"آبخاز",
        "Q414":u"آرژانتین","Q258":u"آفریقای جنوبی","Q222":u"آلبانی","Q183":u"آلمان","Q781":u"آنتیگوا و باربودا","Q228":u"آندورا","Q916":u"آنگولا",
        "Q244":u"باربادوس","Q778":u"باهاما","Q398":u"بحرین","Q155":u"برزیل","Q921":u"برونئی","Q145":u"بریتانیا","Q184":u"بلاروس","Q31":u"بلژیک",
        "Q219":u"بلغارستان","Q242":u"بلیز","Q902":u"بنگلادش","Q962":u"بنین","Q917":u"بوتان (کشور)","Q963":u"بوتسوانا","Q965":u"بورکینافاسو","Q967":u"بوروندی",
        "Q225":u"بوسنی و هرزگوین","Q750":u"بولیوی","Q691":u"پاپوآ گینه نو","Q917":u"پادشاهی بوتان","Q29999":u"پادشاهی هلند","Q733":u"پاراگوئه","Q843":u"پاکستان",
        "Q695":u"پالائو","Q804":u"پاناما","Q45":u"پرتغال","Q419":u"پرو","Q863":u"تاجیکستان","Q924":u"تانزانیا","Q869":u"تایلند","Q865":u"تایوان","Q907112":u"ترانس‌نیستریا",
        "Q874":u"ترکمنستان","Q43":u"ترکیه","Q754":u"ترینیداد و توباگو","Q945":u"توگو","Q948":u"تونس","Q678":u"تونگا","Q672":u"تووالو","Q574":u"تیمور شرقی","Q766":u"جامائیکا",
        "Q785":u"جرزی","Q685":u"جزایر سلیمان","Q26988":u"جزایر کوک","Q709":u"جزایر مارشال","Q9676":u"جزیره من","Q227":u"جمهوری آذربایجان","Q929":u"جمهوری آفریقای مرکزی",
        "Q23681":u"جمهوری ترک قبرس شمالی","Q213":u"جمهوری چک","Q148":u"جمهوری خلق چین","Q40362":u"جمهوری دموکراتیک عربی صحرا","Q974":u"جمهوری دموکراتیک کنگو",
        "Q786":u"جمهوری دومینیکن","Q971":u"جمهوری کنگو","Q221":u"جمهوری مقدونیه","Q977":u"جیبوتی","Q657":u"چاد","Q35":u"دانمارک","Q219060":u"دولت فلسطین",
        "Q784":u"دومینیکا","Q1037":u"رواندا","Q159":u"روسیه","Q218":u"رومانی","Q953":u"زامبیا","Q954":u"زیمبابوه","Q17":u"ژاپن","Q1008":u"ساحل عاج","Q683":u"ساموآ",
        "Q238":u"سان مارینو","Q1039":u"سائوتومه و پرنسیپ","Q1039":u"سائوتومه و پرینسیپ","Q854":u"سری‌لانکا","Q238":u"سن مارینو","Q763":u"سنت کیتس و نویس",
        "Q760":u"سنت لوسیا","Q757":u"سنت وینسنت و گرنادین‌ها","Q334":u"سنگاپور","Q1041":u"سنگال","Q1050":u"سوازیلند","Q1049":u"سودان","Q958":u"سودان جنوبی",
        "Q730":u"سورینام","Q858":u"سوریه","Q1045":u"سومالی","Q34":u"سوئد","Q39":u"سوئیس","Q1044":u"سیرالئون","Q1042":u"سیشل","Q298":u"شیلی","Q6250":u"صحرای غربی",
        "Q403":u"صربستان","Q796":u"عراق","Q851":u"عربستان سعودی","Q842":u"عمان","Q117":u"غنا","Q142":u"فرانسه","Q33":u"فنلاند","Q712":u"فیجی","Q928":u"فیلیپین",
        "Q229":u"قبرس","Q813":u"قرقیزستان","Q232":u"قزاقستان","Q846":u"قطر","Q1011":u"کاپ ورد","Q800":u"کاستاریکا","Q424":u"کامبوج","Q1009":u"کامرون","Q16":u"کانادا",
        "Q884":u"کره جنوبی","Q423":u"کره شمالی","Q224":u"کرواسی","Q739":u"کلمبیا","Q114":u"کنیا","Q485231":u"کنیبال کورپس","Q241":u"کوبا","Q1246":u"کوزوو","Q970":u"کومور",
        "Q817":u"کویت","Q1011":u"کیپ ورد","Q710":u"کیریباتی","Q1000":u"گابن","Q1005":u"گامبیا","Q734":u"گایان","Q230":u"گرجستان","Q769":u"گرنادا","Q25230":u"گرنزی","Q774":u"گواتمالا",
        "Q734":u"گویان","Q1006":u"گینه","Q983":u"گینه استوایی","Q1007":u"گینه بیسائو","Q819":u"لائوس","Q822":u"لبنان","Q211":u"لتونی","Q1013":u"لسوتو","Q36":u"لهستان","Q32":u"لوکزامبورگ",
        "Q1014":u"لیبریا","Q1016":u"لیبی","Q37":u"لیتوانی","Q347":u"لیختن‌اشتاین","Q1019":u"ماداگاسکار","Q1020":u"مالاوی","Q233":u"مالت","Q826":u"مالدیو","Q833":u"مالزی","Q912":u"مالی",
        "Q28":u"مجارستان","Q970":u"مجمع‌الجزایر قمر","Q1028":u"مراکش","Q79":u"مصر","Q711":u"مغولستان","Q96":u"مکزیک","Q1025":u"موریتانی","Q1027":u"موریس","Q1029":u"موزامبیک",
        "Q217":u"مولداوی","Q235":u"موناکو","Q236":u"مونته‌نگرو","Q836":u"میانمار","Q702":u"میکرونزی","Q1030":u"نامیبیا","Q697":u"نائورو","Q837":u"نپال","Q20":u"نروژ","Q1032":u"نیجر",
        "Q1033":u"نیجریه","Q811":u"نیکاراگوئه","Q664":u"نیوزیلند","Q34020":u"نیووی","Q790":u"هائیتی","Q55":u"هلند","Q668":u"هند","Q783":u"هندوراس","Q237":u"واتیکان","Q686":u"وانواتو",
        "Q25":u"ولز","Q717":u"ونزوئلا","Q881":u"ویتنام","Q805":u"یمن","Q41":u"یونان"}
Qery_list={u"Q794":u"ایران"}
#Qery_list={u"Q30":u"ایالات متحده آمریکا"}
#Qery_list={u"Q16":u"کانادا"}


arabic_country=[u"اردن",u"اریتره",u"ازواد",u"اسرائیل",u"الجزایر",u"امارات متحده عربی",u"بحرین",u"تونس"
                ,u"جیبوتی",u"داعش",u"سودان",u"سوریه",u"سومالی‌لند",u"سومالی",u"صحرای غربی",u"عراق",u"عربستان سعودی"
                ,u"عمان",u"فلسطین",u"قطر",u"لبنان",u"لیبی",u"مراکش",u"مصر",u"موریتانی",u"پانتلند",u"چاد"
                ,u"کردستان سوریه",u"کورماکیتیس",u"کومور",u"کویت",u"یمن"]

def getArabic(title,Country):
    arsite = pywikibot.Site('ar', 'wikipedia')
    ensite = pywikibot.Site('en', 'wikipedia')
    params = {
        'action': 'query',
        'redirects': '',
        'titles': title
    }
    query_res = pywikibot.data.api.Request(site=ensite, **params).submit()


    normalizeds = query_res['query'].get('normalized', [])
    if len(normalizeds):
        title = normalizeds[0]['to']
        
    redirects = query_res['query'].get('redirects', [])
    if len(redirects):
        title = redirects[0]['to']


    wikidata = pywikibot.Site('wikidata', 'wikidata')
    
    endbName = ensite.dbName()
    fadbName = arsite.dbName()
    params = {
        'action': 'wbgetentities',
        'sites': endbName,
        'titles': title,
        'props': 'sitelinks'
    }

    try:
        query_res = pywikibot.data.api.Request(site=wikidata, **params).submit()
    except:
        return ''

    matches_titles = {}
    entities = query_res.get('entities', {})
    for qid, entity in entities.items():
        if fadbName in entity.get('sitelinks', {}):
            ar_title = entity['sitelinks'][fadbName]

            # for not updated since addition of badges on Wikidata items
            if not isinstance(title, str):
                ar_title = ar_title['title']
            return ar_title.replace(u'ي',u'ی').replace(u'ك',u'ک').replace(u'ة',u'ه').replace(u'(مدینه)',u'('+Country+u')').replace(u'(عمران)',u'('+Country+u')')

    return ''


def get_query(Qadress,Country,parts):
    text,text2=u'\n',u'\n'
    #u"Q805":u"یمن"
    
    #myurl=u"https://query.wikidata.org/sparql?format=json&query=SELECT%20?item%20?enarticle%20(COUNT(DISTINCT%20?sitelink)%20AS%20?linkcount)%20?itemLabel%20WHERE%20{%20?item%20wdt:P31/wdt:P279%2a%20wd:Q486972%20.%20?sitelink%20schema:about%20?item%20.%20?item%20wdt:P17%20wd:"+Qadress+"%20.%20optional%20{%20?enarticle%20schema:about%20?item%20;%20schema:isPartOf%20%3Chttps://en.wikipedia.org/%3E%20.}%20minus%20{%20?article%20schema:about%20?item%20.%20?article%20schema:inLanguage%20%22fa%22%20.%20?article%20schema:isPartOf%20%3Chttps://fa.wikipedia.org/%3E%20}%20SERVICE%20wikibase:label%20{%20bd:serviceParam%20wikibase:language%20%22en,fa%22%20.%20}%20}%20GROUP%20BY%20?item%20?itemLabel%20?enarticle%20ORDER%20BY%20DESC(?linkcount)"
    if Country==u'ژاپن':
        if parts==u'city':
            cityType=u'Q137773'
        elif parts==u'bakhsh':
            cityType=u'Q1122846'
        else:
            pass
    elif Country==u"جمهوری خلق چین":
        cityType=u'Q1500350'
    elif Country==u"هند":
        cityType=u'Q486972'
    elif Country==u"شیلی":
        cityType=u'Q1840161'
    else:
        cityType=u'Q486972'
    myurl=u"https://query.wikidata.org/sparql?format=json&query=SELECT%20?item%20?enarticle%20(COUNT(DISTINCT%20?sitelink)%20AS%20?linkcount)%20?itemLabel%20WHERE%20{%20?item%20wdt:P31/wdt:P279%2a%20wd:"+cityType+"%20.%20?sitelink%20schema:about%20?item%20.%20?item%20wdt:P17%20wd:"+Qadress+"%20.%20optional%20{%20?enarticle%20schema:about%20?item%20;%20schema:isPartOf%20%3Chttps://en.wikipedia.org/%3E%20.}%20minus%20{%20?article%20schema:about%20?item%20.%20?article%20schema:inLanguage%20%22fa%22%20.%20?article%20schema:isPartOf%20%3Chttps://fa.wikipedia.org/%3E%20}%20SERVICE%20wikibase:label%20{%20bd:serviceParam%20wikibase:language%20%22en,fa%22%20.%20}%20}%20GROUP%20BY%20?item%20?itemLabel%20?enarticle%20ORDER%20BY%20DESC(?linkcount%29%0Alimit%202000"
    myurl=u'https://query.wikidata.org/sparql?format=json&query=PREFIX%20schema%3A%20%3Chttp%3A%2F%2Fschema.org%2F%3E%0A%0ASELECT%20%3Fitem%20%3Fenarticle%20%3Flinkcount%20%3FitemLabel%20WHERE%20%7B%0A%20%20%7B%0A%20%20%20%20SELECT%20%3Fitem%20%3Fenarticle%20(COUNT(DISTINCT%20%3Fsitelink)%20AS%20%3Flinkcount)%20WHERE%20%7B%0A%20%20%20%20%20%20%3Fitem%20(wdt%3AP31%2Fwdt%3AP279)%20wd%3A'+cityType+'.%0A%20%20%20%20%20%20%3Fsitelink%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%20%20%3Fitem%20wdt%3AP17%20wd%3A'+Qadress+'.%0A%20%20%20%20%20%20OPTIONAL%20%7B%0A%20%20%20%20%20%20%20%20%3Fenarticle%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%20%20%20%20%3Fenarticle%20schema%3AisPartOf%20%3Chttps%3A%2F%2Fen.wikipedia.org%2F%3E.%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20MINUS%20%7B%0A%20%20%20%20%20%20%20%20%3Farticle%20schema%3Aabout%20%3Fitem.%0A%20%20%20%20%20%20%20%20%3Farticle%20schema%3AinLanguage%20%22fa%22.%0A%20%20%20%20%20%20%20%20%3Farticle%20schema%3AisPartOf%20%3Chttps%3A%2F%2Ffa.wikipedia.org%2F%3E.%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%20%20GROUP%20BY%20%3Fitem%20%3FitemLabel%20%3Fenarticle%0A%20%20%20%20ORDER%20BY%20DESC(%3Flinkcount)%0A%20%20%7D%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%2Cfa%22.%20%7D%0A%7D%0A'
    myurl=u"https://query.wikidata.org/sparql?format=json&query=SELECT%20?item%20?enarticle%20(COUNT(DISTINCT%20?sitelink)%20AS%20?linkcount)%20?itemLabel%20WHERE%20{%20?item%20wdt:P31/wdt:P279%2a%20wd:Q486972%20.%20?sitelink%20schema:about%20?item%20.%20?item%20wdt:P17%20wd:Q794%20.%20optional%20{%20?enarticle%20schema:about%20?item%20;%20schema:isPartOf%20%3Chttps://en.wikipedia.org/%3E%20.}%20minus%20{%20?article%20schema:about%20?item%20.%20?article%20schema:inLanguage%20%22fa%22%20.%20?article%20schema:isPartOf%20%3Chttps://fa.wikipedia.org/%3E%20}%20SERVICE%20wikibase:label%20{%20bd:serviceParam%20wikibase:language%20%22en,fa%22%20.%20}%20}%20GROUP%20BY%20?item%20?itemLabel%20?enarticle%20ORDER%20BY%20DESC(?linkcount)"
	#print myurl
        
    try:
        resp = requests.get(myurl)
        resp=resp.json()
    except:
        print 'errrrrrrrrrrrrroooooooooooorrrrrrrrrrrr'
        return text,text2,myurl
    counter=0
    for items in resp["results"]["bindings"]:
        #try:
            
            Qitems,items_title=u'',u''
            Qitems=items["item"]["value"]
            try:
                if u'/Q' in Qitems:
                    Qitems=u'Q'+Qitems.split(u'/Q')[1].strip()
                #print str(items)
                items_title=items["enarticle"]["value"]
            except:
                continue
            if u'wiki/' in items_title:
                items_title=items_title.split(u'wiki/')[1]
                items_title=items_title.replace(u'%20',u' ').strip()
                items_title=urllib.unquote(items_title.encode('utf8')).decode('utf8')
            Link_count=items["linkcount"]["value"].strip()
            arabictitle=u''
            if Country in arabic_country:
                arabictitle=getArabic(items_title,Country)
                addlast=u'||'+arabictitle+u'\n'
            else:
                addlast=u'\n'
            try:
                enpage=pywikibot.Page(enSite,items_title)
                entext=enpage.get()
            except:
                with codecs.open( u'erroritme.txt',mode = 'a',encoding = 'utf8' ) as fars:
                    fars.write(Qitems+u'\t'+items_title+u'\n' )
                continue
            if re.sub(ur'\{\{ *([Gg]eobox|[Ii]nfobox)',u'',entext)==entext:
                 continue
            na_lang=re.findall(ur'\| *native_name *\=([^\|\n]+)(?:\n|\|)',entext)
            if not na_lang:
                if u'{{lang' in entext:
                    na_lang=entext.split(u'{{lang')[1].split('}}')[0]
                    if string.count(na_lang,u'|')>1:
                        na_lang=na_lang.split(u'|')[2].strip()
                    else:
                        if u'|' in na_lang:
                            na_lang=na_lang.split(u'|')[1].strip()
                        else:
                            na_lang=na_lang
            else:
                na_lang=na_lang[0].strip()
            if len(addlast.strip())<2:
                if na_lang and len(na_lang.split(u'{')[0].strip())<len(items_title)+5:
                    addlast=u'||'+na_lang.split(u'{')[0].strip()+u'\n'
                else:
                    na_lang=u''
                    addlast=u'|| \n'
            else:
                na_lang=arabictitle
            counter+=1
            #if counter > 2000:
            #    break
            text+=u'|-\n|{{جا:formatnum:'+str(counter)+u'}}||[[:en:'+items_title+u']]||'+Qitems+u'||{{جا:formatnum:'+Link_count+u'}}\n'
            na_lang=na_lang.split(u'{')[0].strip()
            if na_lang.strip() and len(na_lang.strip())<25 and re.sub(u'[a-zA-Z]+',u'',na_lang)==na_lang:
                text2+=u'|-\n| '+na_lang+u' > نام‌فارسی @ '+items_title+u' \n'
            else:
                text2+=u'|-\n| نام‌فارسی @ '+items_title+u' \n'
        #except:
        #    continue
    return text,text2,myurl

def save_page(text,text2,Country,extentions,myurl):
    is_arabic=False
    link_adress=u'ویکی‌پدیا:گزارش دیتابیس/شهرهای ناموجود ۲/'+extentions+Country
    upper_page=u'{{الگوی بالای فهرست شهرهای ناموجود|'+Country+u'}}\n'
    upper_page+=u'['+myurl+u' کوئری مورد نظر]\n'
    upper=u'{|class="wikitable sortable"\n!#!!مقالهٔ زیستگاه‌ها{{سخ}} در ویکی‌انگلیسی!!ویکی{{سخ}}داده!!میان{{سخ}}ویکی'
    down=u'|}'
    #if Country in arabic_country:
    #upper+=u'!!عنوان به زبان محلی{{سخ}} با کمی تغییرات'
    my_text=upper_page+u'\n<div style="float: right">\n'+upper+text+down+u'\n</div>\n<div style="float: right">\n{|class="wikitable sortable"\n!برای ابزار به‌ویکی‌فا انبوه {{سخ}} ستون زیر را کپی کنید'+text2+down+u'\n</div>'
    fapage=pywikibot.Page(faSite,link_adress)
    my_text=fapage.put(my_text,u'ربات: بروزرسانی آمار شهرهای ناموجود')

passport=True
for Ql in Qery_list:
        #if Qery_list[Ql]==u'اسلوونی':
        #    passport=True
        #if not passport:
        #    continue

    #try:
        pywikibot.output(u'------- '+Qery_list[Ql]+u' ---------')
        parts,extentions=u'',u''
        #شهر
        parts=u'city'
        text,text2,myurl=get_query(Ql,Qery_list[Ql],parts)
        save_page(text,text2,Qery_list[Ql],extentions,myurl)
        '''
        #بخش
        parts=u'bakhsh'
        extentions=u'بخش‌های '
        text,text2=get_query(Ql,Qery_list[Ql],parts)
        save_page(text,text2,Qery_list[Ql],extentions)'''
    #except:
    #    continue
#with codecs.open( 'Myresult2.txt',mode = 'w',encoding = 'utf8' ) as f:
#        f.write( str(my_dict) )