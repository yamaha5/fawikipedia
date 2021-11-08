#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# # Reza (User:yamaha5) , 2013
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import wikipedia,pagegenerators,re,pywikibot,query,json
import fa_cosmetic_changes,sys,codecs,string,login,time
wikipedia.config.put_throttle = 0      
wikipedia.put_throttle.setDelay()

#--------------------------------------------------------------------------------------
bot_version=u'(۷.۶)'
disambig_template=u'الگو:جعبه ابهام‌زدایی'
film_name=u'فیلم‌ها'
no_templates=[u'الگو:خوبیده',u'الگو:برگزیده',u'الگو:مقاله برگزیده',u'الگو:ویکی‌سازی رباتیک نه']
no_fa_words=[u'از',u'این',u'آن',u'اگر',u'برای',u'در',u'را',u'ما',u'شما',u'ایشان',u'آن‌ها',u'یک',u'دو',u'سه',u'چهار',u'پنج',u'هفت',u'هشت',u'نه',u'اول'
,u'دوم',u'سوم',u'چهارم',u'پنجم',u'ششم',u'هفتم',u'هشتم',u'نهم',u'زشت‌ترین',u'بهترین',u'بدترین',u'زیباترین',u'کوتاه‌ترین',u'بلندترین',u'بالاترین',u'افزون',
u'افقی',u'اکنون',u'اینجا',u'اینچنین',u'آری',u'پایین',u'پس',u'پسا',u'پشت',u'پیش',u'چنان',u'چندان',u'چندی',u'حالی',u'به',u'بدون',u'چند',
u'دیگر',u'سپس',u'شاید',u'کنون',u'کنونی',u'گاهی',u'گشت',u'گویا',u'گویی',u'ناچار',u'ناگه',u'ناگهان',u'هماره',u'همانا',u'همانجا',u'همچو',u'بزرگ',u'کوچک',u'تاریک'
,u'همچون',u'همگان',u'همواره',u'همیشگی',u'همیشه',u'هنوز',u'هیچ',u'یکان',u'یکبار',u'یکباره',u'آخرین',u'اولین',u'دیرترین',u'به',u'همه',u'هم',u'سر',u'با',u'زیر',u'روز',u'شب']
original_lang='fa'
film_cat=u'رده:مقاله‌های خرد سینمایی'
site_category=ur'رده'
hidden_cat=u'\n[[رده:ویکی‌سازی رباتیک]]'
Black_links=u'کاربر:FawikiPatroller/Black Links'
White_Links=u'کاربر:FawikiPatroller/White Links'
no_words=u'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
#--------------------------------------------------------------------------------------
site = wikipedia.getSite(original_lang)

'''
Select page_title  FROM page WHERE
    page_namespace = 0 AND page_namespace = 0 AND page_is_redirect = 0 AND page_title LIKE "%_%" AND LENGTH(page_title) < 150 AND LENGTH(page_title) > 5 
    AND NOT (page_title LIKE "%(%" or page_title LIKE "%ي%" or page_title LIKE "%ك%" or page_title LIKE "%۱%" or page_title LIKE "%۲%"  
    or page_title LIKE "%۳%" or page_title LIKE "%۴%" or page_title LIKE "%۵%" or page_title LIKE "%۶%" or page_title LIKE "%۷%"  
    or page_title LIKE "%۸%"or page_title LIKE "%۹%"or page_title LIKE "%۰%"or page_title LIKE "%1%"or page_title LIKE "%2%"or page_title LIKE "%3%" 
    or page_title LIKE "%4%"or page_title LIKE "%5%" or page_title LIKE "%6%" or page_title LIKE "%7%" or page_title LIKE "%8%" or page_title LIKE "%9%"  
    or page_title LIKE "%0%") ORDER BY LENGTH(page_title) DESC;

sql fawiki_p < links.sql > wiki_Articles.txt

zip wiki_Articles wiki_Articles.txt
'''

