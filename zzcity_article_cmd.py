# -*- coding: utf-8  -*-
# Reza (User:yamaha5) 
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import wikipedia,pagegenerators,config,urllib,sys,json
import query,codecs,re,string

faSite=wikipedia.getSite("fa")
enSite=wikipedia.getSite("en")

wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
request_page=u'ویکی‌پدیا:ویکی‌پروژه ایجاد مقاله‌های شهرها با ربات/درخواست ساخت رباتیک'
versions=u' (۵.۴)'
boxes=[u'infobox',u'Geobox']
our_errors_done,our_errors_not_done=[],[]
Last_user=None
#{{جا:!}}
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
            ,u'شهرستان در آمریکا':u'شهرستان در آمریکا{{جا:!}}شهرستان',u'فهرست شهرهای ارمنستان':u'فهرست شهرهای ارمنستان{{جا:!}}شهر',u'استان‌های الجزایر':u'استان‌های الجزایر{{جا:!}}استان'
            ,u'شهرستان‌های الجزایر':u'شهرستان‌های الجزایر{{جا:!}}شهرستان',u"ناحیه‌های الجزایر":u"ناحیه‌های الجزایر{{جا:!}}ناحیه",u"district of Bangladesh":u"ناحیه‌های بنگلادش{{جا:!}}ناحیه"
            ,u"commune of Benin":u"کمون‌های بنین{{جا:!}}کمون",u"province of Bolivia":u"استان‌های بولیوی{{جا:!}}استان",u"mukim of Brunei":u"موکیم‌های برونئی{{جا:!}}موکیم",u"شهرداری‌های بلغارستان":u"شهرداری‌های بلغارستان{{جا:!}}شهرداری"
            ,u"استان‌های بورکینافاسو":u"استان‌های بورکینافاسو{{جا:!}}استان",u"commune of Burundi":u"کومون‌های بوروندی{{جا:!}}کومون",u"district of Cambodia":u"ناحیه‌های کامبوج{{جا:!}}ناحیه"
            ,u"department of Cameroon":u"دپارتمان‌های کامرون{{جا:!}}دپارتمان",u"استان‌های شیلی":u"استان‌های شیلی{{جا:!}}استان",u"district of the Republic of the Congo":u"ناحیه‌های جمهوری کنگو{{جا:!}}ناحیه"
            ,u'استان‌های ایران':u'استان‌های ایران{{جا:!}}استان' ,u'شهرستان‌های ایران':u'شهرستان‌های ایران{{جا:!}}شهرستان' ,u'بخش (تقسیمات کشوری)':u'بخش (تقسیمات کشوری){{جا:!}}بخش'
            }

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
            ,u'Airport':u'فرودگاه',u'Public transit':u'حمل و نقل عمومی',u'Abolished':u'منسوخ',u'abolished':u'منسوخ',u'Coastline':u'خط ساحلی'
            ,u"village":u"روستا" ,u"Village":u"روستا"
            }

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

def englishdictionry( enlink ,firstsite,secondsite):

    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    enlink=enlink.split(u'#')[0].strip()
    enlink=redirect_find( enlink,'en')
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

def boxfind(text_en):
    text_en=text_en.replace(u'{{ ',u'{{').replace(u'{{ ',u'{{').replace(u'{{template:',u'{{').replace(u'{{Template:',u'{{').replace(u'}}',u'}}\n')
    text_en=text_en.replace(u'|pop_footnotes',u'\n|pop_footnotes').replace(u'\n\n',u'\n')
    lines=text_en.split('\n')
    start=False    
    box=u'\n'
    diff=1
    linebaz,linebasteh=0,0
    for our_box in boxes:
        our_box=our_box.strip()
        up_our_box=our_box[0].upper()+our_box[1:]
        lower_our_box=our_box[0].lower()+our_box[1:]
        for line in lines:
            if line==u'':
                continue
            if line.find(u'{{'+lower_our_box)!=-1 :# lower case    
                start=True
                linebaz,linebasteh=0,0
                box+=u'{{'+lower_our_box+line.split(u'{{'+lower_our_box)[1]+'\n'
                linebaz += string.count( line,"{{" )
                linebasteh += string.count( line,"}}" )    
                diff=linebaz-linebasteh
                continue
            if line.find(u'{{'+up_our_box)!=-1 :# upper case
                start=True
                linebaz,linebasteh=0,0
                box+=u'{{'+up_our_box+line.split(u'{{'+up_our_box)[1]+'\n'
                linebaz += string.count( line,"{{" )
                linebasteh += string.count( line,"}}" )
                diff=linebaz-linebasteh
                continue
            if start==True and diff!=0:
                linebaz += string.count( line,"{{" )
                linebasteh += string.count( line,"}}" )
                diff=linebaz-linebasteh
                box+=line+'\n'
            if diff==0 and start==True:
                break
    box=box.replace(u'}}\n',u'}}')
    return box

