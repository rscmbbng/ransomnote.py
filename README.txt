ransomenote.py

a set of scripts to produce favicon alphabets!

==building a favicon cypher==
step 1: set the path to your browser in faviconfig.py
step 2: run browser_history.py to extract the favicons from your browser's history
step 3: using make_favicon_db.py make an sqlite3 database to store the favicons
step 4: download all the favicons with download_favicons.py
step 5: (optional) run auto_clean_db.py to remove duplicate images based on similar appearance. Will also remove some false positives though.
step 6: annotate your database by hand, assigning symbols to favicons, using annotate_favicon_db.py
step 7: use print_cypher.py to save your cypher and generate a HTML 'codebook'

optional: to merge multiple annotated favicon dbs made with ransomnote use db_merge.py 

== running ransomnote.py ==

ransomnote.py takes input from stdin and prints to stdout so use it like this:

$ echo 'Hi, how are you?' | python ransomenote.py > output.html

$ cat mysupersecretmessage.txt | python ransomenote.py > output.html