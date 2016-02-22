#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#step four of ransomenote.py
#uses an algorithm that compares images very similary images to detect multiple instances of the same image
#sometimes this method falsely flags two different images as duplicates, we ignore that
#although this step is not strictly necessary, it will save you a lot of work when annotating images by hand (oh yes, by the way, that happens by hand ;)
#it requires the PIL and imageshash pyhton libraries and is based on https://github.com/JohannesBuchner/imagehash/blob/master/find_similar_images.py

#first makes a list of all non-images (fails)
#then compares all other files to find multiple instances of similar images
#delete all fails, delete all multiples minus one instance
#update the database

#go through the favicon folder to see which favions we actually have
#update the file_path entry in the database based on that
#remove database entries of which we have no filepath

from PIL import Image
import imagehash, os, sqlite3, faviconfig,time

db = faviconfig.favicon_db
ff = faviconfig.favicon_folder

conn = sqlite3.connect(db)
cursor = conn.cursor()

filenames = os.listdir(ff)
images = {}
fails = [] #list of things that aren't images according to PIL
rms = [] #list of duplicates that will be deleted

print 'Cleaning favicons in', ff
time.sleep(1)

for i in filenames:
	i = os.path.join(ff, i)
	#make a dictionary of imagehashes
	try:
		hash = imagehash.average_hash(Image.open(i))
		images[hash] = images.get(hash, []) + [i]

	#will fail if not an image
	except:
		print 'failed for', i,'\n'
		fails.append(i)

multiples = []

#make a list of images with multiple similar ones
for k, image_list in images.iteritems():
	if len(image_list) > 1:
	 	multiples.append(" ".join(image_list))


print len(images), 'unique favicons found.'
print len(fails), 'favicons are not imagefiles.'
time.sleep(2)

#remove the multiples, keep one original instance
for m in multiples:
	i = m.split()
	for a in i:
		orig = i[0]
		fn, fe = os.path.splitext(orig)
		favid = fn.split('/')[1]
		
		if a != orig:
			print 'Removing multiple', a		
			os.system('rm '+a)
			rms.append(a)
			#remove the duplicate image from db
			cursor.execute("DELETE FROM favicons WHERE id = "+str(favid)+"")
			conn.commit() 

		else:
			print 'Keeping', a, 'as an original.' 

#remove all the files PIL couldn't open (aka not images)
for i in fails:
	fn, fe = os.path.splitext(i)
	favid = fn.split('/')[1]
	
	print 'Removing non-image',i
	os.system('rm '+i)
	#also remove them from db
	cursor.execute("DELETE FROM favicons WHERE id = "+str(favid)+"")
	conn.commit() 

print "Updating filepaths in", db
time.sleep(2)

#go through the favicon files we actually have and update the file_path value in the db based on that

f_list = os.listdir(ff)
f_list.sort()

for i in f_list:
	favid, ext = os.path.splitext(i)
	
	sql_string = ("UPDATE favicons SET file_path=\'{0}\' WHERE id={1} AND file_path IS NULL").format(i, favid) #dat ' escape 
	#print sql_string
	cursor.execute(sql_string)

	conn.commit()
	print "Updated filepath entry of", i, "in", db

# proceed to delete the rows which have no file_path (means it was either a duplicate or failed to dload earlier on)
time.sleep(2)
print "Removing rows in db without a file path"
cursor.execute("DELETE FROM favicons WHERE file_path IS NULL")
conn.commit()

print "Removed all duplicated favicons, now annotate the rest using annotate_favicon_db.py"