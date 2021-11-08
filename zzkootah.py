#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# Reza (User:yamaha5) , 2011
#
# Distributed under the terms of the CC-BY-SA 3.0 .
import catlib ,pagegenerators
import wikipedia,urllib,gzip,codecs,re
import MySQLdb as mysqldb
import config,os
from datetime import timedelta,datetime
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
internetoff=False #-----------------------------------bedoone internet------------------------
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
text=u' '
file_content=u' '
now = datetime.now()
yesterday=str(now-timedelta(1)).replace('-','').split(' ')[0].strip()
todayup=u"'''به‌روز شده توسط ربات در تاریخ''''': ~~~~~''\n\n"
titlechart=u'!رتبه!! صفحه!!برچسب‌ها!!میان‌ویکی!!تعداد پیوند به!! تعداد رده!!تعداد نگاره!!حجم صغحه (بایت){{سخ}}حجم کمتر از ۵۰۰ بایت رنگی نمایش داده میشود !!توضیحات دیگر'+u'\n|-\n'
uppage=todayup+u'\n{| class="wikitable sortable"\n'+titlechart
downpage=u'\n|}\n[[رده:ویکی‌پدیا]]\n[[رده:آمارهای دیتابیس]]\n'
count=0
lines=u' '
#------------------------------------------------------------ sql part
siteq  = wikipedia.getSite("fa")
query = "SELECT page_title FROM page WHERE page_namespace = 0 AND page_is_redirect = 0 AND page_id NOT IN (SELECT tl_from FROM templatelinks WHERE tl_title = 'ابهام‌زدایی' AND tl_namespace = 10) ORDER BY page_len ASC LIMIT 3500;"
#wikipedia.output(u'Executing query:\n%s' % query)


conn = mysqldb.connect("fawiki.labsdb.org",
                       user = '',
                       passwd = '')
cursor = conn.cursor()
#query = query.encode(site.encoding())
cursor.execute(query)
results = cursor.fetchall()
#------------------------------sql finsh------------------
def condition(link):
      wikipedia.config.put_throttle = 0
      wikipedia.put_throttle.setDelay()
      if internetoff==True:
          return u'||\n|-\n'
      alarm=' '
      try:
         pagef = wikipedia.Page( wikipedia.getSite( u'fa' ),link )
         wikipedia.output( u'opening %s ...' % pagef.title() )
         text = pagef.get()
         alarm+=u' '
         objective=u'||'
        #----------------------------------------------refrences-------------------
         if text.find(u'{{منبع')!=-1:
             alarm+=u'بدون منبع ،'
         if text.find(u'{{حذف')!=-1:
             alarm+=u'حذف،'
         if text.find(u'{{بهبود')!=-1:
              alarm+=u'بهبود منبع ،'           
         if text.find(u'{{بدون منبع')!=-1:
              alarm+=u'بدون منبع ،'
         if text.find(u'{{متخصص')!=-1:
             alarm+=u'متخصص ،'
         if text.find(u'{{نوشتار خوب}}')!=-1:
             alarm+=u'{{قلم رنگ|سورمه‌ای|فیلی|مقاله خوب}}'
         if text.find(u'{{پیشنهاد برگزیدگی}}')!=-1:
             alarm+=u'{{قلم رنگ|بنفش|زرد|پیشنهاد برگزیدگی}}'
         if text.find(u'{{پیشنهاد خوبیدگی}}')!=-1:
             alarm+=u'{{قلم رنگ|سبز|زرد|پیشنهاد خوبیدگی}}'             
         if text.find(u'{{مقاله برگزیده}}')!=-1:
             alarm+=u'{{قلم رنگ|سفید|خاکستری|مقاله برگزیده}}'
        #----------------------------------------------khord----------------------
         if text.find(u'خرد}}')!=-1:
           if text.find(u'{{بخش-خرد')!=-1:
               alarm+=u'{{قلم رنگ|بنفش||بخش خرد}} ،'
           else:
               alarm+=u'خرد ،'
         if text.find(u'نیاز}}')!=-1:
           alarm+=u'نیازمند به ،'
         if text.find(u'{{طرفداری')!=-1:
             alarm+=u'عدم‌بی‌طرفی ،'
         if text.find(u'{{درستی')!=-1:
             alarm+=u'عدم توافق در درستی ،'
         if text.find(u'{{ادغام')!=-1:
             alarm+=u'ادغام ،'
         if text.find(u'{{در دست ویرایش')!=-1:
             alarm+=u'ویرایش ،'
         if text.find(u'{{ویکی‌سازی')!=-1:
             alarm+=u'ویکی‌سازی ،'
         if text.find(u'{{تمیزکاری')!=-1:
             alarm+=u'تمیزکاری ،'
         if text.find(u'{{لحن')!=-1:
             alarm+=u'لحن ،'
         if text.find(u'{{اصلاح')!=-1:
             alarm+=u'نیازمند ترجمه ،'
         if text.find(u'{{ابهام‌زدایی')!=-1:
             alarm+=u'ابهام‌زدایی ،'
         if text.find(u'{{بازنویسی')!=-1:
             alarm+=u'بازنویسی ،'
         if text.find(u'{{به روز رسانی')!=-1:
             alarm+=u'به‌روز رسانی ،'
         if text.find(u'{{به‌روز رسانی')!=-1:
             alarm+=u'به‌روز رسانی ،'
        #--------------------------------------------------------------------------
         if alarm[-1]==u'،':
             alarm=alarm[0:-1].strip()   
         interwikis=u'{{subst:formatnum:'+str(len(pagef.interwiki()) ).strip()+u'}}'
         cats=u'{{subst:formatnum:'+str(len(pagef.categories(api=True))).strip()+u'}}'
         linked=u'{{subst:formatnum:'+str(len(pagef.linkedPages())).strip()+u'}}'
         image=u'{{subst:formatnum:'+str(len(pagef.imagelinks())).strip()+u'}}'
         alarm+=u'||'+interwikis+u'||'+linked+u'||'+cats+u'||'+image+u'||{{حجم مقاله|'+pagef.title().strip()+u'|500}}||\n|-\n'
         return alarm
      except wikipedia.IsRedirectPage:
          return False
      except:
          return False
      
