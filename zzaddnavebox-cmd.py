#!/usr/bin/python
# Reza (User:yamaha5) 
# -*- coding: utf-8 -*-
import fa_cosmetic_changes,re,query,sys,string
import wikipedia, pagegenerators,login,json
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
fasite = wikipedia.getSite('fa','wikipedia')
_cache={}
usernames=u'Fatranslator'
botversion=u'۷.۶'
boxes=[u'infobox',u'Geobox',u'Taxobo', u'جعبه']

def login_fa(usernames):    
    try:
        password_fa = open("/data/project/rezabot/pywikipedia/passfile2", 'r')
    except:
        password_fa = open("/home/reza/compat/passfile2", 'r')

    password_fa=password_fa.read().replace('"','').strip()
    passwords=password_fa.split('(')[1].split(',')[1].split(')')[0].strip()
    #-------------------------------------------
    botlog=login.LoginManager(password=passwords,username=usernames,site=fasite)
    botlog.login()

def solve_redirect(tem,fapage,fapage_redi,delink):
    tem = wikipedia.Page(fasite,tem.title())  
    try:
        text=tem.get()
        text=text.replace(u'[[ ',u'[[').replace(u' ]]',u']]').replace(u' |',u'|').replace(u'[['+fapage.title()+u']]',u'[['+fapage_redi.title()+u'|'+fapage.title()+u']]')
        text=text.replace(u'[['+fapage.title()+u'|',u'[['+fapage_redi.title()+u'|')
        tem.put(text,u'ربات:اصلاح تغییرمسیر')
        #wikipedia.output(u'\03{lightyellow}اصلاح تغیرمسیر درون الگو\03{default}')        
    except:
        pass

