#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#
# oooo d8b  .oooo.   ooo. .oo.    .oooo.o  .ooooo.  ooo. .oo.  .oo.   
# `888""8P `P  )88b  `888P"Y88b  d88(  "8 d88' `88b `888P"Y88bP"Y88b  
#  888      .oP"888   888   888  `"Y88b.  888   888  888   888   888  
#  888     d8(  888   888   888  o.  )88b 888   888  888   888   888  
# d888b    `Y888""8o o888o o888o 8""888P' `Y8bod8P' o888o o888o o888o 
#                                                                    
#                                                                    
#                                                                    
#                           .                                        
#                         .o8                                        
# ooo. .oo.    .ooooo.  .o888oo  .ooooo.      oo.ooooo.  oooo    ooo 
# `888P"Y88b  d88' `88b   888   d88' `88b      888' `88b  `88.  .8'  
#  888   888  888   888   888   888ooo888      888   888   `88..8'   
#  888   888  888   888   888 . 888    .o .o.  888   888    `888'    
# o888o o888o `Y8bod8P'   "888" `Y8bod8P' Y8P  888bod8P'     .8'     
#                                              888       .o..P'      
#                                             o888o      `Y8P'


# Mask your gpgp-encrypted emails by making them appear like a favicon ransom note using a custom cypher!
# Readable by humans, not by machines. Required pen and paper for decryption.
# Takes a textfile as an input and outputs encrypted.html as output
# Example use: $ echo 'Hi, how are you?' | python ransomenote.py > output.html

# Roel Roscam Abbing
# Initial idea made with Michaela Lakova, Jasper van Loenen during the Blending In workshop by Dave Young at Worm Rotterdam
# http://www.worm.org/home/view/event/8834

import sys, re
from favicypher import key as cypher
from random import randrange

textfile = sys.stdin.read()

def encrypt(cypher, input_text):
		sentences = []
		words = []
		letters = []
		n_character =[]
		n_word = []
		n_words = []
		n_sentence = []
		n_sentences = []

		#regex for finding individual sentences in the text
		pattern = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

		#input_text = open(input_text,'r').read()

			#the regex won't detect a pgp key or '\n' linebreaks
		if input_text.startswith('-----BEGIN PGP PUBLIC KEY BLOCK-----'):
			sentences = input_text.split('\n')
			
		elif '\n' in input_text:
			sentences = input_text.split('\n')
			
		else: # maybe this regex needs to go?
			#a list of all sentences in the text
			sentences = pattern.findall(input_text)
			

		for sentence in sentences: 
			#find all the words + non-words in the current sentence	
			words = re.split('(\W+)', sentence)
			for word in words:
				#for each individual character in the current word, do a replace
				for character in word:
					if character in cypher:
						randint = randrange(0, len(cypher[character]))
						imagetag = '<img src="'+cypher[character][randint]+'"></img>'
						character = imagetag
					#take me out!!!
					else:
						character = character*2
					
					n_word.append(character) #a new word out of a list of characters
				n_words.append(n_word) #a list of new words out of a list of individual words
				n_word =[]
			n_sentence.append(['<p>']+n_words+['</p>'])# a list of new sentences out of individual words
			n_words=[]
		n_sentences.append(n_sentence)#all the sentences in the text
		n_sentence = []

		encrypted_text = ''
		for sentence in n_sentences:
			for words in sentence:
				for word in words:
					for characters in word:
						try:
							encrypted_text = encrypted_text + ''.join(characters)
						except:
							#print 'failed to add', characters
							pass
		print """

<!DOCTYPE html>
<html>
<head>
<style>
img {
    height: 16px;
    width: 16px;
}
</style>
</head>
<body>
		"""#							v this is ugly and should be redone in l.69 -88 but fuckit
		print encrypted_text.replace('<p></p>', "<br>")

		print """

</body>
</html>

		"""

		exit()

encrypt(cypher,textfile)
