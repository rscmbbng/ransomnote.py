#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#step three of ransomnote.py
#goes through all favicons that have ben added to the favicon_db
#tries to download them into a folder specified in faviconfig.py
#marks the entry as 'done' in db (means you can stop downlading and continue later)
#if download fails for any reason (such as expired link), removes the entry from db

import os,sqlite3,sys
from urlparse import urlparse
import urllib, urllib2, os, faviconfig

db = faviconfig.favicon_db
ff = faviconfig.favicon_folder
conn = sqlite3.connect(db)
cursor = conn.cursor()

all_favicons = cursor.execute('SELECT url, id, done FROM favicons ORDER BY id ASC').fetchall()

if not os.path.exists(ff):
	os.mkdir(ff)
else:
	pass

for favicon, favid, done in all_favicons:
	fn, fe = os.path.splitext(favicon) #split in 'filename' and extension
	
	if done != 1: #check if favicon is already marked as downloaded
		try:
			fe = fe.split('?')[0] #filter out all the php? arguments that might be in a filename

			try: #download the file
				f = urllib2.urlopen(favicon, timeout=10)
				with open(ff+'/'+str(favid)+fe,'wb') as output:
					output.write(f.read())

				print 'downloaded', favicon, 'as', ff+'/'+str(favid)+fe
				
				#mark the file as downloaded in database
				cursor.execute("UPDATE favicons SET done = 1 WHERE id = "+str(favid)+"")
				conn.commit() 


			except urllib2.HTTPError, e:
				print 'failed to download', favicon, '\n'
				print e.code, e.msg

				#delete missing or forbidden favicons from db
				print 'deleting', favid, 'from db'
				cursor.execute("DELETE FROM favicons WHERE id = "+str(favid)+"")					
				conn.commit()


		except:
			pass
	else:
		print 'already have', favicon


print "Done downloading the favicons \n"
print "Run auto_clean_db.py to algorithmically sift through similar favicons"
print "Or run annotate_favicon_db.py to annotate the database"