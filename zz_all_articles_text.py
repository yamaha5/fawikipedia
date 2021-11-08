# -*- coding: utf-8 -*-
#
#http://dumps.wikimedia.your.org/fawiki/
#http://dumps.wikimedia.your.org/fawiki/20150325/fawiki-20150325-pages-meta-current.xml.bz2

#urllinkmain =u'https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2'
import codecs, re,string
import pickle
from pywikibot import xmlreader
import os
data_d,data_o,data_s,data_b=u'\n',u'\n',u'\n',u'\n'
bot_adress="/data/project/rezabot/"

urllinkmain =u'https://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2'

#os.system('wget '+urllinkmain +" "+bot_adress+"fawiki-latest-pages-articles.xml.bz2")
dump = xmlreader.XmlDump(bot_adress+"pycore/fawiki-latest-pages-articles.xml.bz2")
text=' '
for entry in dump.parse():
    if entry.ns =='0':
       text+='\n@@@\n'+entry.text
'''
with open('all_articles.pickle', 'wb') as handle:
    pickle.dump(text, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
#os.system('zip %sall_articles.zip %sall_articles.pickle'% (bot_adress,bot_adress))
'''
with codecs.open(bot_adress+u'all_articles.txt' ,mode = 'w',encoding = 'utf8' ) as f:
    f.write(text)
os.system('zip %sall_atricles_text.zip %sall_articles.txt'% (bot_adress,bot_adress))