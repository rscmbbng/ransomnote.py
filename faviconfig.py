#favicon config
#configure paths and folders for the ransomenote.py toolchain


#  ______ _          ______        
# |  ____(_)        |  ____|       
# | |__   _ _ __ ___| |__ _____  __
# |  __| | | '__/ _ \  __/ _ \ \/ /
# | |    | | | |  __/ | | (_) >  < 
# |_|    |_|_|  \___|_|  \___/_/\_\ specific settings

ff_db_path = '~/.mozilla/firefox/9645shj6.default/'

#set the path to your mozilla profile
#for more info: http://kb.mozillazine.org/Profile_folder_-_Firefox

#on GNU/LINUX it can be found in:
# ~/.mozilla/firefox/<profile folder>/places.sqlite

#on Mac OSX it can be found in:
# ~/Library/Application Support/Firefox/Profiles/<profile folder>
# ~/Library/Mozilla/Firefox/Profiles/<profile folder> 

#   _____ _                               ___               __  
#  / ____| |                             / (_)              \ \ 
# | |    | |__  _ __ ___  _ __ ___   ___| | _ _   _ _ __ ___ | |
# | |    | '_ \| '__/ _ \| '_ ` _ \ / _ \ || | | | | '_ ` _ \| |
# | |____| | | | | | (_) | | | | | |  __/ || | |_| | | | | | | |
#  \_____|_| |_|_|  \___/|_| |_| |_|\___| ||_|\__,_|_| |_| |_| | specific settings
#                                        \_\                /_/ 
                                                              

chrome_db_path = '~/.config/google-chrome/Default/'
chromium_db_path = '~/.config/chromium/Default/'
#osx chrome:
#chrome_db_path = '~/Library/Application Support/Google/Chrome/Default/'
#osx chromium: 
#chromium_db_path = '~/Library/Application Support/Chromium/Default/'


#Set which browser histories to get, use 0 to skip.
get_ff = 1
get_chrome = 0
get_chromium = 1

#write the list of favicons to a file
output_file = 'faviconlist_clean.txt'

#the database which we will use and populate
favicon_db = 'favicondb.sqlite'

#the folder where we store downloaded favicons:
favicon_folder = 'favicon_collection'

#when doing the annotation, how many do you want to annotate per session?
annotate_num = 100

cypher = "favicypher.py"
