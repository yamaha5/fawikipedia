# -*- coding: utf-8  -*-
# Reza (User:yamaha5) 
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import wikipedia,config,json,fa_cosmetic_changes2
import query,re,string,login,sys

faSite=wikipedia.getSite("fa")
enSite=wikipedia.getSite("en")
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
boxes=[u'infobox',u'Geobox',u'Taxobo']
fortrans={u'فهرست کشورهای مستقل':u'فهرست کشورهای مستقل{{جا:!}}کشور',u'شهرستان‌های اسپانیا':u'شهرستان‌های اسپانیا{{جا:!}}شهرستان'
            ,u'کامین (تقسیمات کشوری فرانسه)':u'کامین (تقسیمات کشوری فرانسه){{جا:!}}کامین',u'بخش‌های جمهوری آذربایجان':u'بخش‌های جمهوری آذربایجان{{جا:!}}بخش'
            ,u'تقسیمات کشوری پاکستان':u'تقسیمات کشوری پاکستان{{جا:!}}بخش',u'زمان اروپای مرکزی':u'زمان اروپای مرکزی{{جا:!}}زمان'
            ,u'استان‌های قزاقستان':u'استان‌های قزاقستان{{جا:!}}استان',u'ایالت‌ها و ناحیه‌های میانمار':u'ایالت‌ها و ناحیه‌های میانمار{{جا:!}}ایالت'
            ,u'بخش‌های خودمختار اسپانیا':u'بخش‌های خودمختار اسپانیا{{جا:!}}بخش خودمختار',u'ایالت‌های برزیل':u'ایالت‌های برزیل{{جا:!}}ایالت'
            ,u'استان‌های آلبانی':u'استان‌های آلبانی{{جا:!}}استان',u'تقسیمات کشوری گرجستان':u'تقسیمات کشوری گرجستان{{جا:!}}بخش',u'استان‌های سری‌لانکا':u'استان‌های سری‌لانکا{{جا:!}}استان'
            ,u'استان‌های اسپانیا':u'استان‌های اسپانیا{{جا:!}}استان',u'فهرست دهستان‌های پالنسیا':u'فهرست دهستان‌های پالنسیا{{جا:!}}دهستان'
            ,u'ولایت‌های افغانستان':u'ولایت‌های افغانستان{{جا:!}}ولایت',u'ولسوالی‌های افغانستان':u'ولسوالی‌های افغانستان{{جا:!}}ولسوالی'
            ,u'ایالت‌ها و قلمروهای هند':u'ایالت‌ها و قلمروهای هند{{جا:!}}ایالت',u'استان‌های ترکیه':u'استان‌های ترکیه{{جا:!}}استان',u'استان‌های مصر':u'استان‌های مصر{{جا:!}}استان'
            ,u'ناحیه‌های ایتالیا':u'ناحیه‌های ایتالیا{{جا:!}}ناحیه',u'استان‌های ایتالیا':u'استان‌های ایتالیا{{جا:!}}استان',u'استان‌های هلند':u'استان‌های هلند{{جا:!}}استان'
            ,u'استان‌های ایرلند':u'استان‌های ایرلند{{جا:!}}استان',u'سرزمین‌های سوئد':u'سرزمین‌های سوئد{{جا:!}}سوئد',u'استان‌های سوئد':u'استان‌های سوئد{{جا:!}}استان'
            ,u'تقسیمات کشوری چین':u'تقسیمات کشوری چین{{جا:!}}استان',u'شهرداری در آلمان':u'شهرداری در آلمان{{جا:!}}شهر',u'سامانه بزرگراه‌های میان ایالتی':u'سامانه بزرگراه‌های میان ایالتی{{جا:!}}سامانه بزرگ‌راه'
            ,u'شهرستان در آمریکا':u'شهرستان در آمریکا{{جا:!}}شهرستان',u'تقسیمات سیاسی ایالات متحده آمریکا':u'تقسیمات سیاسی ایالات متحده آمریکا{{جا:!}}ایالت'
            ,u'فهرست شهرهای ارمنستان':u'فهرست شهرهای ارمنستان{{جا:!}}شهر'}

