#!/usr/bin/python
# -*- coding: utf-8  -*-
#
# # Reza (User:yamaha5) , 2014
#
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-

import query,pagegenerators,re,sys
import wikipedia,codecs,string,login
ensite = wikipedia.getSite('en')
fasite=wikipedia.getSite("fa")
_cache={}
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
YourAcountRootPath='/data/project/rezabot'
YourAcountPywikipediaPath=YourAcountRootPath+'/pywikipedia'

bot_version=u'7.00'

spe_cat_dict={u'People_of_':u'اهالی',u'People_from_':u'اهالی',u'Works_about_':u'آثار درباره',u'Works_based_on_':u'آثار برپایه',u'Politics_of_':u'سیاست'
            ,u'Works_by_':u'آثار',u'Works_of_':u'آثار',u'Works_originally_published_in_':u'آثار منتشرشده در'
            ,u'Works_set_in_the_':u'آثار تنظیم‌شده در',u'Subdivisions':u'تقسیمات کشوری',u'Suicides_by_jumping_in_':u'خودکشی با پریدن در'
            ,u'Suicides_by_sharp_instrument_':u'خودکشی با ابزار تیز در',u'People_associated_with_':u'افراد مرتبط با'
            ,u'People_educated_at_':u'دانش‌آموختگان',u'Magazines_established_in_':u'روزنامه‌های بنیان‌گذاری‌شده در'
            ,u'Kingdom_of_':u'پادشاهی',u'Films_shot_in_':u'فیلم‌های فیلمبرداری‌شده در',u'Films_directed_by_':u'فیلم‌های'
            ,u'Fictional_characters_from_':u'شخصیت‌های داستانی اهل',u'House_of_':u'خانه',u'Houses_in_':u'خانه‌ها در'
            ,u'Important_Bird_Areas_of_':u'پرندگان بومی',u'People_executed_by_':u'اعدام‌شدگان توسط',u"Villages_in_":u"روستاهای ",u"Cities_in_":u"شهرهای "
            ,u'Towns_in_':u'شهرک‌های ' }