fa_link_text = codecs.open( '/data/project/rezabot/pywikipedia/wiki_Articles.txt','r' ,'utf8' )
fa_link_text = fa_link_text.read().replace(u'page_title',u'').strip()
fa_link_list=fa_link_text.replace(u'_',u' ').replace(u'\r',u'').strip().split(u'\n')
del fa_link_text
#--------------------------------------------------------------------------------------

def login_wiki():   
    password_wiki = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
    password_wiki=password_wiki.read().replace('"','').strip()    
    passwords=password_wiki.split(',')[1].split(')')[0].strip()
    usernames=password_wiki.split('(')[1].split(',')[0].strip()
    botlog=login.LoginManager(password=passwords,username=usernames,site=site)
    botlog.login()
    
def templatequery(enlink):
    temps=[]
    if enlink==u'':
        return []    
    enlink=enlink.replace(u' ',u'_')
    params = {
            'action': 'query',
            'prop':'templates',
            'titles': enlink,
            'redirects': 1,
            'tllimit':500,
    }

    try:
        categoryname = query.GetData(params,site)
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' '))         
        return temps
    except: 
        return []

TEMP_REGEX = re.compile(
    '{{(?:msg:)?(?P<name>[^{\|]+?)(?:\|(?P<params>[^{]+?(?:{[^{]+?}[^{]*?)?))?}}')

def compileLinkR(withoutBracketed=False, onlyBracketed=False):
    """Return a regex that matches external links."""
    notAtEnd = '\]\s\.:;,<>"\|\)'
    notAtEndb = '\]\s\.:;,<>"\|'
    notInside = '\]\s<>"'
    regex = r'(?P<url>http[s]?://[^%(notInside)s]*?[^%(notAtEnd)s]' \
            r'(?=[%(notAtEnd)s]*\'\')|http[s]?://[^%(notInside)s]*' \
            r'[^%(notAtEnd)s])' % {'notInside': notInside, 'notAtEnd': notAtEnd}
    regexb = r'(?P<urlb>http[s]?://[^%(notInside)s]*?[^%(notAtEnd)s]' \
            r'(?=[%(notAtEnd)s]*\'\')|http[s]?://[^%(notInside)s]*' \
            r'[^%(notAtEnd)s])' % {'notInside': notInside, 'notAtEnd': notAtEndb}
    if withoutBracketed:
        regex = r'(?<!\[)' + regex
    elif onlyBracketed:
        regex = r'\[' + regexb
    else:
        regex=r'(?:(?<!\[)'+ regex+r'|\['+regexb+')'
    linkR = re.compile(regex)
    return linkR

def findmarker(text, startwith=u'@@', append=None):
    # find a string which is not part of text
    if not append:
        append = u'@'
    mymarker = startwith
    while mymarker in text:
        mymarker += append
    return mymarker