trans_dic={u'Country':u'کشور',u'country':u'کشور',u'Region':u'منطقه',u'Districts':u'بخش',u'Mayor':u'شهردار',u'Vice Mayor':u'معاون شهردار',u'Vice mayor':u'معاون شهردار'
            ,u'Settled':u'سکونتگاه',u'Tourism region':u'منطقه گردشگری',u'First mentioned':u'اولین معرفی',u'Phone prefix':u'پیش‌خط تلفن'
            ,u'Independent':u'خودمختار',u'mayor':u'شهردار',u'City Mayor':u'شهردار',u'Governing body':u'بدنه حکومت',u'Town':u'شهر',u'City':u'شهر'
            ,u'Established':u'تاسیس‌شده',u'Number of city council members':u'تعداد اعضای شورای شهر',u'Island':u'جزیره',u'island':u'جزیره',u'Post Code':u'کد پستی'
            ,u'Post code':u'کد پستی',u'post code':u'کد پستی',u'Postal code':u'کد پستی',u'Autonomous Region':u'منطقه خودمختار',u'Province':u'استان'
            ,u'Founded':u'تاسیس‌شده',u'Incorporated':u'ثبت‌شده',u'Granted city rights':u'معرفی به عنوان شهر',u'ZIP code':u'زیپ کد',u'Religions':u'مذهب‌ها'
            ,u'Mesoregion':u'میان‌منطقه',u'Languages':u'زبان‌ها',u'Official':u'رسمی',u'State':u'ایالت',u'Telephone code':u'کد تلفن',u'Municipality':u'شهرستان'
            ,u'Province':u'استان',u'Seat':u'صندلی',u'Racial makeup':u'ترکیب نژادی',u'Body':u'اعضا',u'Nearest city':u'نزدیک‌ترین شهر'
            ,u'Civic agency':u'نماینده شهر',u'District':u'منطقه',u'constituency':u'حوزهٔ انتخابی',u'County':u'کانتی',u'Administrator':u'مدیر',u'Governing body':u'هیات مدیره'
            ,u'Waterways':u'راه آبی',u'Environs':u'محیط',u'Vice-chairman':u'معاون',u'Chairman':u'مدیر',u'Roadmaster':u'راهدار',u'Capital':u'پایتخت',u'Councillor':u'عضو شورا'
            ,u'Administrative body':u'هیات مدیره',u'Quadrant':u'جهت',u'Ward':u'محدوده',u'Sector':u'بخش',u'Postcode':u'کد پستی',u'Village President':u'دهدار'
            ,u'Sub-Region':u'زیربخش',u'3-digit postal code prefix':u'پیش‌کد سه رقمی کد پستی',u'Post office Founded':u'تاسیس اداره پست',u'Incorporated (Village)':u'تبدیل به روستا'
            ,u'Incorporated (Town)':u'تبدیل به شهر',u'Census Ranking':u'رتبه سرشماری',u'Historic Sites':u'مناطق تاریخی',u'Zone':u'محدوده',u'Municipality/City':u'شهرستان/شهر'
            ,u'Department':u'بخش',u'Location in the state of ':u'موقعیت در ایالت',u'(population and area)':u'(جمعیت و مساحت)',u'Congressional district':u'محدودهٔ کنگره'
            ,u'Airport':u'فرودگاه',u'Public transit':u'حمل و نقل عمومی',u'City from':u'تاریخ شهر شدن',u'Oblast':u'اوبلاسک',u'Raion':u'رایون',u'City status':u'وضعیت شهر',u'Phone code':u'کد تلفن'
            ,u'Leader':u'رهبر',u'City rights':u'شهر شدن',u'Urban areas':u'منطقهٔ شهری',u'Location in Russia':u'موقعیت در روسیه',u'Location in Ukraine':u'موقعیت در اوکراین'
            ,u'Abolished':u'منسوخ',u'abolished':u'منسوخ'}