Nationality={u"Afghan":u"افغانستان",u"Albanian":u"آلبانی",u"Algerian":u"الجزایر",u"American":u"ایالات متحده آمریکا",
u"Ancient Roman":u"روم باستان",u"Andorran":u"آندوران",u"Antigua and Barbuda":u"آنتیگوا و باربودا",u"Argentine":u"آرژانتین",
u"Armenian":u"ارمنستان",u"Aruban":u"اوربان",u"Australian":u"استرالیا",u"Austrian":u"اتریش",u"Austro-Hungarian":u"اتریش-مجارستان",
u"Azerbaijani":u"جمهوری آذربایجان",u"Bahamian":u"باهاما",u"Bangladeshi":u"بنگلادش",u"Belarusian":u"بلاروس",u"Belgian":u"بلژیک",
u"Belizean":u"بلیز",u"Beninese":u"بنین",u"Bermudian":u"برمودا",u"Bolivian":u"بولوی",u"Bonaire":u"بونیر",u"Bosnia and Herzegovina":u"بوسنی و هرزگوین",
u"Bosniak":u"بوسنی",u"Botswana":u"بوتسوانا",u"Brazilian":u"برزیل",u"British":u"بریتانیا",u"British Indian Ocean Territory":u"قلمرو بریتانیا در اقیانوس هند",
u"Bulgarian":u"بلغارستان",u"Cameroonian":u"کامرون",u"Canadian":u"کانادا",u"Catalan":u"کاتالان",u"Central African":u"آفریقای مرکزی",u"Chadian":u"چاد",
u"Chilean":u"شیلی",u"Chinese":u"چین",u"Collectivity of Saint Martin":u"سن-مارتن",u"Colombian":u"کلمبیا",u"Cook Islands":u"جزایر کوک",
u"Costa Rican":u"کاستاریکا",u"Cuban":u"کوبا",u"Curaçao":u"کوراسائو",u"Czech":u"جمهوری چک",u"Danish":u"دانمارک",
u"Democratic Republic of the Congo":u"جمهوری دموکراتیک کنگو",u"Dominica":u"دومینیکا",u"Dominican Republic":u"جمهوری دومینیکن",u"Dutch":u"هلند",
u"Dutch Antillean":u"آنتیل هلند",u"Egyptian":u"مصر",u"Emirati":u"امارات متحده عربی",u"Equatoguinean":u"گینه استوایی",u"Eritrean":u"اریتره",
u"Estonian":u"استونی",u"Ethiopian":u"اتیوپی",u"Falkland Islands":u"جزایر فالکلند",u"Federated States of Micronesia":u"ایالات فدرال میکرونزی",
u"Finnish":u"فنلاند",u"French":u"فرانسه",u"French Guianan":u"گویان فرانسه",u"French Polynesian":u"پلی‌نزی فرانسه",u"Gabonese":u"گابون",
u"Gambian":u"گامبیا",u"German":u"آلمان",u"Ghanaian":u"غنا",u"Greek":u"یونان",u"Guadeloupean":u"جزیره گوادلوپ",u"Guam":u"گوآم",u"Guinea-Bissauan":u"گینه بیسائو",
u"Guinean":u"گینه",u"Haitian":u"هائیتی",u"Hungarian":u"مجارستان",u"Icelandic":u"آیسلند",u"Indian":u"هند",u"Indonesian":u"اندونزی",
u"Iranian":u"ایران",u"Iraqi":u"عراق",u"Irish":u"ایرلند",u"Israeli":u"اسرائیل",u"Italian":u"ایتالیا",u"Jamaican":u"جامائیکا",u"Japanese":u"ژاپن",
u"Jordanian":u"اردن",u"Kazakhstani":u"قزاقستان",u"Kenyan":u"کنیا",u"Kiribati":u"کیریباتی",u"Korean":u"کره",u"Kosovar":u"کوزوو",
u"Kuwaiti":u"کویت",u"Kyrgyzstani":u"قرقیزستان",u"Lebanese":u"لبنان",u"Lesotho":u"لسوتو",u"Libyan":u"لیبی",u"Liechtenstein":u"لیختن‌اشتاین",
u"Lithuanian":u"لیتوانی",u"Luxembourgian":u"زبان لوکزامبورگ",u"Macedonian":u"مقدونیه",u"Malagasy":u"مالاگاسکا",u"Malawian":u"مالاوی",
u"Malaysian":u"مالزی",u"Maldivian":u"مالدیو",u"Malian":u"مالی (کشور)",u"Martinican":u"مارتینیک",u"Mauritian":u"موریتانی",
u"Mexican":u"مکزیک",u"Moldovan":u"مولداوی",u"Moroccan":u"مراکش",u"Mozambican":u"موزامبیک",u"Nagorno-Karabakh":u"ناگورنو قره‌باغ",
u"Namibian":u"نامیبیا",u"Nepalese":u"نپال",u"New Zealand":u"نیوزیلند",u"Nicaraguan":u"نیکاراگوئه",u"Nigerian":u"نیجریه",
u"Nigerien":u"نیجر",u"North Korean":u"کره شمالی",u"Norwegian":u"نروژ",u"Omani":u"عمان",u"Ottoman":u"عثمانی",u"Pakistani":u"پاکستان",
u"Palau":u"پالائو",u"Palestinian":u"فلسطین",u"Panamanian":u"پاناما",u"Papua New Guinean":u"پاپوآ گینه نو",u"Paraguayan":u"پاراگوئه",
u"Pashtun":u"پشتون",u"People's Republic of China":u"جمهوری خلق چین",u"Peruvian":u"پرو",u"Philippine":u"فیلیپین",u"Polish":u"لهستان",
u"Portuguese":u"پرتغال",u"Qatari":u"قطر",u"Republic of the Congo":u"جمهوری کنگو",u"Réunionnais":u"رئونیون",u"Romanian":u"رومانی",
u"Russian":u"روسیه",u"Saint Barthélemy":u"سن بارتلمی",u"Saint Helenian":u"سنت هلن",u"Saint Kitts and Nevis":u"سنت کیتس و نویس",
u"Saint Pierre and Miquelon":u"سن پی‌یر و میکلن",u"Saint Vincent and the Grenadines":u"سنت وینسنت و گرنادین‌ها",u"Sammarinese":u"سن مارینو",
u"São Tomé and Príncipe":u"سائوتومه و پرینسیپ",u"Saudi Arabian":u"عربستان سعودی",u"Scandinavian":u"اسکاندیناوی",u"Scottish":u"اسکاتلند",
u"Senegalese":u"سنگال",u"Serbian":u"صربستان",u"Seychellois":u"سیشل",u"Sierra Leonean":u"سیرالئون",u"Singaporean":u"سنگاپور",u"Sint Eustatius":u"سینت یوستیشس",
u"Sint Maarten":u"سینت مارتن",u"Slovak":u"اسلواکی",u"Slovenian":u"اسلوونی",u"Solomon Islands":u"جزایر سلیمان",u"South African":u"آفریقای جنوبی",
u"South Korean":u"کره جنوبی",u"Soviet":u"اتحاد جماهیر شوروی سوسیالیستی",u"Spanish":u"اسپانیا",u"Sudanese":u"سودان",u"Surinamese":u"سورینام",
u"Swedish":u"سوئد",u"Swiss":u"سوئیس",u"Syrian":u"سوریه",u"Tajikistani":u"تاجیکستان",u"Tanzanian":u"تانزانیا",u"Togolese":u"توگو",
u"Tokelauan":u"توکلائو",u"Trinidad and Tobago":u"ترینیداد و توباگو",u"Tunisian":u"تونس",u"Turkish":u"ترکیه",u"Turkish Cypriot":u"ترک‌های قبرس",
u"Turkmenistan":u"ترکمنستان",u"Turks and Caicos Islands":u"جزایر تورکس و کایکوس",u"Ugandan":u"اوگاندا",u"Ukrainian":u"اوکراین",u"Uruguayan":u"اروگوئه",
u"Uzbekistani":u"ازبکستان",u"Vatican City":u"واتیکان",u"Venezuelan":u"ونزوئلا",u"Wallis and Futuna":u"والیس و فوتونا",u"Welsh":u"ولز",
u"West German":u"آلمان غربی",u"Yemeni":u"یمن",u"Zambian":u"زامبیا",u"Zimbabwean":u"زیمبابوه"}