def Get_box (en_text):
    en_text=re.sub(ur'\<ref(.*?)\/ref\>',ur"", en_text)
    en_text=re.sub(ur'\<ref(.*?)\/\>',ur"", en_text)
    my_box=boxfind(en_text)
    if my_box.strip():
        return my_box
    en_text=en_text.replace(u'\r',u'')
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
    
    my_box=re.sub(ur'\<ref(.*?)\/ref\>',ur"", my_box)
    my_box=re.sub(ur'\<ref(.*?)\/\>',ur"", my_box)
    my_box=my_box.replace(u']]s ',u']] ')
    return my_box

def Get_box_items (en_text,my_box,enpage,enTitle,faTitle,result):
    my_box=my_box.replace(u'\t',u' ').replace(u'\r',u'')
    my_box=re.sub(ur'(\[\[([fF]ile|پرونده|[Ii]mage)\:.*?\]\])',ur"", my_box)
    for i in range(0,10):	
        my_box=my_box.replace(u'   ',u' ').replace(u'  ',u' ')
    my_box=my_box.replace(u'\n ',u'\n').replace(u' \n',u'\n').replace(u' |',u'|').replace(u'| ',u'|').replace(u' =',u'=').replace(u'= ',u'=').replace(u'{{flag|',u'').replace(u'{{Flag|',u'')
    my_box=my_box.replace(u'|\n',u'\n|').replace(u'\n\n\n',u'\n\n')
    my_box=my_box.replace(u'{{flagicon|',u'').replace(u'{{Flagicon|',u'').replace(u'{{FlagIcon|',u'')
    otherLang,population,provience,country,cates,Is_one,elevation,twin_city,area,native_name=u'',u'',u'',u'',u'',u'',u'',u'',u'',u''

    my_box=my_box.replace(u'|Population',u'|population').replace(u'_Total=',u'_total=').replace(u'_Urban=',u'_urban=')
    if u'|population=' in my_box:
        population=my_box.split(u'|population=')[1].split(u'(')[0].split(u'}')[0].split(u'|')[0].split(u'\n')[0].split(u'a')[0].strip()
        population=population.replace(u' ',u'').split(u'(')[0].strip()

    if u'|population_total=' in my_box and (not population.strip()):
        population=my_box.split(u'|population_total=')[1].split(u'(')[0].split(u'}')[0].split(u'|')[0].split(u'\n')[0].split(u'a')[0].strip()
        population=population.replace(u' ',u'').split(u'(')[0].strip()

    if u'|population_metro=' in my_box and (not population.strip()):
        population=my_box.split(u'|population_metro=')[1].split(u'(')[0].split(u'}')[0].split(u'|')[0].split(u'\n')[0].split(u'a')[0].strip()
        population=population.replace(u' ',u'').split(u'(')[0].strip()

    if u'|population_urban=' in my_box and (not population.strip()):
        population=my_box.split(u'|population_urban=')[1].split(u'(')[0].split(u'}')[0].split(u'|')[0].split(u'\n')[0].split(u'a')[0].strip()
        population=population.replace(u' ',u'').split(u'(')[0].strip()
    population=population.split(u'<')[0].split(u'e')[0].split(u'E')[0].strip()
    if u'{{' in population:
        population=u''
    if population:
        population=u'{{جا:formatnum:'+population.split(u'[')[0]+u'}}'

    # Is one
    Is_one=ClaimFinder(enSite,enTitle,31,True)
    if u'|settlement_type=' in my_box:
        Is_one=my_box.split(u'|settlement_type=')[1].split(u'(')[0].split(u'}')[0].split(u'|')[0].split(u'\n')[0].split(u'a')[0].strip()
    
    if (not Is_one.strip()) or (u'زیستگاه انسانی'in Is_one) or Is_one!=re.sub(ur'[a-zA-Z]',u'',Is_one):
       Is_one=u'منطقهٔ مسکونی'
    

    for i in fortrans:
         Is_one=Is_one.replace(i,fortrans[i])

    # elevation
    if not elevation:
        elevation=u''
        my_box=my_box.replace(u'|Elevation',u'|elevation').replace(u'_Ft=',u'_ft=').replace(u'_M=',u'_m=').replace(u' ft=',u'_ft=').replace(u' m=',u'_m=').replace(u'|Höhe=',u'|höhe=')
        if u'|elevation_m=' in my_box:
            elevation=my_box.split(u'|elevation_m=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|höhe=' in my_box and (not elevation.strip()):
            elevation=my_box.split(u'|höhe=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|elevation_ft=' in my_box and (not elevation.strip()):
            elevation_f=my_box.split(u'|elevation_ft=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
            if (not u'{{' in elevation_f) and elevation_f:
                try:
                    elevation=round(int(elevation_f)/3.2808,2)
                    elevation=str(elevation)
                except:
                    pass  
    if u'{{' in elevation:
        elevation=u''
    elevation=elevation.split(u'<')[0].strip()
    if elevation:
        elevation=u'{{جا:formatnum:'+elevation+u'}}'

    # area
    if not area:
        area=u''
        my_box=my_box.replace(u'|Area',u'|area').replace(u'|Fläche',u'|fläche')
      
        if u'|area_total_km2=' in my_box:
            area=my_box.split(u'|area_total_km2=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|area_total_sq_mi=' in my_box and (not area.strip()):
            area_mi=my_box.split(u'|area_total_sq_mi=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
            if (not u'{{' in area_mi) and area_mi:
                try:
                    area=round(int(area_mi)/0.38610,2)
                    area=str(area)
                except:
                    pass
        if u'|area_urban_km2=' in my_box and (not area.strip()):
            area=my_box.split(u'|area_urban_km2=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|fläche=' in my_box and (not area.strip()):
            area=my_box.split(u'|fläche=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|area km2=' in my_box and (not area.strip()):
            area=my_box.split(u'|area km2=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|area_urban_sq_mi=' in my_box and (not area.strip()):
            area_mi=my_box.split(u'|area_urban_sq_mi=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
            if (not u'{{' in area_mi) and area_mi:
                try:
                    area=round(int(area_mi)/0.38610,2)
                    area=str(area)
                except:
                    pass
    
    if u'{{' in area:
        area=u''
    area=area.split(u'<')[0].strip()
    if area:
        area=u'{{جا:formatnum:'+area+u'}}'

    # twin city
    twin_city=ClaimFinder(enSite,enTitle,190,True)
    if not twin_city:
       twin_city=u''

    # native name
    my_box=my_box.replace(u'|Native',u'|native').replace(u'_Name',u'_name=')
    if u'|native_name=' in my_box:
        native_name=my_box.split(u'|native_name=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
        native_name=re.sub(ur"[\=\+\*\'\!\-qwertyuiopasdfghjklzxcvbnm\,\.\/QWERTYUIOPASDFGHJKLZXCVBNM\<\>\\"+'\"]',ur'',native_name)
        native_name=native_name.replace(u'_',u' ').strip()

    # provience
    provience=ClaimFinder(enSite,enTitle,131)
    if not provience:
        my_box=my_box.replace(u'|State',u'|state').replace(u'|Region',u'|region').replace(u'|Canton',u'|canton').replace(u'|District',u'|district')
        my_box=my_box.replace(u'|Location',u'|location').replace(u'|Subdivision',u'|subdivision').replace(u'|Bundesland',u'|bundesland')
        provience=u''
        if u'|state=' in my_box:
            provience=my_box.split(u'|state=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|region=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|region=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|canton=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|canton=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|district=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|district=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|location=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|location=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|subdivision_name1=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|subdivision_name1=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|subdivision_name2=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|subdivision_name2=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        if u'|bundesland=' in my_box and (not provience.strip()):
            provience=my_box.split(u'|bundesland=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()

        provience2=englishdictionry( provience ,'en','fa')
        if provience2:
                provience=provience2
        else:
            provience=provience.split(u'}')[0].split(u'|')[0].replace(u'[[',u'').replace(u']]',u'').strip()
    provience=provience.split(u'<')[0].strip()
    if u'{{' in provience:
        provience=u''
    # country
    country=ClaimFinder(enSite,enTitle,17)
    my_box=my_box.replace(u'|Country',u'|country')

    if not country:
        if u'|country=' in my_box:
            country=my_box.split(u'|country=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
            if u'{' in country:
                country=u''
        elif u'|subdivision_name=' in my_box and (not country):
            country=my_box.split(u'|subdivision_name=')[1].split(u'}')[0].split(u'|')[0].split(u'\n')[0].strip()
            if u'{' in country:
                country=u''
        else:
            if u'{{infobox' in my_box and (len(my_box.split(u'{{infobox')[1].split(u'\n')[0].strip().split(u' '))==2):
                country=my_box.split(u'{{infobox')[1].split(u'\n')[0].strip().split(u' ')[0]
            elif u'{{Infobox Palestinian Authority municipality' in my_box:
                country=u'فلسطین'
            else:
                errors=u'صفحهٔ [[:en:'+enTitle+u']] نام کشورش مشخص نیست!'
                result['error']=errors
                print json.dumps(result)
                return u'',u'',u'',u'',u'',u'',u'',u'',u'',u''
        if  country.lower()==u'settlement':
            errors=u'صفحهٔ [[:en:'+enTitle+u']] نام کشورش مشخص نیست!'
            result['error']=errors
            print json.dumps(result)
            return u'',u'',u'',u'',u'',u'',u'',u'',u'',u''
        if country==u'Georgia' or country==u'georgia':
            country=u'Georgia (country)'
        country2=englishdictionry( country ,'en','fa')
        if country2:
            country=country2
        else:
            country=country.split(u'}')[0].split(u'|')[0].replace(u'[[',u'').replace(u']]',u'').strip()
    if u'{{' in country:
        country=u''
    '''if country==u'ایران':
        result['error']=u'The country was Iran so it is passed'
        print json.dumps(result)
        with codecs.open('ZZIranCity.txt' ,mode = 'a',encoding = 'utf8' ) as f:
                    f.write(u'\n'+enTitle+u'\t'+faTitle)
        return u'',u'',u'',u'',u'',u'',u'',u'',u'',u'''''
    country=country.split(u'<')[0].strip()
    
    en_first_part=en_text.split(u'==')[0]
    if u'{{lang-en' in en_first_part:
        en_first_part=en_first_part.replace(u'{{lang-en'+en_first_part.split(u'{{lang-en')[1].split(u'}}')[0]+u'}}',u'')

    if u'{{lang-' in en_first_part:
        otherLang=u'{{lang-'+en_first_part.split(u'{{lang-')[1].split(u'}}')[0].strip()+u'}}'
        otherLang=otherLang.replace("'","")
        if u'{{Unicode|' in otherLang:
            otherLang=otherLang.split(u'{{Unicode|')[1].split(u'}}')[0].strip()
        if u'{{' in otherLang:
            otherLang=u''
    if not otherLang:
        if country==u'ایالات متحده آمریکا' or country==u'بریتانیا' or country==u'هند' or country==u'اسکاتلند' or country==u'ایرلند'  or country==u'ایرلند شمالی'  or country==u'ایرلند جنوبی' or country==u'استرالیا' or country==u'پاکستان' or country==u'انگلستان' or country==u'نیوزلند' or country==u'کانادا':
            otherLang=u'[[زبان انگلیسی|انگلیسی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'مکزیک' or country==u'اسپانیا' or country==u'آرژانتین' or country==u'پرو' or country==u'کوبا' or country==u'ونزوئلا' or country==u'کلمبیا' or country==u'اکوادور' or country==u'گواتمالا' or country==u'بولیوی' or country==u'هندوراس' or country==u'السالوادور' or country==u'شیلی' or country==u'پاراگوئه' or country==u'پاناما':
            esTitle=englishdictionry(enTitle ,'en','es')
            if esTitle:
                otherLang=u'[[زبان اسپانیایی|اسپانیایی]]: '+esTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان اسپانیایی|اسپانیایی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'پرتغال' or country==u'برزیل':
            ptTitle=englishdictionry(enTitle ,'en','pt')
            if ptTitle:
                otherLang=u'[[زبان پرتغالی|پرتغالی]]: '+ptTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان پرتغالی|پرتغالی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'مراکش' or country==u'فرانسه' or country==u'آلبانی‏' or country==u'بلغارستان‏' or country==u'بنین‏' or country==u'بوروندی‏' or country==u'جمهوری آفریقای مرکزی‏' or country==u'جمهوری دموکراتیک کنگو‏' or country==u'جمهوری کنگو‏' or country==u'چاد‏' or country==u'رواندا‏' or country==u'سنت لوسیا‏' or country==u'سوئیس‏' or country==u'کامرون‏' or country==u'گابن‏' or country==u'گینه استوایی‏' or country==u'لوکزامبورگ‏' or country==u'ماداگاسکار‏' or country==u'موریس‏' or country==u'نیوبرانزویک‏' or country==u'هائیتی‏':
            frTitle=englishdictionry(enTitle ,'en','fr')
            if frTitle:
                otherLang=u'[[زبان فرانسوی|فرانسوی]]: '+frTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان فرانسوی|فرانسوی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'آلمان':
            deTitle=englishdictionry(enTitle ,'en','de')
            if deTitle:
                otherLang=u'[[زبان آلمانی|آلمانی]]: '+deTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان آلمانی|آلمانی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'هلند':
            nlTitle=englishdictionry(enTitle ,'en','nl')
            if nlTitle:
                otherLang=u'[[زبان هلندی|هلندی]]: '+nlTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان هلندی|هلندی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()

        elif country==u'ایتالیا':
            itTitle=englishdictionry(enTitle ,'en','it')
            if itTitle:
                otherLang=u'[[زبان ایتالیایی|ایتالیایی]]: '+itTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان ایتالیایی|ایتالیایی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'سوئد':
            svTitle=englishdictionry(enTitle ,'en','sv')
            if svTitle:
                otherLang=u'[[زبان سوئدی|سوئدی]]: '+svTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                 otherLang=u'[[زبان سوئدی|سوئدی]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'مجارستان':
            otherLang=u'[[زبان مجاری|مجاری]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'الجزایر' or country==u'بحرین' or country==u'کومور' or country==u'چاد' or country==u'جیبوتی' or country==u'مصر' or country==u'اریتره' or country==u'عراق' or country==u'اردن' or country==u'کویت' or country==u'لبنان' or country==u'لیبی' or country==u'موریتانی' or country==u'مراکش' or country==u'عمان' or country==u'فلسطین' or country==u'قطر' or country==u'عربستان سعودی' or country==u'سومالی' or country==u'سودان' or country==u'سوریه' or country==u'تونس' or country==u'امارات متحده عربی' or country==u'صحرای غربی' or country==u'یمن':
            arTitle=englishdictionry( enTitle ,'en','ar')
            if arTitle:
                otherLang=u'[[زبان عربی|عربی]]: '+arTitle.split(u',')[0].split(u'(')[0].strip()
            else:
                otherLang=u''
        elif country==u'ارمنستان':
            hyTitle=englishdictionry(enTitle ,'en','hy')
            if hyTitle:
                otherLang=u'[[زبان ارمنی|ارمنی]]: '+hyTitle.split(u',')[0].split(u'(')[0].strip()
        elif country==u'ایران':
            hyTitle=englishdictionry(enTitle ,'en','fa')
            if hyTitle:
                otherLang=u''
        else:
            otherLang=u'[[خط لاتین|لاتین]]: '+enTitle.split(u',')[0].split(u'(')[0].strip()
        
    if Is_one==u'[[کشور سابق]]':
        country=u''
        Is_one=u''

    categories=enpage.categories()
    cates=u'\n'
    for category in categories:
       fa_cat=englishdictionry( category ,'en','fa')
       if fa_cat:
          cates+=u'[['+fa_cat+u']]\n'           
    return Is_one,otherLang,population,provience,country,cates,elevation,twin_city,area,native_name

def ClaimFinder(our_Site,page_title,claim_num,more=False):
    fa_result=u''
    fa_result_more=[]
    en_wdata=wikipedia.DataPage(wikipedia.Page(our_Site,page_title))
    #try:
    items=en_wdata.get()
    #except:
    #    return ''
    if items['claims']:
        case=items['claims']
        for i in case:
            if i['m'][1]==claim_num:
                fa_result=data2fa(i[u'm'][3][u'numeric-id'])
                if not more:
                     break
                else:
                    fa_result_more.append(u'[['+fa_result+u']]')
    if fa_result==u'ویکی‌پدیا:ابهام‌زدایی':
        return u''
    if more and fa_result_more:
        fa_result=u' '
        lenth=len(fa_result_more)-1
        if lenth>0:
            for i in fa_result_more:
                test_i=re.sub(ur'[a-zA-Z]',u'',i)
                if claim_num==31 and test_i!=test_i:
                   continue
                if i==fa_result_more[lenth]:
                   join=u' و '
                else:
                   join=u'، '
                fa_result+=join+i
            fa_result=fa_result[2:]
        else:
            fa_result=fa_result_more[0]
    if fa_result:
        fa_result=fa_result.strip()
    return fa_result


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

def Creat_fapage(faTitle,enTitle,num,result):
    enpage=wikipedia.Page(enSite,enTitle)
    fapage=wikipedia.Page(faSite,faTitle)
    try:
       en_text=enpage.get()
    except wikipedia.IsRedirectPage:
        enpage = enpage.getRedirectTarget()
        en_text=enpage.get()
        enTitle=enpage.title()
    except:
       errors=u'صفحهٔ [[:en:'+enTitle+u']] در ویکی‌انگلیسی وجود ندارد!'
       result['error']=errors
       print json.dumps(result)
       return num

    fapage_exist=fapage.exists()
    if fapage_exist:
        errors=u'صفحهٔ [['+faTitle+u']] در ویکی‌فا وجود داشت!'
        result['error']=errors
        print json.dumps(result)
        return num

    faTitle_old=englishdictionry( enTitle ,'en','fa')
    if faTitle_old and fapage_exist:
        errors=u'صفحهٔ [['+faTitle+u']] در ویکی‌پدیای فارسی با نام [['+faTitle_old+u']] وجود دارد در نتیجه تغییرمسیرش ساخته شد!'
        result['error']=errors
        print json.dumps(result)
        return num

    my_box=Get_box(en_text)
    if not my_box:
       errors=u'صفحهٔ [[:en:'+enTitle+u']] جعبه ندارد! معادل فارسی‌اش [['+faTitle+u']]'
       result['error']=errors
       print json.dumps(result)
       return num
    Is_one,otherLang,population,provience,country,category,elevation,twin_city,area,native_name=Get_box_items(en_text,my_box,enpage,enTitle,faTitle,result)
    if country.strip()==u'':
       return num
    my_box=linktranslation(my_box)
    my_box=my_box.replace(u'[[پایتخت]]',u'مرکز')
    adress=enpage.permalink().replace(u'&useskin=monobook',u'')
    today=u' '

    ref_adress=u'<ref>{{یادکرد-ویکی |پیوند='+adress+u' |عنوان='+enTitle+u'|بازیابی  ='+today+u'|زبان=انگلیسی}}</ref>'
    if twin_city:
        twin_city_1=u'\n== خواهرخوانده ==\n'
        if string.count(twin_city,u"[[")>1:
           twin_city=twin_city_1+u'شهرهای '+twin_city+u' خواهرخوانده‌های '+faTitle+u' هستند.'
        else:
           twin_city=twin_city_1+u'شهر '+twin_city+u' خواهرخواندهٔ '+faTitle+u' هست.'
    faTitle_Second_name=faTitle.split(u'،')[0].split(u'(')[0].strip()
    if faTitle.strip()!=faTitle_Second_name.strip():
        faTitle_Second_name_2=faTitle.replace(faTitle_Second_name,u'').replace(u'(',u'').replace(u')',u'').replace(u'،',u'').strip()
        category=u'\n{{ترتیب‌پیش‌فرض:'+faTitle_Second_name+u'}}\n'+category
    if u' '+country in Is_one and country.strip():
        countExtend=Is_one.replace(u' '+country,u' ').replace(u' در ',u' ').replace(u'‌های ',u' ').replace(u'های ',u' ').replace(u'‌ها ',u' ').replace(u'ها ',u' ').replace(u'[[',u' ').replace(u']]',u' ').strip()
        
        Is_one=Is_one[:-2]+u'{{جا:!}}'+countExtend+u']]'
    our_subst=u'{{جا:کاربر:Yamaha5/city|'+faTitle_Second_name+u'|'+otherLang+u'|'+population+u'|'+provience+u'|'+country+u'|'+ref_adress+u'|'+Is_one+u'|'+elevation+u'|'+twin_city+u'|'+area+u'|'+faTitle_Second_name+u'|'+enTitle+u'}}'
    for i in fortrans:
         my_box=my_box.replace(i,fortrans[i])
    my_box=my_box.replace(u']]s',u']]').replace(u']], ',u']]، ').replace(u']] and [[',u']] و [[').replace(u']] & [[',u']] و [[')
    my_box=Translate_box(my_box)
    if country==u'ایران':
        my_box=re.sub(ur'\| *native_name *\=[^\n\|]+\n',u'',my_box)
        
    our_text=my_box+u'\n'+our_subst+u'\n'+category+u'\n'
    our_text = re.sub(ur'[\r\n]{3,}', u"\n\n",our_text)
    our_text=our_text.replace(u'(منطقه)|',u'(منطقه){{جا:!}}|').replace(u'(شهرستان)|',u'(شهرستان){{جا:!}}|').replace(u'(ایالت)|',u'(ایالت){{جا:!}}|').replace(u'(استان)|',u'(استان){{جا:!}}|').replace(u'(بخش)|',u'(بخش){{جا:!}}|').replace(u'(محدوده)|',u'(محدوده){{جا:!}}|')
    our_text=our_text.replace(u'(منطقه)]]',u'(منطقه){{جا:!}}]]').replace(u'(شهرستان)]]',u'(شهرستان){{جا:!}}]]').replace(u'(ایالت)]]',u'(ایالت){{جا:!}}]]').replace(u'(استان)]]',u'(استان){{جا:!}}]]').replace(u'(بخش)]]',u'(بخش){{جا:!}}]]').replace(u'(محدوده)]]',u'(محدوده){{جا:!}}]]')

    if not fapage_exist:
        our_text=our_text+u'\n[[en:'+enTitle+u']]'
        #-------------------------------------------------------------------
        result['page_content']=our_text.strip()
        print json.dumps(result)
        #-------------------------------------------------------------------
    return num

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
    my_box=re.sub(ur'(\|official_name\=.*?\n)',ur'|official_name={{جا:PAGENAME}}\n',my_box, re.IGNORECASE)
    my_box=re.sub(ur'(\|map_caption\=.*?\n)',ur'|map_caption=موقعیت {{جا:PAGENAME}} در نقشه\n',my_box, re.IGNORECASE)
    for parameter in [ur'established_date',ur'established_date1',ur'established_date2',ur'established_date3',ur'extinct_date',ur'population_as_of']:
        links = re.findall(ur'\|'+parameter+ur'\=(.*?)\n',my_box, re.IGNORECASE)
        if links:
            my_box=my_box.replace(u'|'+parameter+u'='+links[0]+u'\n',u'|'+parameter+u'='+Translate_date(links[0])+u'\n')
    my_box=re.sub(ur'تاسیس',ur'تأسیس',my_box)
    return my_box

def run(faTitle,enTitle,result):
    faTitle=faTitle.replace(u'_',u' ').strip()
    faTitle = re.sub(u'(\u202A|\u202B|\u202C|\u202D|\u202E|\u200F|¬)',u'\u200C', faTitle)#حذف کارکترهای تغییرجهت
    faTitle = re.sub(u'‌{2,}', u'‌', faTitle) # پشت‌سرهم
    faTitle = re.sub(u'‌(?![ئاآأإژزرذدوؤةبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔ]|[\u0900-\u097F]|ֹ)', '', faTitle) # در پس
    faTitle = re.sub(u'(?<![ئبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔ]|[\u0900-\u097F]|f|ֹ)‌', '', faTitle) # در پیش
    faTitle=re.sub(ur"[ًٌٍَُِّْ]",u"",faTitle)
    faTitle=persian_num(faTitle)
    faTitle=faTitle.replace(u'ي',u'ی').replace(u'ك',u'ک')
    enTitle=enTitle.replace(u'_',u' ')
    num=0
    num=Creat_fapage(faTitle,enTitle,num,result)

def data2fa(number, strict=False):
    data=wikipedia.DataPage(int(number))
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

def main():
    make_text=u''
    result={}
    faname=unicode(sys.argv[1][8:],'UTF-8')
    enname=unicode(sys.argv[2][8:],'UTF-8')
    run(faname,enname,result)
main() 
 