def catquery(enlink):
    cats=[]  
    enlink=enlink.replace(u' ',u'_')
    params = {
                'action': 'query',
                'prop': 'categories',
                'titles': enlink,
                'redirects': 1,
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
        return False

def fa_replaceExcept(text, old, new, exceptions,marker='', site=None):
    if site is None:
        site = pywikibot.getSite()

    exceptionRegexes = {
        'comment':      re.compile(r'(?s)<!--.*?-->'),
        'header':       re.compile(r'\r?\n=+.+=+ *\r?\n'),
        'pre':          re.compile(r'(?ism)<pre>.*?</pre>'),
        'source':       re.compile(r'(?is)<source .*?</source>'),
        'category':       re.compile(ur'\[\['+site_category+ur'\:.*?\]\]'),
        'ref':          re.compile(r'(?ism)<ref[ >].*?</ref>'),
        'startspace':   re.compile(r'(?m)^ (.*?)$'),
        'table':        re.compile(r'(?ims)^{\|.*?^\|}|<table>.*?</table>'),
        'hyperlink':    compileLinkR(),
        'star':         re.compile(ur'^ ?[\#\*].*?(\n|$)'),
        'gallery':      re.compile(r'(?is)<gallery.*?>.*?</gallery>'),
        'link':         re.compile(r'\[\[[^\]\|]*(\|[^\]]*)?\]\]'),
        'URL':          re.compile(r'\[.*?\]'),
        'file':         re.compile(r'\[\[([fF]ile|پرونده|تصویر)\:[^\]\|]*(\|[^\]]*)?\]\]'),
        'interwiki':    re.compile(r'(?i)\[\[:?(%s)\s?:[^\]]*\]\][\s]*'
                                   % '|'.join(site.validLanguageLinks() +
                                              site.family.obsolete.keys())),
        'property':     re.compile(r'(?i)\{\{\s*#property:\s*p\d+\s*\}\}'),
        'invoke':       re.compile(r'(?i)\{\{\s*#invoke:.*?}\}'),
    }
    if isinstance(old, basestring):
        old = re.compile(old)

    dontTouchRegexes = []
    except_templates = False
    for exc in exceptions:
        if isinstance(exc, basestring):
            if exc in exceptionRegexes:
                dontTouchRegexes.append(exceptionRegexes[exc])
            elif exc == 'template':
                except_templates = True
            else:
                dontTouchRegexes.append(re.compile(r'(?is)<%s>.*?</%s>'
                                                   % (exc, exc)))
            if exc == 'source':
                dontTouchRegexes.append(re.compile(
                    r'(?is)<syntaxhighlight .*?</syntaxhighlight>'))
        else:
            dontTouchRegexes.append(exc)
    if except_templates:
        marker1 = findmarker(text)
        marker2 = findmarker(text, u'##', u'#')
        Rvalue = re.compile('{{{.+?}}}')
        Rmarker1 = re.compile('%(mark)s(\d+)%(mark)s' % {'mark': marker1})
        Rmarker2 = re.compile('%(mark)s(\d+)%(mark)s' % {'mark': marker2})
        dontTouchRegexes.append(Rmarker1)
        origin = text
        values = {}
        count = 0
        for m in Rvalue.finditer(text):
            count += 1
            while u'}}}%d{{{' % count in origin:
                count += 1
            item = m.group()
            text = text.replace(item, '%s%d%s' % (marker2, count, marker2))
            values[count] = item
        inside = {}
        seen = set()
        count = 0
        while TEMP_REGEX.search(text) is not None:
            for m in TEMP_REGEX.finditer(text):
                item = m.group()
                if item in seen:
                    continue
                seen.add(item)
                count += 1
                while u'}}%d{{' % count in origin:
                    count += 1
                text = text.replace(item, '%s%d%s' % (marker1, count, marker1))
                for m2 in Rmarker1.finditer(item):
                    item = item.replace(m2.group(), inside[int(m2.group(1))])
                for m2 in Rmarker2.finditer(item):
                    item = item.replace(m2.group(), values[int(m2.group(1))])
                inside[count] = item
    index = 0
    markerpos = len(text)
    while True:
        match = old.search(text, index)
        if not match:
            break
        nextExceptionMatch = None
        for dontTouchR in dontTouchRegexes:
            excMatch = dontTouchR.search(text, index)
            if excMatch and (
                    nextExceptionMatch is None or
                    excMatch.start() < nextExceptionMatch.start()):
                nextExceptionMatch = excMatch

        if nextExceptionMatch is not None \
                and nextExceptionMatch.start() <= match.start():
            index = nextExceptionMatch.end()
        else:
            if callable(new):
                replacement = new(match)
            else:
                new = new.replace('\\n', '\n')
                replacement = new

                groupR = re.compile(r'\\(?P<number>\d+)|\\g<(?P<name>.+?)>')
                while True:
                    groupMatch = groupR.search(replacement)
                    if not groupMatch:
                        break
                    groupID = groupMatch.group('name') or \
                              int(groupMatch.group('number'))   
                    try:
                        replacement = replacement[:groupMatch.start()] + \
                                      match.group(groupID) + \
                                      replacement[groupMatch.end():]
                    except IndexError:
                        print '\nInvalid group reference:', groupID
                        print 'Groups found:\n', match.groups()
                        raise IndexError
            text = text[:match.start()] + replacement + text[match.end():]
            break
            index = match.start() + len(replacement)
            markerpos = match.start() + len(replacement)
        
    text = text[:markerpos] + marker + text[markerpos:]

    if except_templates: 
        for m2 in Rmarker1.finditer(text):
            text = text.replace(m2.group(), inside[int(m2.group(1))])
        for m2 in Rmarker2.finditer(text):
            text = text.replace(m2.group(), values[int(m2.group(1))])
    return text

def redirect_find( page_link,wiki):
    page_link=page_link.replace(u' ',u'_')
    site = wikipedia.getSite(wiki.replace(u'_',u'-'))
    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link
    }
    query_page = query.GetData(params,site)
    try:
        redirect_link=query_page[u'query'][u'redirects'][0]['to']
        return redirect_link
    except:
        if 'missing=""' in str(query_page):
            return False
        else:
            return page_link.replace(u'_',u' ')