people_case=[u"academics",u"accordionists",u"accountants",u"activists",u"actors",u"actresses",u"admirals",u"models",u"agriculturalists",u"agronomists",
u"alchemists",u"groups",u"ambassadors",u"anarchists",u"animators",u"anthropologists",u"communists",u"fascists",u"nationalists",u"people",
u"archaeologists",u"archers",u"architects",u"arsonists",u"artists",u"writers",u"assassins",u"assyriologists",u"astronomers",u"atheists",u"engineers",
u"teams",u"autobiographers",u"avant-garde",u"aviators",u"winners",u"ayatollahs",u"bahá'ís",u"dancers",u"baptists",u"painters",u"players",u"coaches",
u"guitarists",u"billionaires",u"chemists",u"biographers",u"biologists",u"biophysicists",u"bishops",u"bloggers",u"singers",u"bodybuilders",
u"writer",u"botanists",u"boxers",u"directors",u"musicians",u"butchers",u"emperors",u"calligraphers",u"caricaturists",u"catholics",u"cattlemen",
u"cavalry",u"centenarians",u"chairmen",u"chefs",u"child",u"choreographers",u"christian",u"chronicles",u"cinematographers",u"circassians",u"civilians",
u"clarinetists",u"classical cellists",u"liberals",u"organists",u"pianists",u"violinists",u"communists",u"composers",u"programmers",u"computer scientists",
u"conductors",u"objectors",u"cosmologists",u"designers",u"revolutionaries",u"cryptographers",u"curators",u"cyclists",u"demographers",u"dentists",u"diarists",
u"diaspora",u"diplomats",u"divers",u"djs",u"playwrights",u"dramatists",u"traffickers",u"drummers",u"scientists",u"economists",u"editors",u"educationists",
u"educators",u"egyptologists",u"emigrants",u"empresses",u"engineer",u"entertainers",u"entomologists",u"environmentalists",u"equestrians",u"photographers",
u"esperantists",u"essayists",u"ethnologists",u"expatriate",u"explorers",u"families",u"farmers",u"female",u"models",u"swimmers",u"wrestlers",u"rappers",
u"feminists",u"feudalism",u"marshals",u"film actors",u"crew",u"director",u"producers",u"flautists",u"footballers",u"formalism",u"muslims",u"freemasons",
u"futurism",u"generals",u"geneticists",u"geographers",u"geologists",u"girl",u"grammarians",u"gymnasts",u"harpsichordists",u"keyboardists",u"historians",
u"humanists",u"illustrators",u"imams",u"inventors",u"investors",u"saxophonists",u"jewellers",u"jewish",u"journalists",u"jurists",u"knights",u"creatures",
u"lexicographers",u"libertarians",u"librarians",u"linguists",u"liqueurs",u"mafia",u"victims",u"maronites",u"marxists",u"mascots",u"mathematicians",
u"memoirists",u"men",u"merchants",u"meteorologists",u"methodists",u"sopranos",u"leaders",u"officers",u"personnel",u"specialisms",u"poets",u"monarchists",
u"monarchs",u"racers",u"climbers",u"murderers",u"makers",u"nazis",u"neuroscientists",u"novelists",
u"numismatists",u"nurses",u"oboists",u"occultists",u"competitors",u"orientalists",u"ornithologists",u"paleoanthropologists",u"paleontologists",
u"pashas",u"pastries",u"pathologists",u"performing arts",u"pharmacists",u"pharmacologists",u"philanthropists",u"philosophers",u"photojournalists",
u"chemists",u"physicians",u"physicists",u"physiologists",u"politicians",u"detainees",u"princes",u"princesses",u"prisoners",u"prosecutors",
u"prostitutes",u"protestants",u"psychiatrists",u"psychologists",u"puppeteers",u"puritans",u"quakers",u"rapists",u"refugees",u"republicans",u"researchers",
u"rowers",u"rulers",u"runners",u"sailors",u"saints",u"satirists",u"teachers",u"sculptors",u"killers",u"sexologists",u"shepherds",u"putters",u"riders",
u"slaves",u"slavs",u"workers",u"socialists",u"sociologists",u"soldiers",u"women",u"sprinters",u"statisticians",u"performers",u"surgeons",u"tenors",u"translators",
u"trumpeters",u"turkologists",u"violists",u"whistleblowers",u"wikipedians",u"zionists",u"zoologists",u"zoroastrians",u"judges",u"members",u"comedians",
u"noble_titles",u"theologians",u"ismailis",u"anglicans",u"cannibals",u"nobel_laureates",u"founders",u"popes",u"scholars",u"exiles",u"outlaws",
u"practitioners",u"lords",u"judoka",u"rabbis",u"baritones",u"contraltos",u"deists",u"veterinarians",u"alumni",u"clowns",u"hurdlers",u"drivers",u"abbots",
u"clergy",u"hermits",u"beekeepers",u"_duos",u"magicians",u"rebels",u"Satanists",u"Sufis",u"nomads",u"astronauts",u"karateka",u"priests",u"comedians",
u"Lutherans",u"criminals",u"presenters",u"collectors",u"evangelicals",u"critics",u"logicians",u"candidates",u"agnostics",u"semioticians",u"theorists",
u"cellists",u"neoconservatism",u"athletes",u"lawyers",u"practitioners"]

one_word=[u'محیط زیست']

orginal_plural=[u'politics',u'gymnastics']

