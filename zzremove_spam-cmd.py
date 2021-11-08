#!/usr/bin/python
# -*- coding: utf-8  -*-
# Distributed under the terms of the CC-BY-SA 3.0 .
# Reza (User:yamaha5) 

import wikipedia,query,re,codecs,login
faSite = wikipedia.getSite('fa')
wikipedia.config.put_throttle = 0
wikipedia.put_throttle.setDelay()
import sys
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

def get_url(my_url,ns):
    dict={}
    my_url=my_url.replace(u' ',u'_')
    params = {
        'action': 'query',
        'list': 'exturlusage',
        'euquery': my_url,
        'eulimit':500,
    }
    Url_list = query.GetData(params,faSite)
    wikipedia.output(u'>>>'+my_url)
    #wikipedia.output(u'>>>'+str(Url_list))
    if u'query' in str(Url_list) and u'exturlusage' in str(Url_list):
        for item in Url_list[u'query'][u'exturlusage']:
            Title=item[u'title']
            adress=item[u'url']
            if ns==1000:
                if item[u'ns']!=4:
                    dict[Title]=adress
            if ns==0:
                if item[u'ns']==0:
                    dict[Title]=adress
    return dict

def remove_link(title,urls,notremoved,UserName,bmsg):
    wikipedia.output(u'\03{lightyellow}---------'+title+u'---------\03{default}')
    fapage=wikipedia.Page(faSite,title)
    the_list=[urls,urls.replace(ur'http://',u''),urls.replace(ur'https://',u''),urls.replace(ur'https://',ur'http://'),urls.replace(ur'http://',ur'https://')]
    the_list=list(set(the_list))
    for url in the_list:
        try:
           fa_txt=fapage.get().replace(u'\r','').replace(u' '+url,url).replace(url+u' ',url).replace(u' '+url,url).replace(url+u' ',url)
        except:
            continue
        fa_txt=fa_txt.replace(u'\n*',u'\n* ').replace(u'\n*  ',u'\n* ').replace(u'\n#',u'\n# ').replace(u'\n#  ',u'\n# ')
        fa_txt_old=fa_txt
        fa_txt=fa_txt.replace(u'{{URL|example.com}}',u'')
        if url.split('/')[0].strip():
            fa_txt=re.sub(ur'<ref(?:[^\>\<]+)?>(?:[^\<\>]+)'+url.split('/')[0].strip().replace(u'-',u'\-').replace(u'.',u'\.')+ur'(?:[^\<\>]+)\<\/ref\>',u'',fa_txt)
        fa_txt=fa_txt.replace(u'<ref>'+url+ur'</ref>',u'')
        if u'['+url in fa_txt:
            our_link=u'['+url+fa_txt.split(u'['+url)[1].split(u']')[0]+u']'
            wikipedia.output(our_link+u'----------------')
            fa_txt=fa_txt.replace(u'\n* '+our_link+u'\n',u'\n').replace(u'\n* '+our_link,u'\n').replace(u'\n# '+our_link,u'\n').replace(u'* '+our_link+u'\n',u'\n').replace(u'\n# '+our_link+u'\n',u'\n').replace(u'('+our_link+u')',u'').replace(our_link+u'\n',u'\n').replace(our_link,u'')
            fa_txt=fa_txt.replace(u'[]',u'').replace(u'[ ]',u'')

        elif u'|'+url+u'}' in fa_txt:
            fa_txt=fa_txt.replace(u'|'+url+u'}',u'|}')
        elif u'\n'+url in fa_txt:
            fa_txt=fa_txt.replace(u'\n'+url,u'\n')
        elif url+u'\n' in fa_txt:
            fa_txt=fa_txt.replace(url+u'\n',u'\n')
        elif u'|'+url+u'|' in fa_txt:
            fa_txt=fa_txt.replace(u'|'+url+u'|',u'| |')
        elif u'{'+url+u'|' in fa_txt:
            fa_txt=fa_txt.replace(u'{'+url+u'|',u'{ |')
        elif u'{'+url+u'}' in fa_txt:
            fa_txt=fa_txt.replace(u'{'+url+u'}',u'')
        elif u'\n* '+url+u'\n' in fa_txt:
            fa_txt=fa_txt.replace(u'\n* '+url+u'\n',u'\n').replace(u'\n* '+url+u' ',u'\n')
        elif u'\n# '+url+u'\n' in fa_txt:
            fa_txt=fa_txt.replace(u'\n# '+url+u'\n',u'\n').replace(u'\n# '+url+u' ',u'\n')
        elif u'='+url in fa_txt:
            fa_txt=fa_txt.replace(u'='+url,u'=')
        elif url in fa_txt:
            wikipedia.output(u'\03{lightred}Page ='+title+u' is difficult Url='+url+u'\03{default}')
        else:
            wikipedia.output(u'\03{lightblue}Some thing is wrong the page does not have Url\03{default}')
        if fa_txt!=fa_txt_old:
            fa_txt=fa_txt.replace(u'\n#  ',u'\n# ').replace(u'\n*  ',u'\n* ').replace(u'\n* \n',u'\n').replace(u'\n# \n',u'\n').replace(u'<ref></ref>',u'').replace(u'<ref> </ref>',u'').replace(u'<ref>    </ref>',u'').replace(u'<ref>   </ref>',u'').replace(u'<ref>  </ref>',u'').replace(u'<ref> \n </ref>',u'').replace(u'<ref>\n </ref>',u'').replace(u'<ref>  \n</ref>',u'').replace(u'<ref> \n</ref>',u'').replace(u'<ref>\n</ref>',u'').replace(u'<ref>\n\n</ref>',u'')
            try:
                fapage.put(fa_txt,bmsg)
            except:
                addtolist=u'\n# [['+title+u']] > ['+url+u']'
                if not addtolist in notremoved:
                    notremoved=notremoved+addtolist
                pass
        else:
            wikipedia.output(u'\03{lightred}Bot could not remove the link! Page ='+title+u' is difficult Url='+url+u'\03{default}')
            addtolist=u'\n# [['+title+u']] > ['+url+u']'
            if not addtolist in notremoved:
                notremoved=notremoved+addtolist
    return notremoved
