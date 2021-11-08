# -*- coding: utf-8 -*-
#
#http://dumps.wikimedia.your.org/fawiki/
#http://dumps.wikimedia.your.org/fawiki/20150325/fawiki-20150325-pages-meta-current.xml.bz2

#urllinkmain =u'https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2'
import  xmlreader, codecs
import os
data_d=u'\n'
bot_adress="/data/project/rezabot/"
TheDay='latest'

urllinkmain='http://dumps.wikimedia.your.org/fawiki/%s/fawiki-%s-pages-meta-current.xml.bz2' %(TheDay,TheDay)
#urllinkmain =u'https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2'
print urllinkmain
os.system('wget '+urllinkmain +" "+bot_adress+"fawiki-latest-pages-meta-current.xml.bz2")
dump = xmlreader.XmlDump(bot_adress+"pywikipedia/fawiki-latest-pages-meta-current.xml.bz2")

pre,noinclude,includeonly,tags1,tags2=u'\n',u'\n',u'\n',u'\n',u'\n'
for entry in dump.new_parse():
    box_text=u''
    if entry.ns =='10':
        text=entry.text.replace(u'\r',u'').replace(u' /',u'/').replace(u'/ ',u'/').replace(u'< ',u'<').replace(u' >',u'>')
        if u'}}\n<noinclude' in text or u'}}\n\n<noinclude' in text:
            data_d+=entry.title+u'\n'
            print entry.title
with codecs.open(bot_adress+u'zz_tempfind.txt' ,mode = 'w',encoding = 'utf8' ) as f:
    f.write(data_d)