plural_names={u'پرنده':u'پرندگان',u'جونده':u'جوندگان',u'':u'خزنده',u'':u'خزندگان'
              ,u'بازیکن':u'بازیکنان',u'هنرمند':u'هنرمندان',u'گوینده':u'گویندگان',u'نماینده':u'نمایندگان',u'مناطق حفاظت':u'مناطق حفاظت'
              ,u'دانشمند':u'دانشمندان',u'فروشنده':u'فروشندگان',u'قدیس':u'قدیسان',u'تهیه‌کننده':u'تهیه‌کنندگان'
              ,u'پهلوان':u'پهلوانان',u'اثر':u'آثار',u'آثار':u'آثار',u'سوانح':u'سوانح',u'سانحه':u'سوانح',u"افراد":u"افراد",u"اقوام":u"اقوام"
              ,u'میراث':u'میراث',u'خطوط':u'خطوط',u"ارواح":u"ارواح",u"اسامی":u"اسامی",u"اساطیر":u"اساطیر",u"جنگ‌سالار":u"جنگ‌سالاران"
              ,u"مخالف":u"مخالفان",u"روابط":u"روابط",u"رابطه":u"روابط",u"سواحل":u"سواحل",u"دور":u"دور",u"شطرنج":u"شطرنج",u"اقتصاد":u"اقتصاد"
              ,u"سیاست":u"سیاست",u"فجایع":u"فجایع",u"حقوق":u"حقوق",u"احزاب":u"احزاب",u"معادن":u"معادن",u"جوامع":u"جوامع",u"صنایع":u"صنایع",u"القاب":u"القاب"
              ,u"سنت":u"سنت",u"مناطق":u"مناطق",u"اشعار":u"اشعار",u"اعضا":u"اعضا",u"اهالی":u"اهالی"}
ZWNJ=u'‌'


def login_wiki(mode):
    if mode==1:
        dataSite=wikipedia.getSite('wikidata','wikidata')    
    if mode==2:
        dataSite=wikipedia.getSite('fa','wikipedia')
    try:
        password_wiki = open(YourAcountPywikipediaPath+"/passfile", 'r')
    except:
        password_wiki = open(wikipedia.config.datafilepath(config.password_file), 'r')
    password_wiki=password_wiki.read().replace('"','').strip()    
    passwords=password_wiki.split(',')[1].split(')')[0].strip()
    usernames=password_wiki.split('(')[1].split(',')[0].strip()
    botlog=login.LoginManager(password=passwords,username=usernames,site=dataSite)
    botlog.login()

def save_file(case,type):
    replace_dict={
    u'(ابهام‌زدایی)':u'',
    u' (شهر)':u'',
    u' (منطقه)':u'',
    u' (کشور)':u'',
    u'های در ':u'ها در ',    u'های بر ':u'ها بر ',
    u'زبان لوکزامبورگ':u'لوکزامبورگ',    u'افراد اهل':u'اهالی',
    u'همسرهای':u'همسران',    u'مقاله‌های':u'مقالات',
    u'شاهزاده‌های خانم‌های':u'شاهزاده خانم‌های',    u'جزایرها':u'جزایر',
    u'دانشگاه دانشگاه':u'دانشگاه',    u'قدیسین‌ها':u'قدیسین',
    u'کنت‌های (لقب)':u'کنت‌های',    u'شیکاگوها':u'شیکاگو',
    u'وزیران دفاع بر پایه کشور':u'وزیران دفاع',    u'وزارت دفاع بر پایه کشور':u'وزارت‌های دفاع',
    u'Wal':u'ولز',    u'رده:دولت':u'رده:سرپرستی',
    u'استان ایالت':u'ایالت', u'منطقه‌های':u'مناطق',
    u'الگو:':u'الگوهای ', u'مریخ‌ها':u'مریخ' ,u'شارجه (شهر)':u'شارجه',
    u'ساینس (نشریه)':u'مجله ساینس',
    u'خیال‌پردازی (گونه هنری)':u'هنر خیال‌پردازی',
    u'وحشت (گونه هنری)':u'هنر وحشت',
    u'خاطره‌نویسان روزانه':u'خاطره‌نویسان',
    u'بازیگران زن فیلم':u'زنان بازیگر فیلم',
    u'بازیگران مرد فیلم':u'مردان بازیگر فیلم',
    u'فیلم‌های مستند اهل':u'فیلم‌های مستند',
    u'مرد کودک':u'کودک مذکر',   u'زن کودک':u'کودک مؤنث',
    u'اندازه‌گیری اهل':u'اندازه‌گیری',    u'رمان‌های کودکان اهل':u'رمان‌های کودکان',
    u'ادبیات کودکان اهل':u'ادبیات کودکان',    u'واژه‌ها و عبارت‌های اهل':u'واژه‌ها و عبارت‌های',
    u'اپرای اهل':u'اپرا اهل',    u'اسکی (ورزش)':u'اسکی',
    u'٬':u'،', u'مغول‌های (قوم)':u'مغول‌ها',
    u'سنت‌های':u'سنت',
    u'القاب‌های':u'القاب',
    u'رده:الگوهای ':u'رده:الگو:',
    u'موج نوی':u'موج نو',
    u'ژیمناستیک‌ها ':u'ژیمناستیک ',
    u'رده:مردم‌های عرب ':u'رده:عرب‌ها ',
    u'مربع در ':u'میدان‌ها در ',
    u"‌های های ":u"‌های ",
    u"با سابقه کار در دفتر اسناد رسمی":u"دفتر اسناد رسمی",
    u'  ':u' '}
    try:
        ourcae=case.split(u'\t')[1]
        for i in replace_dict:
            case=case.replace(ourcae,ourcae.replace(i,replace_dict[i]))
    except:
        pass
    case=claen(case)
    file_text=u''
    if type==1:
       file=YourAcountPywikipediaPath+'/zz_cat_for_build.txt'
    if type==2:
       file=YourAcountPywikipediaPath+'/zz_cat_for_build_but_article_needed.txt'
    if type==3:
       file=YourAcountPywikipediaPath+'/zz_doublicated_fapages.txt'
    if type==4:
       file=YourAcountPywikipediaPath+'/zz_needed_purge_fapages.txt'
    try:        
        file_text = codecs.open(file,'r' ,'utf8')
        file_text = file_text.read().strip()
    except:
        file_text=u''
    if type==1:
        if not case.split(u'\t')[1]+u'\t'+case.split(u'\t')[2] in file_text:    
            with codecs.open(file ,mode = 'a',encoding = 'utf8' ) as f:
                                f.write(u'\n'+case)
    else:
        if not case in file_text:    
            with codecs.open(file ,mode = 'a',encoding = 'utf8' ) as f:
                                f.write(u'\n'+case)
    
 
