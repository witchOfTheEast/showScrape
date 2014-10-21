import os, urllib2, re
compiled_list = []
compiled_dict = {} 
showObjects = [] # list of show objects to iterate through, search for titles that are not marked found, update the ep number then they are found, mark them unfound
showDict = {} # dictionary of episode numbers by title
siteData = [] 
matchList = []

def printList(_list):
    for i in range(len(_list)):
        print _list[i]

def printDict(dictionary):
    print ""
    print "dict: ", dictionary.items()
 
def getFilePath(fileName):
    """Acquire the absolute path for the desired file"""
    script_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.join(script_dir, os.pardir)
    rel_path_file = "data/"
    abs_file_path = os.path.abspath(os.path.join(parent_dir, rel_path_file, fileName))
    return abs_file_path

def getDirectoryPath(desiredDirectory):
    """Acquire the absolute path for the desired directory"""
    script_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.join(script_dir, os.pardir)
    abs_dir_path = os.path.abspath(os.path.join(parent_dir, desiredDirectory))
    return abs_dir_path

def makeDict(suppliedFile):
    """Take the data/<fileName> file and complies a title/epiNum dictionary"""
    try:
        with open(suppliedFile) as f:
            for line in f:
                lineItems = line.split()
                title, episode = lineItems[0], int(lineItems[1])
                compiled_dict[title] = int(episode)
        f.close()
        return compiled_dict

    except IOError:
        print "%s was not found. Check your data location." % suppliedFile
        exit(1)

def genShowObjects(suppliedFile):
    """Take data/<filename> and compile showEpisode objects"""
    try:
        with open(suppliedFile) as f:
            for line in f:
                lineItems = line.split()
                try:
                    lineItems[2]

                except IndexError:
                    lineItems.append(lineItems[1])
                    lineItems[1] = '00'

                for i in range(1, 3):
                    if len(lineItems[i]) < 2:
                        lineItems[i] = '0' + lineItems[i]
                
                # if these aren't integers they probably break the original
                # search method
                title, seasonNum, episodeNum = lineItems[0], lineItems[1], lineItems[2]
                
                listValue = showEpisode(title, episodeNum, seasonNum) 
                
                showObjects.append(listValue)

        f.close()

    except IOError:
        print "%s was not found. Check your data location." % suppliedFile
        exit(1)

def makeList(suppliedFile):
    """Makes a list from data/<fileName>""" 
    # i should used title1.title2
    # additionally adding seasons to the showlist
    try:
        with open(suppliedFile) as f:
            for line in f:
                lineItems = line.strip('\n')
                compiled_list.append(lineItems)
        f.close
        return compiled_list
    
    except IOError:
        print "%s was not found. Check your data location." % suppliedFile
        exit(1)

class showEpisode(object):
    def __init__(self, title, episodeNum, seasonNum=None):
        self.title = title
        self.episodeNum = episodeNum
        self.seasonNum = seasonNum
        self.downloadLink = None
        self.acquired = False

                
    def processMatch(self, matchCheck):
        
        if matchCheck:

            self.downloadLink = matchCheck.group(0)
            #updateShowDict(title, showDict)

        else:
            print ""
            print "No MATCH for %s S%sE%s yet" % (self.title, self.seasonNum,
                self.episodeNum)
            print ""

    def applyRegEx(self, dataToTest):
            """Apply the regEx to the title:episode combo, return a match object"""
            regEx = re.compile(r"""
                magnet# beginning of magnet link
                .*# anything until title
                %s# title
                .*?S# match the rest of the title up to S
                %sE%s# season number and episode number
                .*?# anything until the end of the link, made ungreedy by the '?'
                (?=")
                """ % (self.title, self.seasonNum, self.episodeNum), re.VERBOSE
                    | re.IGNORECASE)
            matchCheck = regEx.search(dataToTest)
            return matchCheck
        
    def updateFound(self):
        self.acquired = True
        self.episodeNum = int(self.episodeNum) + 1

def getAllData(siteList):
    """Acquire site data from each URL in a list"""
    for url in siteList:
        user_agent = "" # fill this in 
        request = urllib2.Request(url)    
        response = urllib2.urlopen(request)
        tempData = response.read() # make sure to change this to read()
        siteData.append(tempData)
        return siteData

def getSomeData(url):
    """Acquire site data from single supplied URL"""
    user_agent = "" # fill this in 
    request = urllib2.Request(url)    
    response = urllib2.urlopen(request)
    tempData = response.read() # make sure to change this to read()
    return tempData 

