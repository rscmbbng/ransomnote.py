#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#allows you to annotate your favicon db. The script will show favicons one by one in the browser and ask for input. If the character is not a letter use the escape character to mark it as such (by default a space).



import os, sqlite3, faviconfig, string, webbrowser

db = faviconfig.favicon_db
ff = faviconfig.favicon_folder

count_max = faviconfig.annotate_num 

conn = sqlite3.connect(db)
cursor = conn.cursor()

browser_location = '/usr/bin/chromium'

all_favicons = cursor.execute("SELECT url, id FROM favicons WHERE done=1 AND letter IS NULL ORDER BY id ASC").fetchall()

escape_character = ' '
allowedsymbols = string.ascii_letters+string.digits+string.punctuation+' '
count = 0

b = webbrowser.get(browser_location)

for favicon, favid in all_favicons:
	if count == int(count_max):
		print "You've annotated", count_max, "entries. Closing programme"
		exit()
	fn, fe = os.path.splitext(favicon)
	fe = fe.split('?')[0]
	ext = str(favid)+fe
	favicon_file = os.path.join(ff,ext)
	b.open(favicon_file)
	print int(count_max)-count, 'favicons to go!'
	print '\n'
	user_input = raw_input('What symbol is this? \n')

	#if user inputs nothing, prompt again
	if user_input not in allowedsymbols:
		print "You need to provide at least one of the allowed symbols:\n"
		print allowedsymbols
		user_input = raw_input('What symbol is this? \n')

	print 'processing answer "'+user_input+'"..'
	print '\n'

	#if user inputs escape character assign NONE value to letter
	if user_input == escape_character:
		cursor.execute("UPDATE favicons SET letter='NONE' WHERE id="+str(favid)+" ")
		conn.commit()

	#if user inputs letter, assign it
	if user_input != escape_character:
		user_input = "'"+user_input+"'"
		cursor.execute("UPDATE favicons SET letter="+user_input+" WHERE id="+str(favid)+" ")
		conn.commit()

	count+=1

def missing_symbols(database, symbols):
	allsymbols=[]
	for symbol in database:
		symbol = symbol[0]
		if symbol != ' ' or symbol != None or symbol != 'NULL':
			allsymbols.append(symbol.encode('UTF-8'))
			if symbol in symbols:
				symbols = symbols.replace(symbol,'')
	allsymbols.sort()
	print 'Total symbols:\n'
	print allsymbols
	print '\n'

	print '\nMissing symbols:'
	print symbols, '\n'

missing_symbols(cursor.execute('SELECT letter FROM favicons WHERE letter IS NOT "NONE" AND letter IS NOT NULL').fetchall(), allowedsymbols)