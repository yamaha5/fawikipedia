#!/usr/bin/python
# -*- coding: utf-8  -*-
# # Reza (User:yamaha5) , 2014
# Distributed under the terms of MIT License (MIT)
import pywikibot,re,codecs
from pywikibot.compat import query
pywikibot.config.put_throttle = 0
pywikibot.config.maxthrottle = 0
bot_version='۴.۰'
_cache={}
def translation(firstsite,secondsite,enlink):
    if _cache.get(tuple([enlink, firstsite,enlink, 'translation_en'])):
        return _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]
    try:
        enlink=unicode(str(enlink),'UTF-8').replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    except:
        enlink=enlink.replace('[[','').replace(']]','').replace('en:','').replace('fa:','')
    if enlink.find('#')!=-1:
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False
    if enlink=='':
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False    
    enlink=enlink.replace(' ','_')
    site = pywikibot.Site(firstsite)
    sitesecond= pywikibot.Site(secondsite)

    try:
        categoryname = pywikibot.data.api.Request(site=site, action="query", prop="langlinks",titles=enlink,redirects=1,lllimit=500)
        categoryname=categoryname.submit()

        for item in categoryname['query']['pages']:
            case=categoryname['query']['pages'][item]['langlinks']
        for item in case:
            if item['lang']==secondsite:
                intersec=item['*']
                break
        result=intersec
        if result.find('#')!=-1:
            _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
            return False
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=result
        return result
    except:
        _cache[tuple([enlink, firstsite,enlink, 'translation_en'])]=False
        return False

def Solve_linke_translation(fa_link,num):
    if num==1:#link is persian
        en_link=translation('fa','en',fa_link)
        if en_link:
            return '[['+fa_link+'|'+en_link+']]'
        else:
            return '[['+fa_link+']]'

    if num==2:#link is english
        en_link=fa_link
        fa_link=translation('en','fa',en_link)

        if fa_link:
            return '[['+fa_link+'|'+en_link+']]'
        else:
            return '[['+en_link+']]'

def Check_link(fa_link):
    fa_link=fa_link.split('|')[0].replace('[[','').replace(']]','')
    fa_link_2 = re.sub(r'[ءاآأإئؤبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهييك]', r'',fa_link)
    if fa_link_2!=fa_link:
        #pywikibot.output('The link '+fa_link+' is persian!')
        return fa_link,1
    else:
        #pywikibot.output('The link '+fa_link+' is english!')
        return fa_link,2

def check_ref_title_is_english(my_ref):
    my_ref_3=my_ref.replace('= ','=').replace(' =','=').replace('{{ ','{{').replace(' }}','}}').replace('\r','').replace('\n','').replace(' |','|').replace('| ','|').replace('  ',' ').replace('  ',' ').replace('  ',' ')
    if '{{یادکرد' in my_ref_3:
        for item in ['|عنوان','|نویسنده','|کتاب','|نام=','|نام خانوادگی=','|مقاله','|ک=','|ف=','|اثر']:
            if item in my_ref_3:
                ref_title=my_ref_3.split(item)[1].split('|')[0].strip()
                ref_title_2 = re.sub(r'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', r"",ref_title)
                if ref_title_2!=ref_title:
                    #pywikibot.output('!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                    return False
                if ref_title.replace('=','').strip():
                    break
        return True
    elif ('{{Cit' in my_ref_3) or ('{{cit' in my_ref_3):
        for item in ['|title','|first','|last','|work','|contribution','|publisher']:
            if item in my_ref_3:
                ref_title=my_ref_3.split(item)[1].split('|')[0].strip()
                ref_title_2 = re.sub(r'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', r"",ref_title)
                if ref_title_2!=ref_title:
                    #pywikibot.output('!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                    return False
                if ref_title.replace('=','').strip():
                    break
        return True
    else:
        my_ref_3=my_ref_3.replace('[[','@1@').replace(']]','@2@')
        if '[' in my_ref_3:
            my_url=my_ref_3.split('[')[1].split(']')[0]
            if ' ' in my_url:
                my_url_title=my_url.split(' ')[1]
                my_url_title_2 = re.sub(r'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', r"",my_url_title)
                if my_url_title_2!=my_url_title:
                     #pywikibot.output('!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                     return False
            else:
                #pywikibot.output('!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                return False
        else:
            my_ref_3= re.sub(r'\@1\@.*?\@2\@', r"",my_ref_3)
            my_ref_3_2 = re.sub(r'[ضصثقفغعهخحشسيبلاتنمظطزرذدپوکگجچژ]', r"",my_ref_3)
            if my_ref_3_2!=my_ref_3:
                #pywikibot.output('!!!!!\03{lightblue}Title is persian so the links should be persian\03{default}')
                return False
    return True
