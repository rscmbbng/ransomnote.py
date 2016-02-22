#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#tool to merge the uniuqe favicons from one db into another
#usage: $ python db_merge.py myotherdatabase.sqlite3
#takes the db specified in faviconfig as the one that is updated with the unique results from the new one

import os, sqlite3, sys
import faviconfig
db = faviconfig.favicon_db
faviconlistfile = faviconfig.output_file
comparelist = []

db2 = sys.argv[1]

conn = sqlite3.connect(db)
cursor = conn.cursor()

conn2 = sqlite3.connect(db2)
cursor2 = conn2.cursor()

print 'merging favicons from', db2, 'into', db

db_a = dict(cursor.execute('SELECT url, letter FROM favicons WHERE letter IS NOT "NONE" ORDER by rowid DESC').fetchall())
db_b = dict(cursor2.execute('SELECT url, letter FROM favicons WHERE letter IS NOT "NONE" ORDER by rowid DESC').fetchall())


for url in db_b:
	letter = db_b[url]
	if url not in db_a.iterkeys():
		print 'adding', url, 'from', db2, 'to', db
		cursor.execute("""INSERT INTO favicons (url, letter) VALUES(?,?)""", (url, letter))
		conn.commit()

cursor.execute('UPDATE favicons SET id = rowid WHERE id IS NULL')
conn.commit()

print "Done merging", db2, "into", db