def main_r(UserName,bmsg):
    fapage=wikipedia.Page(faSite,u'مدیاویکی:Spam-blacklist')
    Black_text=fapage.get().replace(u'\r',u'')

    metaSite = wikipedia.getSite('meta',fam='meta')
    metapage=wikipedia.Page(metaSite,u'Spam_blacklist')
    Black_text2=metapage.get().replace(u'\r',u'')
    Black_text+=u'\n'+Black_text2

    notremoved=u'\n'
    for line in Black_text.split(u'\n'):
        if u'#' in line or u'{' in line or u'[' in line or u'<' in line or u'>' in line:
            continue
        my_url=line.replace(u'\\b',u'').replace(u"\\",u"").replace(u"\:",u":").replace(u"\.",u".")
        dict=get_url(my_url,1000)
        for title in dict:
            notremoved=remove_link(title,dict[title],notremoved,UserName,bmsg)

    with codecs.open(u'Spam_list.txt' ,mode = 'w',encoding = 'utf8' ) as f:
        f.write(notremoved)

faname=unicode(sys.argv[1],'UTF-8')
UserName=unicode(sys.argv[2],'UTF-8')
login_wiki()

if faname==u'spamlist':
    bmsg=u'ربات:حذف نشانی‌های موجود در [[مدیاویکی:Spam-blacklist]] یا [[:meta:pam_blacklist]] یا نشانی اسپم'      
    main_r(UserName,bmsg)
else:
    bmsg=u'ربات:حذف نشانی اسپم (به درخواست [['+UserName+u']])'
    dict=get_url(faname,1000)
    for title in dict:
        notremoved=remove_link(title,dict[title],notremoved,UserName,bmsg)