def link_filtering(tem_text,links):
    mytext=u'\n'
    tem_text_f=tem_text.replace(u'\r',u'')
    tem_text_f=tem_text_f.replace(u'\n*',u' ')
    tem_text_f=tem_text_f.replace(u'    |',u'|').replace(u'   |',u'|').replace(u'  |',u'|').replace(u' |',u'|')
    tem_text_f=tem_text_f.replace(u'    =',u'=').replace(u'   =',u'=').replace(u'  =',u'=').replace(u' =',u'=')
    #wikipedia.output(tem_text_f)
    our_test_text=re.sub(ur'\{\{ *[Nn]ational.*?squad',u'',tem_text_f)
    if our_test_text!=tem_text_f:
        for i in tem_text_f.split(u'\n|'):
            if i.find(u'p1')==-1 and i.find(u'p2')==-1 and i.find(u'p3')==-1 and i.find(u'p4')==-1 and i.find(u'p5')==-1 and i.find(u'p6')==-1 and i.find(u'p7')==-1 and i.find(u'p8')==-1 and i.find(u'p9')==-1 and i.find(u'p0')==-1 and i.find(u'coach')==-1:
                #wikipedia.output(i)
                mytext+=i
    elif tem_text_f!=re.sub(ur'\{\{ *[nN]avbox with columns',u'',tem_text_f):
        for i in tem_text_f.split(u'\n|'):
            if re.sub(u'^ *col\d{1,2} *\=',u'',i)==i:
                #wikipedia.output(i)
                mytext+=i
    elif tem_text_f!=re.sub(ur'\{\{ *[Yy]ear [Nn]obel [pP]rize [Ww]inners',u'',tem_text_f):
        for i in tem_text_f.split(u'\n|'):
            if re.sub(u'(chemistry|physics|medicine|economy|literature|peace)',u'',i)==i:
                #wikipedia.output(i)
                mytext+=i
    elif tem_text_f!=re.sub(ur'\{\{ *([Cc]ounty|جستارهای کشور)',u'',tem_text_f):
        for i in tem_text_f.split(u'\n|'):
            if re.sub(u'^ *(cr|md|ua|bd|ct|rv|cl|history|geography|politics|military|economy|society|culture|symbols) *\=',u'',i)==i:
                #wikipedia.output(i)
                mytext+=i
    elif tem_text_f!=re.sub(ur'\{\{ *([Uu]S state navigation box|[uU]S county navigation box)',u'',tem_text_f):
        for i in tem_text_f.split(u'\n|'):
            if i.find(u'body1')==-1 and i.find(u'body2')==-1 and i.find(u'body3')==-1 and i.find(u'body4')==-1 and i.find(u'body5')==-1 and i.find(u'body6')==-1 and i.find(u'body7')==-1 and i.find(u'body8')==-1:
                #wikipedia.output(i)
                mytext+=i
    else:
        for i in tem_text_f.split(u'\n|'):
            if i.find(u'list ')==-1 and i.find(u'list=')==-1 and i.find(u'list1')==-1 and i.find(u'list2')==-1 and i.find(u'list3')==-1 and i.find(u'list4')==-1 and i.find(u'list5')==-1 and i.find(u'list6')==-1 and i.find(u'list7')==-1 and i.find(u'list8')==-1 and i.find(u'list9')==-1 and i.find(u'list0')==-1 and i.find(u'فهرست۰')==-1 and i.find(u'فهرست۹')==-1 and i.find(u'فهرست۸')==-1 and i.find(u'فهرست۷')==-1 and i.find(u'فهرست۶')==-1 and i.find(u'فهرست۵')==-1 and i.find(u'فهرست۴')==-1 and i.find(u'فهرست۳')==-1 and i.find(u'فهرست۲')==-1 and i.find(u'فهرست۱')==-1 and i.find(u'content1')==-1 and i.find(u'content2')==-1 and i.find(u'content3')==-1 and i.find(u'content4')==-1 and i.find(u'content5')==-1 and i.find(u'content6')==-1 and i.find(u'content7')==-1 and i.find(u'content8')==-1 and i.find(u'content9')==-1 and i.find(u'content0')==-1:
                #wikipedia.output(u'>>>>>>'+i)
                mytext+=i

    black_text=u' '
    dict={u'<noinclude>':u'</noinclude>',u'{{یادکرد':u'}}',u'<ref':u'</ref',u'{{cite':u'}}',u'{{Cite':u'}}'}
    for a in dict:
        count=0
        for i in mytext.split(a):
            count+=1
            if count>1:
               black_text+=i.split(dict[a])[0]
    black_links2 = re.findall(ur'\[\[(.*?)(?:\||\]\])',black_text+mytext, re.S)
    #black_links2=[]
    #for i in black_links:
    #    black_links2.append(i.replace(u']]',u'').replace(u'[[',u'').strip().split(u'|')[0])
    new_links,delink=[],[]
    for i in links:
        itest=i.split(u'|')[0].replace(u'_',u' ').replace(u'&nbsp;',u' ')
        if not itest.strip():
            delink.append(i)
        if itest in black_links2 or itest in new_links or u':' in i:    
            continue
        else:  
            if itest==u'آذرشهر':    
                new_links.append(i)
                continue
            itest=itest.strip()
            itest=re.sub(u'[۱۲۳۴۵۶۷۸۹۰]',u'',itest)
            itest=re.sub(u'\((میلادی|قمری|پیش از میلاد|قبل از میلاد)\)',u'',itest)
            b_list=[u'کاپیتان (فوتبال)',u'استان',u'دهستان',u'کشور',u'شهر',u'شهرستان',u'بخش',u'فروردین',u'اردیبهشت',u'خرداد',
                u'تیر',u'مرداد',u'شهریور',u'مهر',u'آبان',u'آذر',u'دی',u'بهمن',u'اسفند',u'ژانویه',u'فوریه',u'مارس',u'ژوئیه',u'ژوئن',
                u'آوریل',u'اوت',u'سپتامبر',u'نوامبر',u'دسامبر',u'می',u'اکتبر']
            itest=re.sub(u'('+u'|'.join(b_list).replace(u')',u'\)').replace(u'(',u'\(')+u')',u'',itest)
            if not itest.strip():
                delink.append(i)
                continue
            itest=re.sub(u'[^صثقفغعهخحجچشسیبلاتنمکگظطزرذدپوژآيئؤًٌٍَُِّْٔ]',u'',itest)
            if not itest.strip():
                continue
            new_links.append(i)
    #for i in new_links:
    #    wikipedia.output(i)
    return new_links,delink