def organize_tag(my_text,my_box):
    my_text_result=re.findall(ur'\{\{(?:ویکی[‌ ]?سازی|برای|دیگر کاربردها|کاربردهای دیگر|دیگر کاربردهای|همچنین ببینید|درباره|سرنویس|بیشتر|بیشتر۲|درباره|درباره۲|دیگر افراد|دیگر افراد۲|دیگر افراد۳|تغییرمسیر|تغییرمسیر۲|تغییرمسیر۳|تغییرمسیر۴|اصلی|اصلی ۲|منبع|بدون منبع|لحن|تمیزکاری|طفره‌آمیز|نامفهوم|تبلیغات|بهبود منبع|طرفداری|درستی|ادغام با|ادغام از|ادغام|در دست ویرایش ۲|تازه درگذشته|اصلاح ترجمه|رده-نیاز)(?:.*?)?\}\}',my_text, re.IGNORECASE)
    if my_text_result:
       for i in my_text_result:
           my_text=i+u'\n'+my_text.replace(i+u'\n',u'').replace(i,u'')
    my_result=re.findall(ur'\| *(?:image|image2|image3|image4) *\=(.*?)(?:\n|\<|\||$)',my_box, re.IGNORECASE)
    if my_result:
       for i in my_result:
           my_text=re.sub(ur'\[\[ *(?:(:?file|image|پرونده|تصویر)\:)?'+i+ur' *\|.*?\]\]\n?',ur'',my_text, re.IGNORECASE)
    my_text=re.sub(ur'\{\{ *(جعبه اطلاعات|تصویر)\-نیاز.*?\}\}',ur'',my_text, re.IGNORECASE)
    return my_text

def login_wiki():
    password_wiki = open("/data/project/rezabot/pywikipedia/passfile", 'r')
    password_wiki=password_wiki.read().replace('"','').strip()    
    passwords=password_wiki.split(',')[1].split(')')[0].strip()
    usernames=password_wiki.split('(')[1].split(',')[0].strip()
    botlog=login.LoginManager(password=passwords,username=usernames,site=faSite)
    botlog.login()

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
            return u''
        else:
            return page_link.replace(u'_',u' ')

def persian_num(text):
    counti=-1
    for i in u'0123456789':
        counti+=1
        text=text.replace(i,u'۰۱۲۳۴۵۶۷۸۹'[counti])
        
    return text

def cleaning_box(my_box):
    my_box=my_box.replace(u'\r',u'')
    my_box=re.sub(ur'\<ref(.*?)\/ref\>',ur"", my_box)
    my_box=re.sub(ur'\<ref(.*?)\/\>',ur"", my_box)
    my_box=my_box.replace(u']]s ',u']] ').replace(u']] and [[',u']] و [[').replace(u']], [[',u']]، [[')
    my_box=my_box.replace(u'–present\n',u'-اکنون\n').replace(u'– present\n',u'- اکنون\n').replace(u'–present ',u'-اکنون ')
    my_box=my_box.replace(u'– present ',u'- اکنون ')
    return my_box

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

def Get_box (en_text):
    en_text=en_text.replace(u'\r',u'')
    en_text=en_text.replace(u'\n}}',u'\n}}\n')
    my_box=boxfind(en_text)
    if my_box.strip():
        return my_box
    lines=en_text.split('\n')
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
    print 'aaaaaaaaaaaa'
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
    return my_box

def linktranslation(text):
        linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        for item in linken:
                if not item in text:
                    continue
                if item.find(u'File:')!=-1 or item.find(u'file:')!=-1 or item.find(u'Image:')!=-1 or item.find(u'image:')!=-1 or item.find(u'Category:')!=-1 or item.find(u'category:')!=-1:
                    continue
                itemmain=item
                item=item.replace(u'en:',u'')
                if item.find('user:')!=-1 or item.find('User:')!=-1 or item.find('template:')!=-1 or item.find('Template:')!=-1 or item.find('category:')!=-1 or item.find('Category:')!=-1 or item.find('Wikipedia:')!=-1 or item.find('wikipedia:')!=-1 or item.find('Talk:')!=-1 or item.find('talk:')!=-1 or item.find('Help:')!=-1 or item.find('help:')!=-1:
                    continue
                itemen=item.split(u'|')[0].replace(u'[[',u'').replace(u']]',u'').strip()
                if text.find(itemmain)!=-1:
                    itemfa=englishdictionry(itemen ,'en','fa')
                else:
                    continue
                if itemfa==False:
                    itemen=item.replace(u'[[',u'').replace(u']]',u'').strip()
                    itemen=itemen.replace(u'[[',u'').replace(u']]',u'')
                    text=text.replace(u'[['+itemen+u']]',u'@1@'+itemen+u'@2@')
                    continue
                else:
                    text=text.replace(itemmain,u'@1@'+itemfa+u'@2@')
                linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        text=text.replace(u'@1@',u'[[').replace(u'@2@',u']]')

        trans_list=[u'river',u'parent',u'category']
        text=text.replace(u'\r',u'').replace(u'\t',u' ')
        for i in range(0,10):
             text=text.replace(u'   ',u' ').replace(u'  ',u' ')
        text=text.replace(u'\n ',u'\n').replace(u' \n',u'\n').replace(u' |',u'|').replace(u'| ',u'|').replace(u' =',u'=').replace(u'= ',u'=')

        for i in trans_dic:
            text=text.replace(u"="+i+u"\n",u"="+trans_dic[i]+u"\n").replace(u"="+i+u"|",u"="+trans_dic[i]+u"|")
        for i in trans_list:
            itemes=ur"|"+i+ur"="
            if itemes in text:
                results=text.split(itemes)[1].split(u'\n')[0]
                fa_results=englishdictionry(results,'en','fa')
                if fa_results:
                    text=text.replace(u"="+results+u'\n',u"="+fa_results+u'\n').replace(u"="+results+u'|',u"="+fa_results+u'|')

        return text

