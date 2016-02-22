#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#generates the favicon cypher (favicypher.py) and prints an HTML 'codebook', showing you an overview of favicons assigned to symbols
#usage: $ python print_cypher.py > codebook.html

import os, sqlite3, sys
import faviconfig
db = faviconfig.favicon_db
favicon_cypher = faviconfig.cypher
conn = sqlite3.connect(db)
cursor = conn.cursor()
all_favicons = cursor.execute("SELECT url, letter, id FROM favicons WHERE done=1 AND letter IS NOT NULL ORDER BY letter ASC").fetchall()

codebook = {}
cypher = {}

for url, letter, favid in all_favicons:
	codebook[letter] = []
	cypher[letter] = []
for url, letter, favid in all_favicons:
	codebook[letter].append((url,favid))
	cypher[letter].append(url)

print """
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
</style>
</head>
<body>

"""

for entry in sorted(codebook.items()):
	letter = entry[0]
	urls = entry[1]
	print "<table>"
	print "<tr><b>", letter,"</b>"
	for url, favid in urls:
		print "<td><img src=",url, 'width="16px" height="16px"></img>',favid,'</td>'
	print "</tr>"
	print "</table>"


print """

</body>
</html>

"""
with open(favicon_cypher,'w') as f:
		a = "key = "
		f.write(a+str(cypher))