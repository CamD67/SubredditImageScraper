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
import urllib.request
from image import image
import os


# constants for connecting to reddit
PLATFORM = 'windows'
VERSION = '0.5'
APP_ID = 'TopImageScraper'
USERNAME = 'I_Collect_Images'
USER_AGENT = PLATFORM + ':' + APP_ID + ':' + VERSION + 'by /u/' + USERNAME
TOP_FOLDER = 'C:\\Users\\<WINDOWS_USER>\\Pictures\\Anime\\Scraped' #removed for Github

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
        includeGifs = sys.argv[3].upper() == 'TRUE'

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
        print('#' + str(listing) + ': ' + submission.url[:35] + ' posted by: ' + submission.author)
        listing += 1
    print('Test Complete!')
    print('------------------------------------')
    
def scrapeImages():
    """
    Main entry point to scrape images off the given subreddit
    """
    listings = redditConnection.get_subreddit(subreddit).get_hot(limit=count)
    for submission in listings:
        print('getting: ' + submission.url[:35] + ' titled: ' + submission.title[:30])
        data = image(submission.title, submission.url)
        if data.imageType != FILE_TYPES[0] and data.imageType != FILE_TYPES[1]:
            print('^ERROR! Could not download the file. No proper extension was given^')
            continue
        path = TOP_FOLDER + '\\' + data.folderName
        os.makedirs(path, exist_ok=True)
        if not os.path.isfile(path + '\\' + data.fileName):            
            urllib.request.urlretrieve(data.url, TOP_FOLDER + '\\' + data.folderName+'\\'+data.fileName)
        
if __name__ == "__main__":
    setup()
    #testConnection()
    scrapeImages()
    exit()
