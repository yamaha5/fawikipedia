#!/usr/bin/python
from __future__ import unicode_literals
# -*- coding: utf-8  -*-
# Reza (User:yamaha5) 
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
#todo:
#-------------------------------
#---------------------------
#python pwb.py imagetransfer -family:wikipedia -lang:en 'File:Question_Mark_Film_Poster.jpg' -tolang:fa -tofamily:wikipedia -keepname
#python pycore/pwb.py zzimageuploader
import scripts.imagetransfer0 as imagetransfer
import pywikibot,re,sys,json
from pywikibot import pagegenerators
from pywikibot import config
#from pywikibot.compat import query


pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0
faSite=pywikibot.Site('fa',fam='wikipedia')
enSite=pywikibot.Site('en',fam='wikipedia')
version=u' (۴.۱)'

def encat_query(ImageTilte):
    cats=[]
    if ImageTilte=='':
        return []    
    ImageTilte=ImageTilte.replace(u' ',u'_')
    queryresult = pywikibot.data.api.Request(site=enSite, action="query", prop="categories",titles=ImageTilte)
    queryresult=queryresult.submit()
    try:
        items=queryresult['query']['pages']
        for item in items:
            categoryha=queryresult['query']['pages'][item]['categories']
            break
        for cat in categoryha:
            cats.append(cat['title'])         
        return cats
    except: 
        return []

def make_image_description (faTitle,ImageTilte):
        categories=encat_query(ImageTilte)
        categories=u'\n'.join(categories)
        categories=categories.lower().replace(u'_',u' ')
        license, template, description=u'',u'',u''
        if 'album covers' in categories:
            license = u'جلد آلبوم'
            template = u'دلیل استفاده جلد آلبوم غیر آزاد'
            description = u'جلد'
        elif u'film poster' in categories or u'video covers' in categories or u'movie posters' in categories:
            license = u'جلد فیلم'
            template = u'دلیل استفاده جلد فیلم غیر آزاد'
            description = u'جلد'
        elif u'software covers' in categories:
            license = u'جلد نرم‌افزار غیر آزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'جلد'
        elif u'game covers' in categories:
            license = u'جلد بازی'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'جلد'
        elif u'book covers' in categories:
            license = u'جلد کتاب'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'جلد'
        elif u'magazine covers' in categories or u'journal covers‎' in categories or u'newspaper covers‎' in categories:
            license = u'جلد مجله'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'جلد'
        elif u'stamp' in categories:
            license = u'نگاره تمبر'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'نگاره تمبر'
        elif u'currency' in categories:
            license = u'نگاره پول'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'نگاره پول'
        elif u'coat of arms' in categories:
            license = u'نشان غیر آزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'نشان غیر آزاد'
        elif u'audio samples' in categories or u'audio clips‎' in categories:
            license = u'پرونده صوتی غیرآزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'پروندهٔ صوتی برای'
        elif u'video samples' in categories  or 'fair use media' in  categories:
            license = u'پرونده ویدئویی غیرآزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'پروندهٔ ویدئویی برای'
        elif u'logos' in categories or u'symbols' in categories or u'seals' in categories:
            license = u'نگاره نماد'
            template = u'دلیل استفاده لوگو غیر آزاد'
            description = u'نماد'
        elif u'icon' in categories:
            license = u'آیکون برنامه رایانه‌ای غیر آزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'آیکون'
        elif u'fair use character artwork' in categories:
            license = u'شخصیت غیرآزاد'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'تصویر'
        elif u'non-free posters' in categories:
            license = u'پوستر'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'پوستر'
        elif u'game covers' in categories:
            license = u'جلد بازی'
            template = u'دلیل استفاده جلد بازی غیر آزاد'
            description = u'جلد بازی'
        elif u'fair use in... images' in categories:
            license = u'منصفانه|عکس|عکاس یا ناشر آن'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'تصویر'
        elif u'fair use images' in categories:
            license = u'منصفانه|عکس|عکاس یا ناشر آن'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'تصویر'
        elif u'public domain' in categories:
            license = u'PD-USonly'
            template = u'اطلاعات'
            description = u'تصویر'
        elif u'abroad' in categories:
            license = u'PD-US-1923-abroad'
            template = u'اطلاعات'
            description = u'تصویر'
        else:
            license = u'منصفانه|عکس|عکاس یا ناشر آن'
            template = u'دلیل استفاده اثر غیر آزاد'
            description = u'تصویر'

        if template==u'اطلاعات':
            our_discription=u'\n'.join([
            u'{{اطلاعات',
            u'| توضیحات     = '+ description + u' [[' + faTitle + u']]',
            u'| منبع        = [[:en:' + ImageTilte.replace(u'پرونده:','File:') + u'|ویکی‌پدیای انگلیسی]]',
            u'| پدیدآور     = کاربران ویکی‌پدیای انگلیسی',
            u'| اجازه‌نامه   = {{' + license + u'}}',
            u'}}'
            ])
        else:
            our_discription=u'\n'.join([
                u'{{' + template,
                u' |توضیحات       = ' + description + u' [[' + faTitle + u']]',
                u' |منبع          = [[:en:' + ImageTilte.replace(u'پرونده:',u'File:') + u'|ویکی‌پدیای انگلیسی]]',
                u' |مقاله         = ' + faTitle,
                u' |بخش یا قسمت   = در جعبه',
                u' |کیفیت پایین‌تر = بله',
                u' |دلیل          = استفاده در مقالهٔ [[' + faTitle + u']]',
                u' |جایگزین       = ندارد',
                u' |اطلاعات بیشتر  = ',
                u'}}',
                u'',
                u'== اجازه‌نامه ==',
                u'{{' + license + u'}}'
            ])

        return our_discription

