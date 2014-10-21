superTestData="""


v class="detName">          <a href="/torrent/11157514/Doctor.Who.2005.8x07.Kill.The.Moon.720p.HDTV.x264-FoV[rartv]" class="detLink" title="Details for Doctor.Who.2005.8x07.Kill.The.Moon.720p.HDTV.x264-FoV[rartv]">Doctor.Who.2005.8x07.Kill.The.Moon.720p.HDTV.x264-FoV[rartv]</a>
</div>
<a href="magnet:?xt=urn:btih:bc83aeb4a66d35263327a797ed6f939af31f01dc&dn=Doctor.Who.2005.8x07.Kill.The.Moon.720p.HDTV.x264-FoV%5Brartv%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Fopen.demonii.com%3A1337" title="Download this torrent using magnet"><img src="/static/img/icon-magnet.gif" alt="Magnet link" /></a><img src="/static/img/icon_comment.gif" alt="This torrent has 6 comments." title="This torrent has 6 comments." /><a href="/user/Drarbg"><img src="/static/img/vip.gif" alt="VIP" title="VIP" style="width:11px;" border='0' /></a>
            <font class="detDesc">Uploaded Y-day&nbsp;22:17, Size 997.69&nbsp;MiB, ULed by <a class="detDesc" href="/user/Drarbg/" title="Browse Drarbg">Drarbg</a></font>
                    </td>
                            <td align="right">6501</td>
                                    <td align="right">3097</td>
                                        </tr>
                                            <tr>
                                                    <td class="vertTh">i
    """

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
    """Take the data/<fileName> file and complies a title/epiNum dictionary
    """
    try:
        with open(suppliedFile) as f:
            for line in f:
                item = line.split()
                title, episode = item[0], int(item[1])
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
                item = line.split()
                title, episodeNum = item[0], int(item[1])
                listValue = showEpisode(title, episodeNum) 
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
                item = line.strip('\n')
                compiled_list.append(item)
        f.close
        return compiled_list
    
    except IOError:
        print "%s was not found. Check your data location." % suppliedFile
        exit(1)

class showEpisode(object):
    def __init__(self, title, episodeNum):
        self.title = title
        self.episodeNum = episodeNum
        self.downloadLink = None
        self.acquired = False

                
    def processMatch(self, matchCheck):
        print "processMatch processing %s E %s" % (self.title, self.episodeNum)
        if matchCheck:
            print "MATCH found for %s E %s" % (self.title, self.episodeNum) 
            self.downloadLink = matchCheck.group(0)
            #updateShowDict(title, showDict)
        else:
            print "Episode not available yet"

    def applyRegEx(self, dataToTest=superTestData):
            """Apply the regEx to the title:episode combo, return a match object"""
            print "applyRegEx processing %s E %s" % (self.title, self.episodeNum)
            regEx = re.compile(r"""
                magnet# beginning of magnet link
                .*# anything until title
                %s# title
                .*?S# match the rest of the title up to S
                .{0,2}?# all the bits between title and episode
                E?0?%s# episode number
                .*?# anything until the end of the link, made ungreedy by the '?'
                (?=")
                """ % (self.title, self.episodeNum), re.VERBOSE | re.IGNORECASE)
            matchCheck = regEx.search(dataToTest)
            return matchCheck
        
    def updateFound(self):
        self.acquired = True
        self.episodeNum += 1

def getSiteData(siteList):
    """Acquire site data from each URL in a list"""
    for url in siteList:
        user_agent = "" # fill this in 
        request = urllib2.Request(url)    
        response = urllib2.urlopen(request)
        tempData = response.read() # make sure to change this to read()
        siteData.append(tempData)
    return siteData

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
            print "No link for %s E %s" % (showObjects[i].title, showObjects[i].episodeNum)
        elif showObjects[i].downloadLink != None:
            print "Writing link files for %s E %s" % (showObjects[i].title, showObjects[i].episodeNum)
            ## to write links into one file
            #with open(suppliedFile, 'a') as f:
            #    f.write(showObjects[i].downloadLink +'\n')
            #    f.close()
            ## to write out individual link files
            dataDir = getDirectoryPath("data/")
            print dataDir
            abs_file_path = os.path.join(dataDir, "magnets", showObjects[i].title +  ".magnet")
            print abs_file_path
            with open(abs_file_path, 'w') as f:
                f.write(showObjects[i].downloadLink +'\n')
                f.close()
            
            showObjects[i].updateFound()
        print raw_input(">>")

def writeOutShowFile():
    dataDir = getDirectoryPath("data/")
    print dataDir
    abs_file_path = os.path.join(dataDir, 'showList')
    print abs_file_path
    with open(abs_file_path, 'w') as f:
        for i in range(len(showObjects)):
            title = showObjects[i].title
            episode = showObjects[i].episodeNum
            fileEntry = "%s %s\n" % (title, episode)
            f.write(fileEntry)
        f.close()

        print showObjects[i].title, showObjects[i].episodeNum

def searchForShows(data):
    for idata in range(len(data)):
        for i in range(len(showObjects)):
            print "seachForShows processing %s E %s" % (showObjects[i].title, showObjects[i].episodeNum)
            if showObjects[i].acquired == False:
                showObjects[i].processMatch(showObjects[i].applyRegEx(data[idata]))
            else:
                print "%s already FOUND" % showObjects[i].title

def whatDo():
    """Execute all the things"""
    showListFile = getFilePath('showList')
    urlListFile = getFilePath('urlList')
    matchListFile = getFilePath('matchList.magnet')
    
    showDict = makeDict(showListFile)
    urlList = makeList(urlListFile)

    genShowObjects(showListFile)
    printList(showObjects)
    for i in range(len(showObjects)):
        print showObjects[i].title, showObjects[i].episodeNum

    data = getSiteData(urlList)
    searchForShows(data) # change to variable data for real life
    writeOutLinks(matchListFile)
    writeOutShowFile()    
# testing
    #print showListFile
    #print urlListFile
    #printDict(showDict)
    #for i in range(len(showObjects)):
    #print showObjects[i].title, showObjects[i].episodeNum, "\tFound:", showObjects[i].acquired
    #printList(urlList)    
whatDo()


