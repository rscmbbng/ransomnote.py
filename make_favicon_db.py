#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#step two of ransomenote.py
#creates a sqlite database which is populated with the urls of the favicons
#it will assign a numerical id to each unique favicon url
#this db can be updated by first running browser_history.py and then running this script again


import os, sqlite3, sys
import faviconfig
db = faviconfig.favicon_db
faviconlistfile = faviconfig.output_file
comparelist = []
#make new db with tables
if not os.path.exists(db):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute('CREATE TABLE favicons (url TEXT, id INTEGER, letter TEXT, file_path TEXT, done BOOLEAN)')
	count = 0
#or if it already exists connect to it and get the current count from it.
else:
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		count = int(cursor.execute('SELECT id FROM favicons ORDER BY id DESC').fetchone()[0])
	except:
		count =0
#produce a list see which favicons are already in that database
existing_icons = cursor.execute('SELECT url from favicons').fetchall()
for icon in existing_icons:
	comparelist.append(icon[0].encode('UTF-8'))

for a in open(faviconlistfile).readlines():
	letter = None
	#for list with linebreak input
	##########################
	url = a.replace('\n','')
	##########################
	if url not in comparelist:
		try:
			cursor.execute("""INSERT INTO favicons (url, id, letter, done) VALUES(?,?,?,?)""", (url, int(count), letter, False))
			conn.commit()
			print "Added", url, "to", db
		except:
			print "Couldn't add", url, "to", db
			pass
		count+=1

print "\nDone generating a sqlite database of favicons"
print "Run download_favicons.py next to download them to a local folder called", faviconfig.favicon_folder