def get_cite_template(backage,test_text,text_refs):
        test_text=test_text.replace('{{ Cit','{{Cit').replace('{{ cit','{{cit').replace('{{ یادکرد','{{یادکرد')
        if  '{{Cit' in test_text:
            text_refs_2=test_text.split('{{Cit')
            for i in  text_refs_2:
               i='{{Cit'+i.split('}}')[0]
               text_refs.append(i)
            backage='}}'

        if  '{{cit' in test_text:
            text_refs_2=test_text.split('{{cit')
            for i in  text_refs_2:
               i='{{cit'+i.split('}}')[0]
               text_refs.append(i)
            backage='}}'

        if  '{{یادکرد' in test_text:
            text_refs_2=test_text.split('{{یادکرد')
            for i in  text_refs_2:
               i='{{یادکرد'+i.split('}}')[0]
               text_refs.append(i)
            backage='}}'
        return backage,text_refs

def run (text,sum,text2):
    old_text=text
    old_text2=text2
    yes=False
    text_refs=[]
    text2=text2.replace('< ref','<ref').replace('< /ref','</ref').replace('</ ref','</ref').replace('ref >','ref>')
    test_text=text2.replace('<ref name=','@').replace('<references group=','@').replace('<ref group=','@')
    text_refs=test_text.split('<ref')
    backage='</ref>'
    if text_refs[0]==test_text:
        backage,text_refs=get_cite_template(backage,test_text,text_refs)

    count=0
    for refs in text_refs:
        count+=1
        if count==1:
           continue
        my_ref=refs.split(backage)[0]
        if my_ref!=refs:
            should_english=check_ref_title_is_english(my_ref)
            if should_english:
                #pywikibot.output('\03{lightblue}-------ref--------\03{default}'+str(count))
                #pywikibot.output(my_ref)
                #pywikibot.output('>>>>>\03{lightred}Title is english so the links should be english\03{default}')
                RE=re.compile(r'\[\[.*?\]\]')
                fa_links=RE.findall(my_ref)
                if fa_links:
                    #pywikibot.output('----links----')
                    for fa_link in fa_links:
                        fa_link_r,num=Check_link(fa_link)
                        if fa_link_r:
                            new_link=Solve_linke_translation(fa_link_r,num)
                            new_refs=refs.replace('[['+fa_link_r+']]',new_link)
                            old_text=old_text.replace(refs,new_refs)
                            old_text2=old_text2.replace(refs,new_refs)
                            refs=new_refs

                    else:
                        #pywikibot.output('It doesnt have any wiki link!')
                        continue
    if old_text2!=text2:
        return old_text,sum+'+'+'اصلاح ارجاع لاتین'
    else:
        return text,sum

def main(text,sum):
    sum2='اصلاح ارجاع لاتین'
    #The first time
    new_text,sum=run(text,sum,text)
    #The second time
    new_text_2=new_text.replace('< ref','<ref').replace('< /ref','</ref').replace('</ ref','</ref').replace('ref >','ref>')
    new_text_2=new_text_2.replace('<ref name=','@').replace('<references group=','@').replace('<ref group=','@')
    text_refs_2=new_text_2.split('<ref')
    for i in text_refs_2:
        i=i.split('</ref>')[0]
        new_text_2=new_text_2.replace(i,'').replace('<ref','').replace('</ref','')
    new_text,sum2=run(new_text,sum,new_text_2)
    if sum:
       sum2=sum
    return new_text,sum2

if __name__ == "__main__":
    sum=''
    PageTitle =raw_input('Page name > ').decode('utf-8')
    faSite=pywikibot.Site('fa',fam='wikipedia')
    fapage=pywikibot.Page(faSite,PageTitle)
    text=fapage.get()

    new_text,sum2=main(text,sum)

    if text!=new_text:
        fapage.put(new_text,'ربات:اصلاح پیوندهای ارجاع لاتین')
        pywikibot.output("\03{lightgreen}Links of the page are updated!\03{default}")
    else:
        pywikibot.output("This Page doesn't need any change")