def englishdictionry(enlink ,firstsite,secondsite):
    try:
        enlink=unicode(str(enlink),'UTF-8').replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    except:
        enlink=enlink.replace(u'[[',u'').replace(u']]',u'').replace(u'en:',u'').replace(u'fa:',u'')
    if enlink.find('#')!=-1:
        return u''
    if enlink==u'':    
        return u''
    if _cache.get(tuple([enlink, 'englishdictionry'])):
        return _cache[tuple([enlink, 'englishdictionry'])]
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
        try:
           redirect=categoryname[u'query'][u'redirects']
           _cache[tuple([enlink, 'englishdictionry'])]=u''
           return u''
        except:
            if result.find('#')!=-1:
                _cache[tuple([enlink, 'englishdictionry'])]=u''
                return u''
            _cache[tuple([enlink, 'englishdictionry'])]=result
            return result
    except:
        _cache[tuple([enlink, 'englishdictionry'])]=u''
        return u''
def Check_Page_Exists(page_link,wikisite):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'Check_Page_Exists'])):
        return _cache[tuple([page_link, 'Check_Page_Exists'])]
    params = {
        'action': 'query',
        'prop':'info',
        'titles': page_link
    }
    query_page = query.GetData(params,wikisite)
    try:
        for i in query_page[u'query'][u'pages']:    
            redirect_link=query_page[u'query'][u'pages'][i]['pageid']
            _cache[tuple([page_link, 'Check_Page_Exists'])]=True
            return True# page existed
    except:
        _cache[tuple([page_link, 'Check_Page_Exists'])]=False
        return False# page not existed
 
def redirect_find( page_link):
    page_link=page_link.replace(u' ',u'_')
    if _cache.get(tuple([page_link, 'redirect_find'])):
        return _cache[tuple([page_link, 'redirect_find'])]
    params = {
        'action': 'query',
        'redirects':"",
        'titles': page_link
    }
    query_page = query.GetData(params,ensite)
    try:
        redirect_link=query_page[u'query'][u'redirects'][0]['to']
        _cache[tuple([page_link, 'redirect_find'])]=False
        return False
    except:
        _cache[tuple([page_link, 'redirect_find'])]=True
        return True

def claen(cat_name):
    cat_name = re.sub(u'‌(?![ئاآأإژزرذدوؤةبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔ]|[\u0900-\u097F]|ֹ)', '', cat_name) # در پس
    cat_name = re.sub(u'(?<![ئبپتثجچحخسشصضطظعغفقکگلمنهیيًٌٍَُِّْٰٓٔ]|[\u0900-\u097F]|f|ֹ)‌', '', cat_name) # در پیش
    return cat_name

def get_cat (enTitle,faTitle):
    enpage= wikipedia.Page(ensite,enTitle)
    categories=enpage.categories()
    cates=u'\n'
    for category in categories:
       fa_cat=englishdictionry( category ,'en','fa')
       if fa_cat and fa_cat!=faTitle:
          cates+=u'[['+fa_cat+u']]\n'
    return cates

def Interwiki(enTitle,faTitle,num):
    if num==1:
        login_wiki(1)
        num=2
    en_wdata=wikipedia.DataPage(wikipedia.Page(ensite,enTitle))
    fa_wdata=wikipedia.DataPage(wikipedia.Page(fasite,faTitle))
    if en_wdata.exists():
        if fa_wdata.exists():
            wikipedia.output(u"Something is wrong, you need to merge with "+en_wdata.title())
        else:
            #try:
                items=en_wdata.get()
                en_wdata.setitem(summary=u"update item",items={'type': u'sitelink', 'site': 'fa', 'title': faTitle}) 
                en_wdata.setitem(summary=u"update label",items={'type': u'item', 'label': 'fa', 'value': faTitle})
                wikipedia.output(u"\03{lightgreen}Wikidata is updated!\03{default}")
            #except:
                #wikipedia.output(u"\03{lightred}Page in wikidata had error or it dosen't have any item!\03{default}")
    else:
        wikipedia.output(u"\03{lightblue}enwiki doesn't have any item so we will creat it!\03{default}")
        items={}
        try:
            en_wdata.setitem(summary=u"update item",items={'type': u'sitelink', 'site': 'en', 'title': enTitle}) 
            en_wdata.setitem(summary=u"update label",items={'type': u'item', 'label': 'en', 'value': enTitle})
            en_wdata.setitem(summary=u"update item",items={'type': u'sitelink', 'site': 'fa', 'title': faTitle}) 
            en_wdata.setitem(summary=u"update label",items={'type': u'item', 'label': 'fa', 'value': faTitle})
            wikipedia.output(u"\03{lightgreen}Wikidata is Created!\03{default}")
            return num
        except:
            wikipedia.output(u"\03{lightred}Page in wikidata had error or it dosen't have any item!\03{default}")
    return num

   