def clean_discription(imagename,page_title):
    page_title=page_title.replace(u'_',u' ')
    faImagepage = pywikibot.Page(faSite, u'File:'+imagename)
    enImagepage = pywikibot.Page(enSite, u'File:'+imagename)
    image_discription=make_image_description (page_title,u'File:'+imagename)
    pywikibot.output(u"\03{lightblue}"+image_discription+u"\03{default}")
    if faImagepage.get():
        faImagepage.put(image_discription,u'ربات:ترجمه و اصلاح متن پرونده'+version)
def upload_image(imagename,page_title):
        imagename=endig(imagename)
        pywikibot.output(imagename)
        try:
            imagepage = pywikibot.Page(enSite, u'File:'+imagename)
            imagepage = iter([imagepage])
            bot=imagetransfer.ImageTransferBot(imagepage, interwiki=False, targetSite=faSite,keep_name=True,ignore_warning=True)
            bot.run()
        except:
           return
        clean_discription(imagename,page_title)

def check_image(imagename):
    try:
        en_imagepage = pywikibot.Page(enSite, u'File:'+imagename)
        en_image_text=en_imagepage.get()
    except:
        pywikibot.output(u"\03{lightred}The image not existed in en.wikipedia. so it is passed!\03{default}")
        return False
    list_templates=templatequery('File:'+imagename)
    if list_templates:
        balck_list=[u'Template:Db',u'Template:Duplicate',u'Template:Db-meta',u'Template:Deletable image',u'Template:Deletable file',u'Template:Copy to Wikimedia Commons']
        for i in balck_list:
            if  i in list_templates:
                pywikibot.output(u"\03{lightyellow}The image condidated for delete or should move to commons. so it is passed!\03{default}")
                return False
        if u'Template:Non-free media' in list_templates:
            #try:
            fa_imagepage = pywikibot.Page(faSite, 'File:'+imagename)
            link_list=fa_imagepage.getReferences()
            counter=0
            for repage in link_list:
                if repage.title()!=u'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود':
                    counter+=-1
                counter+=1
                if counter>1:
                    pywikibot.output(u"\03{lightred}the image was Non-Free and in fa.wikipedia it used on many pages. so it is passed!\03{default}")
                    return False
                if repage.namespace()!=0 and repage.title()!=u'ویکی‌پدیا:گزارش دیتابیس/مقاله‌های دارای پیوند به پرونده ناموجود':
                    pywikibot.output(u"\03{lightred}the image was Non-Free and in fa.wikipedia it used on other namespaces (not Article)\03{default}")
                    return False
            #except:
            #   return False
        pywikibot.output(u"\03{lightgreen}The image is Ok! continue...\03{default}")
        return True
    else:
        pywikibot.output(u"\03{lightred}The image on en.wikipedia does not have standard template. so it is passed!\03{default}")
        return False