def wikify(link,username):
            result={}    
            counter=0
            passing=True
            item_in_text=[]
            page = wikipedia.Page(site,link )
            old_text,text,text2=u' ',u' ',u' '
            del old_text,text,text2
            old_text=page.get()
            page_size=sys.getsizeof(old_text)
            #if page_size>170000:
            #    return
            temp_list=templatequery(link)
            for i in no_templates:
                if i in temp_list:
                    passing=False                  
                    break
            if passing:
                Black_page = wikipedia.Page( site,Black_links)
                Black_List=Black_page.get().replace(u'*',u'').replace(u'\r',u'').split(u'\n')

                White_page = wikipedia.Page( site,White_Links)
                White_List=White_page.get().replace(u'*',u'').replace(u'\r',u'').split(u'\n')
                old_text,cleaning_version,msg_clean=fa_cosmetic_changes.fa_cosmetic_changes(old_text,page)
                old_text=old_text.replace(u'\r',u'').strip()
                text=old_text
                text2=text
                exceptions = ['URL','math', 'template', 'timeline','comment','header','pre','source','category','ref','startspace','table','hyperlink','gallery','link','interwiki','property','invoke', 'inputbox']
                fa_links = len(page.linkedPages())
                page_size=sys.getsizeof(old_text)
                size_limitation=page_size/1000
                counter=fa_links
                added_item=u' '
                if (size_limitation-counter)<1:
                    mojaz=u'۰'
                else:
                    mojaz=str(size_limitation-counter)
                result['msg']=u'تعداد پیوندهای مجاز برای اضافه شدن= '+mojaz
                for item in fa_link_list:
                    pass_root=True
                    if item.strip().find(u' ')==-1 or item.strip()==link.strip() or item.replace(u' ',u'_').strip()==link.replace(u' ',u'_').strip() :
                        continue
                    if counter > size_limitation:
                        result['msg']=result['msg']+u'<br>'+u'تعداد پیوندهای درونی بیش از حد مجاز برای ربات است.'
                        break
                    if old_text.find(item.strip())!=-1:
                        text3 = re.sub(ur"(\n|\*|\#|\s)"+item.strip()+ur"(\n|\.|\s|\،)", ur"",text)
                        if text3==text:
                            continue
                    else:
                        continue
                    if item not in Black_List:
                    
                    #if (old_text.find(u' '+item.strip()+u' ')!=-1 or old_text.find(u' '+item.strip()+u'،')!=-1 or old_text.find(u' '+item.strip()+u'.')!=-1 or old_text.find(u'\n'+item.strip()+u'\n')!=-1 or old_text.find(u'\n'+item.strip()+u' ')!=-1 or old_text.find(u' '+item.strip()+u'\n')!=-1) and (item not in Black_List):
                        for white in White_List:
                            if item in white and (old_text.find(u' '+white.strip()+u' ')!=-1 or old_text.find(u' '+white.strip()+u'\n')!=-1 or old_text.find(u'\n'+white.strip()+u' ')!=-1):
                                    item=white.strip()
                                    break
                        #--------------------------------
                        if old_text.find(u'[['+item.strip()+u']]')!=-1:
                            item_in_text.append(item)
                            continue
                        #--------------------------------
                        for i in item_in_text:
                             if item in i:
                                 pass_root=False
                                 break
                        if not pass_root:
                            continue
                        #--------------------------------
                        Item_R=redirect_find( item.strip(),original_lang)
                        if not Item_R:
                            continue
                        if old_text.find(u'[['+Item_R.strip()+u']]')!=-1 or Item_R.replace(u' ',u'_').strip()==link.replace(u' ',u'_').strip() or item in link or Item_R in link:
                            continue
                        #---------------------------------------
                        item_cat=catquery(item)
                        if item_cat:
                            if film_cat in item_cat:
                                continue
                        #---------------------------------------
                        if item_cat:
                            for i in item_cat:
                                 if film_name in i:
                                    pass_root=False
                                    break
                            if not pass_root:
                                continue
                        #----------------------------------------
                        temp_list=templatequery(item)
                        if not disambig_template in temp_list:
                            item_test=item
                            for i in no_words:
                                item_test=item_test.replace(i,u'')
                            if item_test!=item:
                                continue
                            if item.split(u' ')[0] in no_fa_words or item.split(u' ')[-1] in no_fa_words:
                                continue
                            pre_text={ur'\s':u' ',ur'\n':u'\n',ur'\*':u'*',ur'\#':u'#'}
                            for i in pre_text:
                                if old_text==text and ( pre_text[i]+item.strip()+u' ' in old_text):
                                    text = fa_replaceExcept(old_text, i+item.strip()+ur'\s', pre_text[i]+ur'[['+item.strip()+ur']] ', exceptions)
                                if old_text!=text:
                                    break
                                if old_text==text and ( pre_text[i]+item.strip()+u'\n' in old_text):
                                    text = fa_replaceExcept(old_text, i+item.strip()+ur'\n', pre_text[i]+ur'[['+item.strip()+ur']]\n', exceptions)
                                if old_text!=text:
                                    break
                                if old_text==text and ( pre_text[i]+item.strip()+u'.' in old_text):
                                    text = fa_replaceExcept(old_text, i+item.strip()+ur'.', pre_text[i]+ur'[['+item.strip()+ur']].', exceptions)
                                if old_text!=text:
                                    break
                                if old_text==text and ( pre_text[i]+item.strip()+u'،' in old_text):
                                    text = fa_replaceExcept(old_text, i+item.strip()+ur'\،', pre_text[i]+ur'[['+item.strip()+ur']]،', exceptions)
                                if old_text!=text:
                                    break

                            if old_text!=text:
                                counter+=1
                                old_text=text
                                added_item=added_item+u'[['+item+u']]، '

                if text!=text2:
                    added_item=added_item.strip()[:-1]
                    if not hidden_cat.strip() in text:
                         text=text+hidden_cat
                    page.put(text,u'[[وپ:ور|ویکی‌سازی رباتیک]] (درخواست '+username+')' +bot_version+u' >'+added_item +msg_clean)
                    result['msg']=result['msg']+u'<br>'+u'ویکی‌سازی انجام شد!'
                    del old_text,text,text2
                else:
                    result['msg']=u'ویکی‌سازی انجام نشد شاید تعداد پیوندهای درونی به حد مجاز رسیده باشند یا ربات موردی را نیافت!'
                print json.dumps(result)

login_wiki()
faname=unicode(sys.argv[1],'UTF-8')
username=unicode(sys.argv[2],'UTF-8')
try:
    wikify(faname,username)
except:
    result['msg']=u'خطایی رخ داد!'
    print json.dumps(result)