def boxfind(text_en):
    text_en=text_en.replace(u'{{ ',u'{{').replace(u'{{ ',u'{{').replace(u'{{template:',u'{{').replace(u'{{Template:',u'{{').replace(u'\r',u'')
    start=False    
    box=u'\n'
    diff=1
    linebaz,linebasteh=0,0
    for our_box in boxes:
        our_box=our_box.strip()
        up_our_box=our_box[0].upper()+our_box[1:]
        lower_our_box=our_box[0].lower()+our_box[1:]
        regex_result=re.findall(u'(\{\|([\n\s]+|)\{\{([\s]+|)'+our_box+u')',text_en, re.IGNORECASE)
        if regex_result:
            if regex_result[0][0].strip():
                pre_template=u'{|'
                post_tempate=u'|}'
                text_en=text_en.replace(u'{| ',u'{|').replace(u'{| ',u'{|').replace(u'{|\n',u'{|').replace(u'{|\n',u'{|')
                text_en=text_en.replace(u' |}',u'|}').replace(u' |}',u'|}').replace(u'\n|}',u'|}').replace(u'\n|}',u'|}')
        else:
            pre_template,post_tempate=u'',u''
        lines=text_en.split('\n')
        for line in lines:
            if line==u'':
                continue
            if line.find(pre_template+u'{{'+lower_our_box)!=-1 :# lower case    
                start=True
                linebaz,linebasteh=0,0
                box+=pre_template+u'{{'+lower_our_box+line.split(pre_template+u'{{'+lower_our_box)[1]+'\n'
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}"+post_tempate )    
                diff=linebaz-linebasteh
                continue
            if line.find(pre_template+u'{{'+up_our_box)!=-1 :# upper case
                start=True
                linebaz,linebasteh=0,0
                box+=pre_template+u'{{'+up_our_box+line.split(pre_template+u'{{'+up_our_box)[1]+'\n'
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}" +post_tempate)
                diff=linebaz-linebasteh
                continue
            if start==True and diff!=0:
                linebaz += string.count( line,pre_template+"{{" )
                linebasteh += string.count( line,"}}"+post_tempate )
                diff=linebaz-linebasteh
                box+=line+'\n'
            if diff==0 and start==True:
                break
        if box.strip():
            break
    return box.replace(u'}}|}',u'}}\n|}')

def Get_box (txt):
    my_box=boxfind(txt)
    if my_box.strip():
        return my_box.strip()
    txt=txt.replace(u'\r',u'')
    lines=txt.split('\n')
    matn=' '
    for line in lines:
        linebaz=string.count(line,'{{')
        linebaste=string.count(line,'}}')
        diff=linebaz-linebaste
        if diff==0:
            line=line.replace('{{','$AAAA$').replace('}}','!BBBB!')
        linebaz=0
        linebaste=0
        matn+=line+u'\n'
    my_box=''
    for our_box in boxes:
        our_box=our_box.strip()
        try:
            my_box= re.search(ur'(\{\{\s*['+our_box[0].lower()+our_box[0].upper()+ur']'+our_box[1:]+ur'[_\s](?:\{\{.*?\}\}|[^\}])*\}\})',matn, re.S).group(1)# if Template box has other name please chang this regex
            my_box=my_box.replace(u'$AAAA$',u'{{').replace(u'!BBBB!',u'}}')
            break
        except:
            continue
    if not my_box.strip():
        return False
    return my_box.strip()

def addtext (fapage,text,addtemplate,addtemplate2,msg_clean,username_r,tempetype):
    text_t=text.replace(u'_',u' ')
    if text_t.find(u'{{ابهام‌زدایی')!=-1 or text_t.find(u'{{نمایه')!=-1 or text_t.find(u'{{نام کوچک')!=-1 or text_t.find(u'{{نام خانوادگی')!=-1 or text_t.find(u'{{مقالات مجموعه‌نمایه')!=-1:
        return False
    text=text.replace(addtemplate+u'\n',u'')
    if tempetype=='navbox':
        if text.find(u'رده:')!=-1:
            num=text.find(u'[[رده:')
            text=text[:num]+addtemplate+u'\n'+text[num:]
        else:    
            text+=u'\n'+addtemplate
    elif tempetype=='sidebar':
        ourbox=Get_box (text)
        if not ourbox:
            text=addtemplate+u'\n'+text
            my_text_result=re.findall(ur'\{\{(?:ویکی[‌ ]?سازی|منبع|بدون منبع|لحن|تمیزکاری|طفره‌آمیز|نامفهوم|تبلیغات|بهبود منبع|طرفداری|درستی|ادغام با|ادغام از|ادغام|در دست ویرایش ۲|تازه درگذشته|اصلاح ترجمه|رده-نیاز)(?:.*?)?\}\}',text, re.IGNORECASE)
            if my_text_result:
               for i in my_text_result:
                   text=i+u'\n'+text.replace(i+u'\n',u'').replace(i,u'')
        else:
            return False
    else:
        return False

    text,cleaning_version,msg_clean2=fa_cosmetic_changes.fa_cosmetic_changes(text,fapage)
    try:                
        fapage.put(text,u'[[وپ:ابزارک|افزودن ناوباکس]] '+botversion+u'> '+addtemplate2+u' (درخواست [['+username_r+u']])'+msg_clean)
        #wikipedia.output(u'\03{lightred}++++'+fapage.title()+u'\03{default}')
        return True
    except:
        pass    
    return False

