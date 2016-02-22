#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#step one of ransomenote.py creates a list of favicons based on the webhistory of various browsers on your system
# make sure to select the right paths to your browser's history in faviconfig.py

import sqlite3,os 
import faviconfig, time

ff_db = os.path.join(os.path.expanduser(faviconfig.ff_db_path), 'places.sqlite')

chrome_db = os.path.join(os.path.expanduser(faviconfig.chrome_db_path), 'Favicons')

chromium_db = os.path.join(os.path.expanduser(faviconfig.chromium_db_path), 'Favicons')

browsers = {chrome_db:faviconfig.get_chrome, chromium_db:faviconfig.get_chromium, ff_db:faviconfig.get_ff}

for i in browsers.iteritems():
	if i[1] == 1:
		conn = sqlite3.connect(i[0])
		c = conn.cursor()

		if 'chrom' in i[0]:
			print "Getting favicons from Chrome/ium.."
			time.sleep(2)
			c.execute('SELECT url, id FROM favicons ORDER BY id ASC')
		
		elif 'firefox' in i[0]:
			print "Getting favicons from Firefox.."
			time.sleep(2)
			c.execute("SELECT url, id FROM moz_favicons WHERE mime_type != 'image/x-icon' ORDER BY id ASC")
	

		faviconlist= c.fetchall()

		with open(faviconfig.output_file, 'a') as f:
			for url, row_id in faviconlist:
				print "writing", url
				try:
					f.write('\n')
					f.write(url)
				except:
					print "couldnt write", url
			
print "Done getting favicons\n"
print "Run make_favicon_db.py to continue the process"