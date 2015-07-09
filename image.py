#
#   Stores an Image, specifically the URL to the image
#   along with some metadata relating to the series, submitter, and title
#

class image:

    synonymList = {}
    
    def __init__(self, title, url):
        """
        Initializes the image class with the given title and url
        throws an IOError if the url is badly formatted or the title
        could not be parsed
        """

        #create the synonym list if necessary
        if image.synonymList == {}:
            image.setupSynonyms()
            
        # get the file type
        self.imageType = url[url.rfind('.'):]
        self.url = url
        
        #search for the folder title, in square brackets
        if title.find('[') == -1 or title.find(']') == 1:
            # Author didn't add in the source, file under unknown
            self.folderName = 'Unknown'
            self.fileName = title
        else:
            bracketLastIndex = title.rindex(']')
            bracketFirstIndex = title.rindex('[')        
            #get the folder name, which is usually between brackets
            self.removeKeyWords(title[bracketFirstIndex + 1:bracketLastIndex])
            self.simplifyFolder()
            #get the file name, which is everything before and after the brackets
            title = self.removeSpecial(title)        
            self.fileName = title[:bracketFirstIndex - 1] + title[bracketLastIndex + 1:]        
            self.fileName = self.fileName.replace(' ', '_')[:20]
        
        # add on the image type
        self.fileName = self.fileName + self.imageType
    
    def initAsSplit(self, url, folder, file, imgType):
        self.url = url
        self.folderName = folder
        self.fileName = file
        self.imageType = imgType

    def removeSpecial(self, s):
        specials = ['/', '\\','\'','\"',':','*','<','>','|','?', '.','~']
        for c in specials:
            s = s.replace(c,'')
        return s

    def removeKeyWords(self, s):
        keys = ['daily','#','Daily','DAILY']
        for c in keys:
            s = s.replace(c,'')
        # also get rid of numbers, typically found with "Daily #92" or similar
        for i in range(0,10):
            s = s.replace(str(i),'')
        self.folderName = s.strip()

    def simplifyFolder(self):
        # Look for a possible synonym and if found, make that the new folder name
        folder = self.folderName.lower()
        for (key, vals) in image.synonymList.items():
            for s in vals:
                if s == folder:
                    self.folderName = key
                    return

    def setupSynonyms():
        file = open('SynonymList.txt','r')
        fullRead = file.read().splitlines()
        for line in fullRead:
            # seperate the key from the synonyms
            split = line.split(':')
            # trim the newline character from the end
            key = split[0]
            # split up the synonyms
            syns = split[1].split(';')
            image.synonymList[key] = syns
        file.close()