def creat_all_cat(username):
    num=0
    file=YourAcountPywikipediaPath+'/zz_cat_for_build.txt'
    file_text = codecs.open(file,'r' ,'utf8')
    file_text =u'\t'+file_text.read().replace(u'\r',u'').replace(u'  ',u' ').strip()
    lines=file_text.split(u'\n')
    doublicated_pages=u'\n'
    for i in lines:
        parts=i.split(u'\t')
        first_part=parts[0].strip()
        wikipedia.output(u'--------------------')
        wikipedia.output(parts[1])
        if parts[3].strip() :
            topPart=u'{{اصلی رده|'+englishdictionry(parts[3],'en','fa')+u'}}\n'
        else:
            topPart=u''
        fa_page= wikipedia.Page(fasite,parts[1].strip())
        if fa_page.exists():
            wikipedia.output(u'Page existed so it will continue')
            save_file(u'[['+parts[1].strip()+u']]\n',4)
            continue
        #------------if fa.page exists in another name!-----------
        fa_cat_page3th=englishdictionry( parts[2] ,'en','fa')
        if fa_cat_page3th:
            wikipedia.output(parts[1]+u' is doublicated page!')
            doublicated_pages=u'# [[:'+parts[1]+u']]\t > \t[[:en:'+parts[2]+u']]\t > \t[[:'+fa_cat_page3th+u']]\n'
            save_file(doublicated_pages,3)
            continue
        #----------------------------------------------------------
        fa_text=topPart+get_cat (parts[2],parts[1].strip())+u'\n[[en:'+parts[2]+u']]'
        fa_page.put(fa_text,u'ربات:ساخت رده خودکار'+username)

        fa_page= wikipedia.Page(fasite,parts[1].strip())
        if fa_page.exists():
            if num==0:
                login_wiki(2)
                num=1
            num=Interwiki(parts[2],parts[1].strip(),num)

    ali=ali2 #for stoping the bot after creation :)

def check_plural(i2,plural):
    if Check_Page_Exists(i2,ensite) and redirect_find(i2):
            fa_name=englishdictionry(i2,'en','fa').replace(u'رده:',u'')
            if fa_name.strip():
                if string.count(fa_name,u' ')>0 and (not one_word in one_word):
                    fa_name_part1=fa_name.split(u' ')[0].strip()
                    if i2[-1]==u's' or i2[-2:]==u'es' and (not i2.lower() in orginal_plural) and check_not_decade(i2):
                        plural=True
                    else:
                        plural=False
                    if fa_name_part1[-3:]!=u'های' and fa_name_part1[-2:]!=u'ها' and fa_name_part1[-1:]!=u'ز' and fa_name_part1[-1:]!=u'س' and fa_name_part1[-2:]!=u'ون' and fa_name_part1[-2:]!=u'ات' and fa_name_part1[-2:]!=u'ان' and plural:
                        if fa_name_part1 in plural_names:
                            fa_name_part1=plural_names[fa_name_part1]
                        else:
                            fa_name_part1=fa_name_part1+ZWNJ+u'های'
                    cat_name=fa_name.replace(fa_name.split(u' ')[0].strip(),fa_name_part1.strip())
                    cat_name = claen(cat_name)
                    return cat_name
                else:
                    cat_name=fa_name
                    if i2[-1]==u's' or i2[-2:]==u'es' and (not i2.lower() in orginal_plural) and check_not_decade(i2):
                        plural=True
                    else:
                        plural=False
                    if cat_name[-2:]!=u'ان' and cat_name[-2:]!=u'ها' and cat_name[-1:]!=u'س' and cat_name[-1:]!=u'ز' and cat_name[-2:]!=u'ون' and cat_name[-2:]!=u'ات' and cat_name[-3:]!=u'های' and plural:
                        if cat_name in plural_names:
                            cat_name=plural_names[cat_name]
                        else:
                            cat_name=cat_name+ZWNJ+u'ها'
                        cat_name = claen(cat_name)           
                    return cat_name
    return False

def double_check(i2,plural):
    i3=u'Category:'+i2
    fa_cat=check_plural(i3,plural)
    if fa_cat:
       return fa_cat 
    fa_cat=check_plural(i2,plural)
    return fa_cat

def check_not_decade(part):
    if part[-1:]==u's':
        numpart=part[:-1]
        numpart = re.sub(u'[0123456789۰۱۲۳۴۵۶۷۸۹\(\)]‌', u'', numpart)
        if numpart.strip():
           return False
        else:
           return True
    else:
        return True
