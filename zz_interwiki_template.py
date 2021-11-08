#!/usr/bin/python
# -*- coding: utf-8  -*-
# # Reza (User:yamaha5) 
# Distributed under the terms of the CC-BY-SA 3.0 .
# -*- coding: utf-8 -*-
import pywikibot,os

faSite = pywikibot.Site('fa', 'wikipedia')
titleList={u"en:module:Bananas/testcases":u"module:Bananas/testcases",
u"en:module:Common abbreviations (meta)/data":u"module:Common abbreviations (meta)/data",
u"en:module:Coordinates/testcases":u"module:Coordinates/testcases",
u"en:module:Find sources/links/archive.org/autodoc":u"module:Find sources/links/archive.org/autodoc"}

for fatitle in titleList:
    try:
        fatitle=fatitle.replace(u'الگو:',u'Template:').replace(u'پودمان:',u'Module:').replace(u' ',u'_').replace(u'en:',u'')
        fapage=pywikibot.Page(faSite,fatitle)
        fatext=fapage.get()
        fatext+=u'\n[[en:'+fatitle+u']]'
        fapage.put(fatext,u'ربات:افزودن میان‌ویکی')
        os.system('python /data/project/rezabot/pycore/pwb.py interwikidata -clean -langs:fa -lang:fa -always -create -page:'+fatitle)
    except:
        continue