def endig(a):
    for i in range(0,10):
       b=a.replace(u'۰۱۲۳۴۵۶۷۸۹'[i], u'0123456789'[i])
       a=b
    return b

def checksite(image):
    queryresult = pywikibot.data.api.Request(site=faSite, action="query", prop="imageinfo",titles=u'File:'+image.replace(u" ",u"_"))
    queryresult=queryresult.submit()
    try:
        items=queryresult['query']['pages']
        for item in items:
            if queryresult['query']['pages'][item]['imagerepository']==u'shared':
                return True
            else:
                return True
    except:
        return False

def templatequery(enlink):
    temps=[]
    enlink=enlink.replace(u' ',u'_')
    categoryname = pywikibot.data.api.Request(site=enSite, action="query", prop="templates",titles=enlink,redirects=1,tllimit=500)
    categoryname=categoryname.submit()
    try:
        for item in categoryname['query']['pages']:
            templateha=categoryname['query']['pages'][item]['templates']
            break
        for temp in templateha:
            temps.append(temp['title'].replace(u'_',u' '))         
        return temps
    except: 
        return []

def upload_fatext(text,fa_page,image_case):    
    try:    
        pywikibot.output(u"ربات:حذف تصویر ناموجود"+u" [[:پرونده:"+ image_case+u"]]")
        text=text.replace(u'\r',u'').replace(u'{{audio||Play}}',u'').replace(u'<gallery>\n</gallery>',u'').replace(u'<gallery></gallery>',u'')
        text=gallerycheck(text)
        text=text.replace(u'تصویر:',u'پرونده:').replace(u'تصوير:',u'پرونده:').replace(u'پرونده:تصویر:',u'پرونده:')
        text=text.replace(u'پرونده:پرونده:',u'پرونده:').replace(u'پرونده:تصوير:',u'پرونده:').replace(u'File:',u'پرونده:').replace(u'file:',u'پرونده:')
        text=text.replace(u'تصویر:|\n',u'')
        text=text.replace(u'پرونده:|\n',u'')
        text=text.replace(u'تصوير:|\n',u'')
        fa_page.put(text,u"ربات:حذف تصویر ناموجود"+u" [[:پرونده:"+ image_case+u"]]"+version)
    except Exception as inst:
        pywikibot.output(inst)
        pass  

def main(gent):
    for page_title in gent:
        try:
            pywikibot.output(u"Working on '%s'..." % page_title.title())
            page_title=page_title.title().replace(u' ',u'_')
            pywikibot.output(u"\03{lightpurple}-------------Working on page '%s' ..." % page_title+u'---------------\03{default}')
            imagelist = pywikibot.data.api.Request(site=faSite, action="query", prop="images",imlimit="max",titles=page_title)
            imagelist=imagelist.submit()
            print(imagelist)
            value=imagelist['query']['pages'].values()
            print('-'*100)
            print(value)
            print('-'*100)
            print(list(value)[0]['images'])
            print('-'*100)
            for image in list(value)[0]['images']:
                print(image)
                imagesinfo = pywikibot.data.api.Request(site=faSite, action="query", prop="imageinfo",titles=image['title'])
                imagesinfo=imagesinfo.submit()
                for imageinfo in imagesinfo['query']['pages'].values():
                    imagename = re.match(ur'(?:' + u'|'.join(faSite.namespace(6, all = True))\
                    + u')\:(.*)', image[u'title']).group(1)
                    try:
                        if (imageinfo['missing']==u"" and imageinfo['imagerepository']==u""):
                            pywikibot.output(u"\03{lightpurple}++++Working on image '%s' ..." % imagename+u'++++\03{default}')
                            check_result=check_image(imagename)
                            if check_result:
                                upload_image(imagename,page_title)
                    except:
                        pywikibot.output(u"Skiping image '%s'..." % imagename)
        except:
            continue


cat = pywikibot.Category(faSite, u'رده:صفحه‌های دارای پیوند خراب به پرونده')
gent = pagegenerators.CategorizedPageGenerator(cat)
main(gent)