def templatequery(enlink):
    temps=[]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    enlink=enlink.replace(u' ',u'_')
    if _cache.get(tuple([enlink, 'templatequery'])):
        return _cache[tuple([enlink, 'templatequery'])]
    if enlink==u'':
        _cache[tuple([enlink, 'templatequery'])]=False
        return False    

    params = {
            'action': 'query',
            'prop':'templates',
            'titles': enlink,
            'redirects': 1,
            'tllimit':500,
    }
 
    try:
        categoryname = query.GetData(params,fasite)
        for item in categoryname[u'query'][u'pages']:
            templateha=categoryname[u'query'][u'pages'][item][u'templates']
            break
        for temp in templateha:
            temps.append(temp[u'title'].replace(u'_',u' ').replace(u'الگو:',u'').replace(u'template:',u'').strip())  
        _cache[tuple([enlink, 'templatequery'])]=temps
        return temps
    except: 
        _cache[tuple([enlink, 'templatequery'])]=False
        return False


def check_user_edits(username):
    username=username.replace(u' ',u'_')
    if _cache.get(tuple([username, 'check_user_edits'])):
        return _cache[tuple([username, 'check_user_edits'])]
    params = {
        'action': 'query',
        'list': 'users',
        'ususers': username,
        'usprop':'editcount'    
    }
    try:
        usernamequery = query.GetData(params,fasite)
        if usernamequery[u'query'][u'users'][0][u'editcount']>1000:
            _cache[tuple([username, 'check_user_edits'])]=True
            return True
        else:
            _cache[tuple([username, 'check_user_edits'])]=False
            return False
    except:
        _cache[tuple([username, 'check_user_edits'])]=False
        return False    


def check_user(fapage):
    First_user=''
    try:
        page_history=fapage.getVersionHistory()
        First_user=page_history[-1][2]
        if check_user_edits(First_user):
            return True,First_user
        else:
            return False,First_user
    except:
        return False,First_user