My_Mode=u'T'
username=u''
for arg in wikipedia.handleArgs():
    if arg == u'-C' or arg == u'-c' or arg == u'-Creat' or arg == u'-creat':
       My_Mode=u'C'
    elif arg.startswith(u'-usern:'):
       username=u' (ترجمه توسط [[کاربر:'+arg[7:].replace(u'"',u'').replace(u'user:',u'').replace(u'User:',u'').replace(u'کاربر:',u'').strip()+u']])'
       wikipedia.output(u'\03{lightgreen}--> '+username+u'\03{default}')
    else:
       continue

if not My_Mode==u'T':
    creat_all_cat(username) # creat new categories!
    wikipedia.stopme()    
    sys.exit()

#----------------------------------------------------------------------
try:
    text2 = codecs.open( YourAcountRootPath+'/encat.txt','r' ,'utf8' )
    text = text2.read().strip()
except:
    wikipedia.output(u"file doesn't exist")
#----------------------------------------------------------------------

text=text.replace(u'\r',u'')
cat_link=text.split(u'\n')    
black_list=[u'_stubs',u'stubs_']
taghi=False
for i in cat_link:
    try:
        if i ==u'America_West_Holdings':#checking
           taghi=True
        if not taghi:
           continue
        wikipedia.output(u'----------------------------------------------------------')
        word_pass=True
        for black_l in black_list:
            if black_l in i:
                word_pass=False
                break
        if word_pass:
            cat_name=u''
            i_page= wikipedia.Page(ensite,i)
            wikipedia.output(i)    
            if Check_Page_Exists(i,ensite):    
                if redirect_find(i):
                    cat_name=u'رده:'+englishdictionry(i,'en','fa')
                    if cat_name.strip()!=u'رده:':
                        if i[-1]==u's' and cat_name[-2:]!=u'ان' and cat_name[-2:]!=u'ها' and cat_name[-1:]!=u'س' and cat_name[-1:]!=u'ز' and cat_name[-2:]!=u'ون' and cat_name[-2:]!=u'ات' and cat_name[-3:]!=u'های':
                            if cat_name in plural_names:
                                cat_name=plural_names[cat_name]
                            extention=u' s_ha'
                        else:
                            extention=u' '
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(extention+u'\t'+cat_name+u'\tCategory:'+i+u'\t'+i,1)
                            wikipedia.output(u'\03{lightgreen}--OK! '+extention+u'---Added: '+i+u' as '+cat_name+u'\03{default}')
                            continue
            else:
                continue
            if len(i)<3:    
                continue
            #wikipedia.output(u'+++1'+i)
            facat=u''
            if i[-3:]==u'ies':
                i_new=i[:-3]+u'y'
                facat=double_check(i_new,True)
                extensions=u'ies'
            elif i[-2:]==u'es':
                i_new=i[:-2]
                facat=double_check(i_new,True)
                extensions=u'es'
            elif i[-1:]==u's' and check_not_decade(i):
                i_new=i[:-1]
                facat=double_check(i_new,True)
                extensions=u's'
            else:
                facat=double_check(i,True)
                i_new=i
                extensions=u''

            if facat:
                    cat_name=u'رده:'+facat
                    if not Check_Page_Exists(cat_name,fasite):
                        save_file(u'<-'+extensions+u'\t'+cat_name+u'\tCategory:'+i+u'\t',1)
                        wikipedia.output(u'\03{lightgreen}<- Added: '+i+u' as '+cat_name+u'\03{default}')
                        continue

            for this_cat in spe_cat_dict:
                cat_len=len(this_cat)
                if i[:cat_len]==this_cat:
                    part_2=i.split(this_cat)[1].strip()
                    fa_part_1=spe_cat_dict[this_cat]
                    if part_2[-3:]=='ies':
                        fa_part_2=double_check(part_2[:-3]+u'y',False)
                    elif part_2[-2:]=='es':
                        fa_part_2=double_check(part_2[:-2],False)
                    elif part_2[-1]=='s' and check_not_decade(part_2):
                        fa_part_2=double_check(part_2[:-1],False)
                    else:
                        fa_part_2=double_check(part_2,False)
                    if fa_part_2:
                        cat_name=u'رده:'+fa_part_1+u' '+fa_part_2
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(u'##3\t'+cat_name+u'\tCategory:'+i+u'\t ',1) 
                            wikipedia.output(u'\03{lightyellow}##3 Added: '+i+u' as '+cat_name+'\03{default}')
                            break

            if cat_name.replace(u'رده:',u'').strip():
                continue
            cat_name=u''
            #wikipedia.output(u'+++3'+i)
            for nash in Nationality:
                cat_len=len(nash)
                if i[:cat_len]==nash:
                    for peop in people_case:
                        if peop in i.lower():
                           peop_case=True
                           break
                        else:
                           peop_case=False

                    part_2=i.split(nash)[1].strip()
                    if string.count(part_2,u'_')>0:
                        firstpart_part_2=part_2.split(u'_')[0]
                        if firstpart_part_2[-1:]==u's' and check_not_decade(firstpart_part_2):
                            plu=True
                        else:
                            plu=False
                        fa_part_2=double_check(part_2,plu)
                    else:
                        firstpart_part_2=part_2
                        if firstpart_part_2[-1:]==u's' and check_not_decade(firstpart_part_2):
                            plu=True
                        else:
                            plu=False
                        if part_2[-3:]=='ies':
                            fa_part_2=double_check(part_2[:-3]+u'y',plu)
                        elif part_2[-2:]=='es':
                            fa_part_2=double_check(part_2[:-2],plu)
                        elif part_2[-1]=='s' and check_not_decade(part_2):
                            fa_part_2=double_check(part_2[:-1],plu)
                        else:
                            fa_part_2=double_check(part_2,plu)
                    backage=u'##4'
                    if string.count(part_2,u'_')>0:
                        backage=u'z##4'
                    if peop_case:
                        fa_part_1=u'اهل '+Nationality[nash]
                        backage=backage+u'-People'
                    else:
                        fa_part_1=Nationality[nash]
                        backage=backage+u'-error'
                    if fa_part_2:
                        if fa_part_2[-1]==u'ا' or fa_part_2[-1]==u'و':
                            fa_part_2+=u'ی'
                            cat_name=u'رده:'+fa_part_2+u' '+fa_part_1
                            if string.count(fa_part_2,u' ')<3:
                                backage='##4-Simple-'+backage
                            if not Check_Page_Exists(cat_name,fasite):
                                save_file(backage+u'+y\t'+cat_name+u'\tCategory:'+i+u'\t ',1)
                        else:
                            cat_name=u'رده:'+fa_part_2+u' '+fa_part_1
                            if string.count(fa_part_2,u' ')<3:
                                backage='##4-Simple-'+backage
                            if not Check_Page_Exists(cat_name,fasite):
                                save_file(backage+u'\t'+cat_name+u'\tCategory:'+i+u'\t ',1)

                        wikipedia.output(u'\03{lightyellow}##4 Added: '+i+u' as '+cat_name+u'\03{default}')    
                        break

            if cat_name.replace(u'رده:',u'').strip():
                continue
            cat_name=u''

            if string.count(i,u'_in_')==1:
                part_1=i.split(u'_in_')[0].strip()
                part_2=i.split(u'_in_')[1].strip()
                fa_part_1=double_check(part_1,True)
                if part_2[-3:]=='ies':
                    fa_part_2=double_check(part_2[:-3]+u'y',False)
                elif part_2[-2:]=='es':
                    fa_part_2=double_check(part_2[:-2],False)
                elif part_2[-1]=='s' and check_not_decade(part_2):
                    fa_part_2=double_check(part_2[:-1],False)
                else:
                    fa_part_2=double_check(part_2,False)
                if fa_part_1 and fa_part_2 and fa_part_1!=part_1 and fa_part_2!=part_2:
                    test_fa_part_1=u' '+fa_part_1
                    for a in u'۰۱۲۳۴۵۶۷۸۹':
                        test_fa_part_1=test_fa_part_1.replace(a,u'')
                    for a in [u'(میلادی)',u'(قمری)',u'(پیش از میلاد)',
                              u'رده:دهه‌های',u'رده:سده‌های',u'رده:هزاره‌های',
                              u'رده:دهه‌ها',u'رده:سده‌ها',u'رده:هزاره',
                              u' سده ',u' دهه ',u'رده:سال‌های'
                              u'اول ',u'دوم ',u'سوم ',u'چهارم ',u'پنجم ',u'ششم ',u'هفتم ',u'هشتم ',u'نهم ',
                              u'دهم ',u'یازدهم ',u'دوازدهم ',u'سیزدهم ',u'چهاردهم ',u'پانزدهم ',u'شانزدهم ',
                              u'هفدهم ',u'هجدهم ',u' نوزدهم ',u' بیستم ',u' بیست و یکم ',    
                              u'رده:']:
                        test_fa_part_1=test_fa_part_1.replace(a,u'')
     
                    if test_fa_part_1.strip():
                        cat_name=u'رده:'+fa_part_1+u' در '+fa_part_2
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(u'@@1\t'+cat_name+u'\tCategory:'+i+u'\t ',1)
                    else:
                        cat_name=u'رده:'+fa_part_2+u' در '+fa_part_1.replace(u'رده:',u'').strip()
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(u'@@2\t'+cat_name+u'\tCategory:'+i+u'\t ',1)
                    wikipedia.output(u'\03{lightred}@@@ Added: '+i+u' as '+cat_name+u'\03{default}')
                    continue

            if string.count(i,u'_of_')==1:
                part_1=i.split(u'_of_')[0].strip()
                part_2=i.split(u'_of_')[1].strip()
                fa_part_1=double_check(part_1,True)
                if part_2[-3:]=='ies':
                    fa_part_2=double_check(part_2[:-3]+u'y',False)
                elif part_2[-2:]=='es':
                    fa_part_2=double_check(part_2[:-2],False)
                elif part_2[-1]=='s' and check_not_decade(part_2):
                    fa_part_2=double_check(part_2[:-1],False)
                else:
                    fa_part_2=double_check(part_2,False)
                if fa_part_1 and fa_part_2 and fa_part_1!=part_1 and fa_part_2!=part_2:
                    if fa_part_1[-1]==u'ا' or fa_part_1[-1]==u'و':
                        cat_name=u'رده:'+fa_part_1+u'ی '+fa_part_2
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(u'##2\t'+cat_name+u'\tCategory:'+i+u'\t ',1)    
                    else:
                        cat_name=u'رده:'+fa_part_1+u' '+fa_part_2
                        if not Check_Page_Exists(cat_name,fasite):
                            save_file(u'##1\t'+cat_name+u'\tCategory:'+i+u'\t ',1) 
                    wikipedia.output(u'\03{lightyellow}### Added: '+i+u' as '+cat_name+u'\03{default}')    
                    continue
    except:
        continue