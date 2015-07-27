#
#   /r/awwnime scraper that gathers images from a specific page, usually the top 100 from today
#
#   NOTE: reddit limits requests to at most 1000 items of anything
#   However, praw will split requests up into 100 item batches
#

import sys
import praw             # Reddit python wrapper
import time             # Used to get the time the image was DL'ed
import urllib           # Used to download images
import urllib.request   # ^^^
from image import image # Custom image class
import os               # Folder operations


# constants for connecting to reddit
PLATFORM = 'windows'
VERSION = '0.5'
APP_ID = 'TopImageScraper'
USERNAME = 'I_Collect_Images'
USER_AGENT = PLATFORM + ':' + APP_ID + ':' + VERSION + 'by /u/' + USERNAME
TOP_FOLDER = 'C:\\Users\\<USER>\\Pictures\\Anime\\Scraped' #removed for Github

#other constants
FILE_TYPES = ['.jpg', '.png']

redditConnection = praw.Reddit(user_agent=USER_AGENT)

# defaults to be changed by the user
subreddit = 'all'
count = 50
includeGifs = False

def setup():
    if len(sys.argv) > 1:
        global subreddit, count, includeGifs
        subreddit = sys.argv[1]
        count = int(sys.argv[2])
        # Temporarily removing this feature
        # includeGifs = sys.argv[3].upper() == 'TRUE'

def testConnection():
    """
    Tests out the connection to reddit by grabbing the
    top 3 submissions in /r/all and displaying their
    URL along with the submitter
    """
    print('------------------------------------')
    print('Testing connection...')
    testSub = redditConnection.get_subreddit('all')
    print('Top 3 submissions in /r/all right now')
    listing = 1
    for submission in testSub.get_hot(limit=3):
        uprint('#' + str(listing) + ': ' + submission.url[:35] + ' posted by: ' + submission.author)
        listing += 1
    print('Test Complete!')
    print('------------------------------------')

def scrapeImages():
    """
    Main entry point to scrape images off the given subreddit
    """
    listings = redditConnection.get_subreddit(subreddit).get_hot(limit=count)
    for idx, submission in enumerate(listings):
        uprint('#'+ str(idx + 1) + ' getting: ' + submission.url[:35] + ' titled: ' + submission.title[:25])
        data = image(submission.title, submission.url)
        if data.imageType != FILE_TYPES[0] and data.imageType != FILE_TYPES[1]:
            print('^ERROR! Could not download the file. No proper extension was given^')
            continue
        path = TOP_FOLDER + '\\' + data.folderName
        os.makedirs(path, exist_ok=True)
        if not os.path.isfile(path + '\\' + data.fileName):            
            urllib.request.urlretrieve(data.url, TOP_FOLDER + '\\' + data.folderName+'\\'+data.fileName)

# http://stackoverflow.com/questions/14630288/unicodeencodeerror-charmap-codec-cant-encode-character-maps-to-undefined
# Unicode print function. This is to ensure that unicode strings in post titles don't break stdout
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

        
if __name__ == "__main__":
    setup()
    #testConnection()
    scrapeImages()
    exit()