def add_nav(preloadingGen,username_r):
    for tem in preloadingGen:
        #user_pass,First_user=check_user(tem)
        #if not user_pass:
        #    continue
        #passport=True
        enchar=u'qwertyuiopasdfghjklzxcvbnm'
        tem_title=tem.title().replace(u'الگو:',u'')
        if not re.sub(u'[^صثقفغعهخحجچشسیبلاتنمکگظطزرذدپوژآيئؤًٌٍَُِّْٔ]',u'',tem_title).strip():
            continue
        if tem_title.find(u'/')!=-1 or tem_title.find(u'\\')!=-1:
            continue  
        try:
            tem_text=tem.get()
        except:
            continue
        tem_text=tem_text.replace(u'{{ ',u'{{').replace(u'{{ ',u'{{').replace(u'{{الگو:',u'{{').replace(u'{{Template:',u'{{').replace(u'{{template:',u'{{')
        TempTemplates=templatequery(tem.title())

        if not u'Navbox' in TempTemplates and not u'نوار جانبی' in TempTemplates:
            continue
        if u'Navbox' in TempTemplates:
            tempetype=u'navbox'
        if u'نوار جانبی' in TempTemplates:
            tempetype=u'sidebar'

        added_template=tem.title().replace(u'الگو:',u'').replace(u'template:',u'').replace(u'Template:',u'')
        if tem.namespace()!=10:
            continue
        redirects=tem.getReferences(redirectsOnly=True)
        redirect_list=[]
        for i in redirects:
            redirect_list.append(i.title().replace(u'الگو:',u'').replace(u'template:',u'').replace(u'Template:',u''))
        links=tem.linkedPages()
        link_t=[]
        for i in links:
            link_t.append(i.title())
        links_ref=tem.getReferences()
        link_t2=[]
        for i in links_ref:
            link_t2.append(i.title())
        links=[x for x in link_t if x not in link_t2]
        links,delink=link_filtering(tem_text,links)
        #wikipedia.output(u'-----------------------------------------')    
        old_tem_text=tem_text
        for nonlink in delink:
            tem_text=tem_text.replace(u'[['+nonlink+u']]',nonlink.split(u'|')[0])
        if old_tem_text!=tem_text:
            #wikipedia.output(u'\03{lightred}delinking\03{default}')
            tem.put(tem_text,u'ربات:برداشتن پیوندهای نالازم')
        added_links=[]
        for faTitle in links:
            #wikipedia.output(u'-------------'+faTitle)
            try:
                fapage=wikipedia.Page(fasite, faTitle)
                text=fapage.get()
            except wikipedia.IsRedirectPage:
                fapage_redi = fapage.getRedirectTarget()
                try:
                    text=fapage_redi.get()
                    solve_redirect(tem,fapage,fapage_redi)
                    fapage=fapage_redi
                except:
                    continue
            except:
                #wikipedia.output(u'\03{lightred}link was red\03{default}')
                continue
            #wikipedia.output(u'\03{lightblue}--'+fapage.title()+u'---------\03{default}')
            msg=u' '
            text,cleaning_version,msg_clean=fa_cosmetic_changes.fa_cosmetic_changes(text,fapage,msg)

            old_text=text
            for i in redirect_list: 
                text=text.replace(u'{{'+i+u'}}',u'{{'+added_template+u'}}').replace(u'{{'+i+u'|',u'{{'+added_template+u'|')
            fatemplates=templatequery(fapage.title())
            text=text.replace(u'{{ ',u'{{').replace(u' }}',u'}}').replace(u'{{الگو:',u'{{').strip()
            if not fatemplates:
                continue
            if text.find(u'{{'+added_template+u'}}')==-1 and (not added_template in fatemplates):
                addtemplate2=u'[[الگو:'+added_template+u']]'
                addtemplate=u'{{'+added_template+u'}}'
                addtext_result= addtext (fapage,text,addtemplate,addtemplate2,msg_clean,username_r,tempetype)
                if addtext_result:
                   added_links.append(faTitle)
                   #wikipedia.output(u'added= {{\03{lightpurple}'+added_template+u'\03{default}}}')    
                continue
 
            if old_text!=text:
                try:
                    fapage.put(text,u'ربات:اصلاح تغییرمسیر ناوباکس‌')
                    #wikipedia.output(u'\03{lightpurple}ربات:اصلاح تغییرمسیر ناوباکس\03{default}')
                except:
                    pass    
                continue
        my_result={}
        if added_links:
            my_result['msg']=u'الگو به «'+u'»، «'.join(added_links)+u'» افزوده شده!'
        else:
            my_result['msg']=u'الگو در همهٔ مقالات موجود است!'
        print json.dumps(my_result)

def main():    
    gen = None
    username_r=u'User:Yamaha5'
    genFactory = pagegenerators.GeneratorFactory()    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-newtem'):    
            arg=arg.replace(':','')
            if len(arg) == 7:
                genfa = pagegenerators.NewpagesPageGenerator(100, False, None,10)
            else:
                genfa = pagegenerators.NewpagesPageGenerator(int(arg[8:]), False, None,10)
            gen = pagegenerators.PreloadingGenerator( genfa,60)
        else:
            gen = genFactory.handleArg( arg )    
 
    if not gen:
        wikipedia.stopme()
        sys.exit()
    preloadingGen = pagegenerators.PreloadingGenerator(gen,pageNumber = 60)    
    #preloadingGen = pagegenerators.NamespaceFilterPageGenerator(gen,10)
    add_nav(preloadingGen,username_r)

login_fa(usernames)
faTitle=u'الگو:'+unicode(sys.argv[1],'UTF-8')
username_r=unicode(sys.argv[2],'UTF-8')
faPage = wikipedia.Page(fasite, faTitle)
add_nav([faPage],username_r)

'''
if __name__ == "__main__":
    login_fa(usernames)
    main()
else:
    login_fa(usernames)
    faTitle=unicode(sys.argv[1],'UTF-8')
    username_r=unicode(sys.argv[2],'UTF-8')
    faPage = pywikibot.Page(fasite, faTitle)
    add_nav([faPage],username_r)
'''