def temp_getSiteData(siteList):
    """FOR TESTING: Acquire site data from each URL in a list"""
    for i in range(1):
        user_agent = "" # fill this in 
        request = urllib2.Request(siteList[1])    
        response = urllib2.urlopen(request)
        tempData = response.read()
        siteData.append(tempData)
        return tempData

def writeOutLinks(suppliedFile):
    """Write the magnet links out to a file to be read by a bittorrent program"""
    for i in range(len(showObjects)):
        if showObjects[i].downloadLink == None:
            pass

        elif showObjects[i].downloadLink != None:
            print ""
            print "Writing link file for %s S%sE%s" % (showObjects[i].title,
                showObjects[i].seasonNum, showObjects[i].episodeNum)
            
            ## to write links into one file
            #with open(suppliedFile, 'a') as f:
            #    f.write(showObjects[i].downloadLink +'\n')
            #    f.close()
            
            ## to write out individual link files
            
            dataDir = getDirectoryPath("data/")
            
            abs_file_path = os.path.join(dataDir, "magnets",
                showObjects[i].title + ".S" + showObjects[i].seasonNum + "E" +
                showObjects[i].episodeNum + ".magnet")
            
            with open(abs_file_path, 'w') as f:
                f.write(showObjects[i].downloadLink +'\n')
                f.close()
            
            showObjects[i].updateFound()

def writeOutShowFile():
    dataDir = getDirectoryPath("data/")
    abs_file_path = os.path.join(dataDir, 'showList')
    
    with open(abs_file_path, 'w') as f:
        for i in range(len(showObjects)):
            title = showObjects[i].title
            season = showObjects[i].seasonNum
            episode = showObjects[i].episodeNum
            fileEntry = "%s %s %s\n" % (title, season, episode)
            f.write(fileEntry)
        f.close()

def searchForShows(data):
    for idata in range(len(data)):
        for i in range(len(showObjects)):
            
            if showObjects[i].acquired == False:
                showObjects[i].processMatch(showObjects[i].applyRegEx(data[idata]))
            else:
                print "%s already FOUND" % showObjects[i].title

def searchForShowsByUrlSearch():
    for i in range(len(showObjects)):
        url = makeSearchUrl(showObjects[i])
        data = getSomeData(url)
        searchData = showObjects[i].applyRegEx(data)
        showObjects[i].processMatch(searchData)

def makeSearchUrl(whichShow):
    """Return single url with title/season/episode inserted"""
    # pattern is TITLE%20S##E##/0/7/0
    searchUrl = '' 
    baseUrl = "http://thepiratebay.se/search/%s%%20S%sE%s/0/7/0"
    baseUrl2 = "http://thepiratebay.se/search/%s%%20E%s/0/7/0"
     
    if whichShow.seasonNum == '00':
        compositeUrl = baseUrl2 % (whichShow.title, whichShow.episodeNum)
    else:
        compositeUrl = baseUrl % (whichShow.title, whichShow.seasonNum,
            whichShow.episodeNum)
    
    return compositeUrl 

def makeUrlSearchList():
    """Make a list of urls with title/episodes inserted"""
    # pattern is TITLE%20S##E##/0/7/0
    searchUrlList = []
    baseUrl = "http://thepiratebay.se/search/%s%%20S%sE%s/0/7/0"
    baseUrl2 = "http://thepiratebay.se/search/%s%%20E%s/0/7/0"
     
    for i in range(len(showObjects)):
        if showObjects[i].seasonNum == '00':
            compositeUrl = baseUrl2 % (showObjects[i].title, showObjects[i].episodeNum)
        else:
            compositeUrl = baseUrl % (showObjects[i].title,
                showObjects[i].seasonNum, showObjects[i].episodeNum)
        
        searchUrlList.append(compositeUrl)

    return searchUrlList

def whatDo():
    """Execute all the things"""
    showListFile = getFilePath('showList')
    urlListFile = getFilePath('urlList')
    matchListFile = getFilePath('matchList.magnet')
    showDict = makeDict(showListFile)
    urlList = makeList(urlListFile)
    genShowObjects(showListFile)
    searchForShowsByUrlSearch()

    #urlSearchList = makeUrlSearchList()
    #data = getAllData(urlList)
    #data = getAllData(urlSearchList)
    #searchForShows(data) # change to variable data for real life
    
    writeOutLinks(matchListFile)
    writeOutShowFile()    

whatDo()