def englishdictionry( enlink ,firstsite,secondsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    if enlink==u'':
        return False    
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
        categoryname = query.GetData(params,site)  
        for item in categoryname[u'query'][u'pages']:
            case=categoryname[u'query'][u'pages'][item][u'langlinks']
        for item in case:
            if item[u'lang']==secondsite:
                intersec=item[u'*']
                break
        result=intersec    
        return result
    except: 
        return False

def text_translator(text):
        linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        for item in linken:
                itemmain=item
                item=item.replace(u'en:',u'')
                if item.find('user:')!=-1 or item.find('User:')!=-1 or item.find('template:')!=-1 or item.find('Template:')!=-1 or item.find('category:')!=-1 or item.find('Category:')!=-1 or item.find('Wikipedia:')!=-1 or item.find('wikipedia:')!=-1 or item.find('Talk:')!=-1 or item.find('talk:')!=-1 or item.find('Help:')!=-1 or item.find('help:')!=-1:
                    continue
                itemen=item.split(u'|')[0].replace(u'[[',u'').replace(u']]',u'').strip()
                if text.find(itemmain)!=-1:
                    itemfa=englishdictionry(itemen ,'en','fa')
                else:
                    continue
                if itemfa==False:
                    itemen=item.replace(u'[[',u'').replace(u']]',u'').strip()
                    itemen=itemen.replace(u'[[',u'').replace(u']]',u'')
                    text=text.replace(u'[['+itemen+u']]',u'@1@'+itemen+u'@2@')
                    continue
                else:
                    text=text.replace(itemmain,u'@1@'+itemfa+u'@2@')
                linken = re.findall(ur'\[\[.*?\]\]',text, re.S)
        text=text.replace(u'@1@',u'[[').replace(u'@2@',u']]')
        return text

def checksite(gallery,text):
    commons_images,image_texts=[],[]
    for aa in range(0,30):        
        gallery=gallery.replace(u' |',u'|').replace(u'\t',u'')
    gallery=gallery.replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n').replace(u'\n\n',u'\n')
    images=gallery.replace(u'\r',u'').split(u'\n')

    for image in images:
        if image.strip()=="":    
            continue
        imagefa=image
        image=image.split(u'|')[0].strip()
        imagecheck=image.replace(u'File:',u'').replace(u'file:',u'').replace(u'Image:',u'').replace(u'image:',u'')
        imagecheck=imagecheck.replace(u'پرونده:',u'').replace(u'تصویر:',u'').replace(u'تصوير:',u'').replace(u'رسانه:',u'')
        if image=="":    
            continue
        if image.find(u'.ogg')!=-1 or image.find(u'>')!=-1 or image.find(u'.oga')!=-1 or image.find(u'.ogv')!=-1 or image.find(u'.mid')!=-1:
            continue    
        params = {
                'action': 'query',
                'titles': image,#Image name
                'prop': 'imageinfo'
        }
        try :
           extend=imagefa.split(u'|')[1]    
           image_text=imagefa.replace(image.split(u'|')[0]+u'|',image.split(u'|')[0]+u'|<!--')+u'-->'
        except:
           image_text=imagefa.split(u'|')[0].strip()+u'|'
        try:
            queryresult = query.GetData(params)
            items=queryresult['query']['pages']
            for item in items:
                if queryresult['query']['pages'][item]['imagerepository']=='shared':
                    if text.lower().find(imagecheck.lower())!=-1 or text.lower().find(imagecheck.replace(u'_',u' ').lower())!=-1:
                       continue
                    image_texts.append(image_text)      
                else:
                    continue
        except:
            continue
    if image_texts !=[]:
        gallery=u'<gallery>\n'       
        for item in image_texts: 
            gallery+=item+u'\n'
        gallery+=u'</gallery>\n'
        gallery=text_translator(gallery)
        return gallery
    else:
        return False

def enwikiimagecheck(text_en2):
    try:
        im = re.search(ur'<(?:gallery)[^<>]*>[\S\s]*?</(?:gallery)>', text_en2)
        imagename=im.group(0).strip()
        return imagename.replace(u'<gallery>',u'<gallery>\n').replace(u'</gallery>',u'\n</gallery>')
    except:
        return False

def get_gallory_Run(text_fa,text_en):
    text_fa2=text_fa.replace(u'\r',u'')
    text_en2=text_en.replace(u'\r',u'')
    imagename=u''
    try: 
        imagename=enwikiimagecheck(text_en2)
        if imagename:
            engallerry=checksite(imagename,text_fa)
            if engallerry:
               try:
                  imfa = re.search(ur'<(?:gallery)[^<>]*>[\S\s]*?</(?:gallery)>', text_fa2)
                  imagename=imfa.group(0).strip()
                  return False
               except:
                    text_fa2=text_fa2.replace(u'\r',u'')    
                    if text_fa2.find(u'== جستارهای وابسته ==')!=-1 or text_fa2.find(u'==جستارهای وابسته==')!=-1 or text_fa2.find(u'== جُستارهای وابسته ==')!=-1 or text_fa2.find(u'==جُستارهای وابسته==')!=-1:
                       text_fa2=text_fa2.replace(u'==جستارهای وابسته==',u'== جستارهای وابسته ==').replace(u'== جُستارهای وابسته ==',u'== جستارهای وابسته ==').replace(u'==جُستارهای وابسته==',u'== جستارهای وابسته ==')
                       text_fa2=text_fa2.replace(u'== جستارهای وابسته ==',u'== نگارخانه ==\n'+engallerry+u'\n== جستارهای وابسته ==')
                       return text_fa2    
                    if text_fa2.find(u'== پانویس ==')!=-1 or text_fa2.find(u'==پانویس==')!=-1 :
                       text_fa2=text_fa2.replace(u'== پانویس ==',u'== نگارخانه ==\n'+engallerry+u'\n== پانویس ==')
                       return text_fa2    
                    if text_fa2.find(u'== منابع ==')!=-1 or text_fa2.find(u'==منابع==')!=-1 or text_fa2.find(u'==منبع==')!=-1 or text_fa2.find(u'==منبع‌ها==')!=-1 or text_fa2.find(u'== منبع ==')!=-1 or text_fa2.find(u'== منبع‌ها ==')!=-1:
                       text_fa2=text_fa2.replace(u'==منابع==',u'== منابع ==').replace(u'==منبع==',u'== منابع ==').replace(u'==منبع‌ها==',u'== منابع ==').replace(u'== منبع ==',u'== منابع ==').replace(u'== منبع‌ها ==',u'== منابع ==')
                       text_fa2=text_fa2.replace(u'== منابع ==',u'== نگارخانه ==\n'+engallerry+u'\n== منابع ==')
                       return text_fa2
                    if text_fa2.find(u'== پیوند به بیرون ==')!=-1 or text_fa2.find(u'==پیوند به بیرون==')!=-1 :
                       text_fa2=text_fa2.replace(u'== پیوند به بیرون ==',u'== نگارخانه ==\n'+engallerry+u'\n== پیوند به بیرون ==')
                       return text_fa2
                    if text_fa2.find(ur'رده:')!=-1:
                        num=text_fa2.find(ur'[[رده:')
                        text_fa2=text_fa2[:num]+u'== نگارخانه ==\n'+engallerry+'\n'+text_fa2[num:]
                    else:
                        m = re.search(ur'\[\[([a-z]{2,3}|[a-z]{2,3}\-[a-z\-]{2,}|simple):.*?\]\]', text_fa2)
                        if m:
                            if m.group(0)==u'[[en:Article]]':    
                                try:
                                    if string.count(text_fa2,u'[[en:Article]] --->')==1:
                                        text_fa2=text_fa2.split(u'[[en:Article]] --->')[0]+u'[[en:Article]] --->\n'+u'== نگارخانه ==\n'+engallerry+'\n'+text.split(u'[[en:Article]] --->')[1]
                                    else:
                                        text_fa2+='\n== نگارخانه ==\n'+engallerry    
                                except:
                                    text_fa2+='\n== نگارخانه ==\n'+engallerry
                            else:
                                num=text_fa2.find(m.group(0))
                                text_fa2=text_fa2[:num]+u'== نگارخانه ==\n'+engallerry+'\n'+text_fa2[num:]
                        else:                
                            text_fa2+='\n== نگارخانه ==\n'+engallerry
                    return text_fa2
            else:
                return False
    except:
        return False

def get_gallery(fa_text,en_text):
    if en_text==u' ' or en_text==u'':
        return fa_text
    if fa_text.find(u'<gallery')!=-1 or fa_text.find(u'</gallery')!=-1:  
        return fa_text
    new_text=get_gallory_Run(fa_text,en_text)
    if new_text:
        return new_text
    return fa_text

def check_coord(my_box,fa_text):
    my_box_case2=u''
    fa_text2 = re.sub(ur'(\{\{[Cc]oord\|.*?(\=title|,title)\}\})', u'', fa_text, re.MULTILINE)
    my_box_cases=re.findall(ur'\|(\s|)(lat_deg|latd|)*=(.*?)[\n\|]', my_box, re.MULTILINE)
    if my_box_cases:
        my_box_case2=my_box_cases[0][2].strip()
        try:
            my_box_case2=int(my_box_case2)
            if fa_text2!=fa_text:
                return fa_text2
        except:
            my_box_case2=u''
    if not my_box_case2:
        my_box2 = re.sub(ur'\{\{[Cc]oord\|.*?\}\}', u'', my_box, re.MULTILINE)
        if my_box2!=my_box:
            if fa_text2!=fa_text:
                return fa_text2

    return fa_text

def Translate_date_EntoFa(text):
    old_text=text
    enMonth = {u'آگست':u'اوت',u'آگوست':u'اوت',u'جولای':u'ژوئیه',
    u'مارچ':u'مارس',u'آپریل':u'آوریل',u'فوریوری':u'فوریه',
    u'january':u'ژانویه',u'jan ':u'ژانویه ',u'february':u'فوریه',
    u'feb ':u'فوریه ',u'march':u'مارس',u'mar ':u'مارس ',u'april':u'آوریل',
    u'apr ':u'آوریل ',u'may':u'مه',u'june':u'ژوئن',u'jun ':u'ژوئن ',
    u'july':u'ژوئیه',u'august':u'اوت',u'aug ':u'اوت ',u'september':u'سپتامبر',
    u'sept ':u'سپتامبر ',u'sep ':u'سپتامبر ',u'october':u'اکتبر',u'oct ':u'اکتبر ',
    u'november':u'نوامبر',u'nov ':u'نوامبر ',u'december':u'دسامبر ',u'dec ':u'دسامبر '}
    text=text.lower().strip()
    for i in enMonth:
        text_new = text.replace(i, enMonth[i])
        if text_new != text:
            return persian_num(text_new)
    return old_text

def Translate_date(text):
    enMonthRegex = ur'(?:آگست|آگوست|جولای|مارچ|آپریل|january|jan|february|feb|march|mar|april|apr|may|jun|june|july|august|aug|sep|sept|september|oct|october|nov|november|december|dec)'
    links = re.findall(ur'('+ enMonthRegex + ur' (?:\d{1,2}|[۱۲۳۴۵۶۷۸۹۰]{1,2})\, (?:\d{3,4}|[۱۲۳۴۵۶۷۸۹۰]{3,4}))',text, re.IGNORECASE)
    if links:
        links = re.findall(ur'(آگست|آگوست|جولای|مارچ|آپریل|january|jan|february|feb|march|mar|april|apr|may|jun|june|july|august|aug|sep|sept|september|oct|october|nov|november|december|dec) (\d{1,2}|[۱۲۳۴۵۶۷۸۹۰]{1,2})\, (\d{3,4}|[۱۲۳۴۵۶۷۸۹۰]{3,4})', links[0].lower())
        links=links[0][1]+u' '+links[0][0]+u' '+links[0][2]
        return Translate_date_EntoFa(links)
    links = re.findall(ur'((?:(?:\d{1,2}|[۱۲۳۴۵۶۷۸۹۰]{1,2}) |)' + enMonthRegex + ur' (?:\d{3,4}|[۱۲۳۴۵۶۷۸۹۰]{3,4}))',text, re.IGNORECASE)
    if links:
        return Translate_date_EntoFa(links[0])
    links = re.findall(ur'(\d{4}) census',text.lower(), re.IGNORECASE)
    if links:
        return u'سرشماری '+persian_num(links[0])
    return text

def Translate_box(my_box):
    my_box=re.sub(ur'(\|name\=.*?\n)',ur'|name={{جا:PAGENAME}}\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'\|airline\=(.*?)\n',ur'|airline={{جا:PAGENAME}}{{سخ}}\1\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'(\|en_name\=.*?\n)',ur'|en_name={{جا:PAGENAME}}\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'(\|official_name\=.*?\n)',ur'|official_name={{جا:PAGENAME}}\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'(\|title\=.*?\n)',ur'|title={{جا:PAGENAME}}\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'(\|map_caption\=.*?\n)',ur'|map_caption=موقعیت {{جا:PAGENAME}} در نقشه\n',my_box, re.IGNORECASE)
    for parameter in [ur'established_date',ur'established_date1',ur'established_date2',ur'established_date3',ur'extinct_date',ur'population_as_of']:
        links = re.findall(ur'\|'+parameter+ur'\=(.*?)\n',my_box, re.IGNORECASE)
        if links:
            my_box=my_box.replace(u'|'+parameter+u'='+links[0]+u'\n',u'|'+parameter+u'='+Translate_date(links[0])+u'\n')
    my_box=re.sub(ur'تاسیس',ur'تأسیس',my_box)
    return my_box

def main_box(faTitle,UserName):
    result={}
    passport=False
    msg,my_box=u' ',u''
    enTitle=englishdictionry(faTitle ,'fa','en')
    enpage=wikipedia.Page(enSite,enTitle)
    fapage=wikipedia.Page(faSite,faTitle)
    try:
        fa_text=fapage.get()
        fa_text_old=fa_text
    except:
        return
    try:
        en_text=enpage.get()   
    except:
        return

    fa_text2=fa_text.replace(u'{{جعبه اطلاعات-نیاز',u'{{')
    if u'{{جعبه' in fa_text2 or u'{{infobox' in fa_text2 or u'{{Infobox' in fa_text2 or u'{{geobox' in fa_text2 or u'{{Geobox' in fa_text2 or u'{{Taxobox' in fa_text2 or u'{{taxobox' in fa_text2:
        my_box=u''
    else:
        my_box=Get_box(en_text)
        if my_box:
            my_box=cleaning_box(my_box)
            my_box=my_box.replace(u'\t',u'    ').replace(u'\r',u'')
            my_box=linktranslation(my_box)
            for i in fortrans:
                my_box=my_box.replace(i,fortrans[i])
            my_box=Translate_box(my_box)
            fa_text=check_coord(my_box,fa_text)
            my_box=my_box.strip()+u'\n'
    if u'{{Taxobox' in my_box or u'{{taxobox' in my_box:
        my_box=re.sub(ur'(\]\][a-z]+)(?:\n|$)',u']]\n',my_box)
    if fa_text:
        fa_text=fa_text.strip()
        fa_text=get_gallery(fa_text,en_text)
        if my_box:
            fa_text=re.sub(ur'\{\{جعبه اطلاعات\-نیاز(\}\}|\|.*?\}\})',u'',fa_text)
        my_text=my_box+fa_text.strip()
        if fa_text_old.strip()!=my_text.strip():
            msg_main=u'[[وپ:ابزارک|افزودن جعبه]]> (درخواست [['+UserName+u']])'+msg
            my_text,Botversion,msg=fa_cosmetic_changes2.fa_cosmetic_changes(my_text,fapage,msg)
            msg_main+=msg.strip()
            my_text=organize_tag(my_text,my_box)
            fapage.put(my_text,msg_main)
            result['msg']=u'انجام شد! صفحه را تازه کنید.'
            print json.dumps(result)
        else:
            result['msg']=u'مقاله نیازی به تغییر نداشت!'
            print json.dumps(result)

faTitle=unicode(sys.argv[1],'UTF-8')
UserName=unicode(sys.argv[2],'UTF-8')
login_wiki()
main_box(faTitle,UserName)