savetext,rowfa,rowfaend=u' ',u' ',u' '
count=0
for row in results:
            passport=True
            line=unicode(row[0],'UTF-8')
            wikipedia.output(line)
            blacklists=[u'۰',u'۱',u'۲',u'۳',u'۴',u'۵',u'۶',u'۷',u'۸',u'۹',u'خورشیدی',u'میلادی)',u'میلاد)',u'قمری)']
            for item in blacklists:
                if line.find(item)!=-1:
                    passport=False
                    break
            if passport:    
                conditions=condition(line.replace(u'_',u' '))
                if conditions:
                    count+=1
                    text+=u'|{{subst:formatnum:'+str(count)+u'}}||{{مقاله|'+line.replace(u'_',u' ').strip()+u'}}||'+conditions
                    if count==500 or count==1000 or count==1500:
                       text=uppage+text.strip()+downpage
                       #---------------------------------------------------------wiki upload----------------------
                       countf=str(count).replace(u'0',u'۰').replace(u'1',u'۱').replace(u'2',u'۲').replace(u'3',u'۳').replace(u'4',u'۴').replace(u'5',u'۵').replace(u'6',u'۶').replace(u'7',u'۷').replace(u'8',u'۸').replace(u'9',u'۹')
                       countl=str(count-499).replace(u'0',u'۰').replace(u'1',u'۱').replace(u'2',u'۲').replace(u'3',u'۳').replace(u'4',u'۴').replace(u'5',u'۵').replace(u'6',u'۶').replace(u'7',u'۷').replace(u'8',u'۸').replace(u'9',u'۹')             
                       uptitle=u'ویکی‌پدیا:گزارش دیتابیس/فهرست مقاله‌های کوتاه از %s تا %s/فهرست' %(countl,countf)
                       pagefa = wikipedia.Page( wikipedia.getSite( u'fa' ),uptitle)
                       pagefa.put(text, u'ربات:به‌روز رسانی', minorEdit = True)
                       del text
                       text=u' '
sign_page=u'ویکی‌پدیا:گزارش دیتابیس/فهرست مقاله‌های کوتاه/امضا'
madak=u'~~~~~'
site=wikipedia.getSite('fa')
sign_page=wikipedia.Page(site,sign_page)
sign_page.put(madak,u'ربات:تاریخ بروز رسانی')