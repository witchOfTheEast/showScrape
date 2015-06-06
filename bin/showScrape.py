import os, urllib2, re, sys, getopt, time, gzip
from StringIO import StringIO

outToShowList = []

def checkDir(desiredDir):
    """Check for a necessary directory in the script root. If not found, create it recursively."""
    if os.path.exists(desiredDir) != True:
        os.makedirs(desiredDir)

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

def processShowListFile(suppliedFile):
    """Search for each show entry in file line by line."""
    with open(suppliedFile) as f:
        for line in f:
            lineContents = line.split()
            
            if len(lineContents) < 3:
                try:
                    print "%s entry is incorrectly formatted. Likely \
                    missing season or episode numbers." % lineContents[1]
                
                except IndexError:
                    print "Catastrophic error reading line from %s" % suppliedFile

            else:
                try: # catch a missing season and insert '00' season place holder
                    lineContents[2]

                except IndexError:
                    lineContents.insert(1, '00')
            
            # append a zero before single digit episode and season numbers
            for i in range(1, 3):
                if len(lineContents[i]) < 2:
                    lineContents[i] = '0' + lineContents[i]
            
            title, season, episode = lineContents[0:3]
            
            singleEntry(title, season, episode)
            time.sleep(20) 

class show(object):
    def __init__(self, title, seasonNum, episodeNum):
        self.title = title
        self.episodeNum = episodeNum
        self.seasonNum = seasonNum
        self.downloadLink = None
        self.acquired = False

                
    def processMatch(self, matchCheck):
        
        if matchCheck:

            self.downloadLink = matchCheck.group(0)

        else:
            print ""
            print "No MATCH for %s S%sE%s yet" % (self.title, self.seasonNum,
                self.episodeNum)
            print ""

    def applyRegEx(self, dataToTest):
            """Search data for title/season/episode regex, return a match object"""
            regEx = re.compile(r"""
                (?<=href=")# ensure we match the actual link, non-capturing
                magnet# beginning of magnet link
                .*# anything until title
                %s# title
                .*?S# match the rest of the title up to S
                %sE%s# season number and episode number
                .*?# anything after episode number
                (eztv|ettv|rarbg)# to avoid downloading fakes
                .*?# anything until the end of the link, made ungreedy by the '?'
                (?=")# ungreedy, non-inclusive link closing quote mark
                """ % (self.title, self.seasonNum, self.episodeNum), re.VERBOSE
                    | re.IGNORECASE)
            matchCheck = regEx.search(dataToTest)
            return matchCheck
        
    def updateFound(self):
        self.acquired = True
        self.episodeNum = int(self.episodeNum) + 1

def getSomeData(url):
    """Acquire site data from single supplied URL"""
    user_agent = "" # fill this in 
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip') # not strickly necessary? 
    request.add_header('User-agent', 'Mozilla/5.0') # not strickly necessary? 
    response = urllib2.urlopen(request)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        tempData = f.read() 
    else:
        print 'Response encoding: ', response.headers['content-encoding']
        tempData = response.read()
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

def writeSingleLink(showObject):
    if showObject.downloadLink != None:
        print ""
        print "Writing link file for %s S%sE%s" % (showObject.title,
            showObject.seasonNum, showObject.episodeNum)
               
        dataDir = getDirectoryPath("data/")
        
        abs_file_path = os.path.join(dataDir, "magnets",
            showObject.title + ".S" + showObject.seasonNum + "E" +
            showObject.episodeNum + ".magnet")
        
        with open(abs_file_path, 'w') as f:
            f.write(showObject.downloadLink +'\n')
            f.close()
        
        showObject.updateFound()
        print 'Success!'
    else:
        # do nothing because there is no link
        pass

def writeOutShowFile(showListArg):
    
    with open(showListArg, 'w') as f:
        for i in outToShowList:
            str1 = '%s %s %s\n' % (i[0], i[1], i[2])
            f.write(str1) 
        f.close()

def makeSearchUrl(whichShow):
    """Return single title/season/episode search url from show object"""
    # pattern is TITLE%20S##E##/0/7/0
    searchUrl = '' 
    baseUrl = "http://thepiratebay.se/search/%s%%20S%sE%s/0/7/0"
    baseUrl2 = "http://thepiratebay.se/search/%s%%20E%s/0/7/0"
     
    #baseUrl = "http://piratebay.ws/search/%s%%20S%sE%s/0/7/0"
    #baseUrl2 = "http://piratebay.ws/search/%s%%20E%s/0/7/0"
    #baseUrl = 'https://kickass.so/usearch/?q=%s+S%sE%s'
    #baseUrl2 = 'https://kickass.so/usearch/?q=%s+E%s'
    
    if whichShow.seasonNum == '00':
        compositeUrl = baseUrl2 % (whichShow.title, whichShow.episodeNum)
    else:
        compositeUrl = baseUrl % (whichShow.title, whichShow.seasonNum,
            whichShow.episodeNum)
    
    return compositeUrl 

def genShowObject(title, season, episode):
    """Return a single show object"""
    if len(season) < 2:
        season = '0' + season
    if len(episode) < 2:
        episode = '0' + episode

    return show(title, season, episode)

def handleShowListArg(showListArg):
    """Place holder to initialize a showList and send it to process"""
    processShowListFile(showListArg)
    writeOutShowFile(showListArg)    

def singleEntry(title, season, episode):
    """Process a search for a single show entered on the command line"""
    activeShow = genShowObject(title, season, episode)
    activeUrl = makeSearchUrl(activeShow) # why can't the show class do this automatically?
    activeData = getSomeData(activeUrl)
    activeTest = activeShow.applyRegEx(activeData)
    activeResults = activeShow.processMatch(activeTest)
    writeSingleLink(activeShow)
    outToShowList.append((activeShow.title, activeShow.seasonNum, activeShow.episodeNum))

def main(argv):
    print "main is running"
    checkDir('data/magnets')    

    try:
        opts, args = getopt.getopt(argv, "hi:s", ["ifile="])
    
    except getopt.GetoptError:
        print 'usage:\t-i <inputfile>'
        print '\t-s <title> <season number> <episode number>'
        sys.exit(2)

    for opt, arg in opts:
        
        if opt == '-h':
            print '-s <title> <season number> <episode number>'
            print '-i <inputfile>'
            sys.exit()
        
        elif opt in ("-s", "--search"):
            title = args[0] 
            season = args[1]
            episode = args[2]
            print '%s S%sE%s' % (title, season, episode)
            singleEntry(title, season, episode) 

        elif opt in ("-i", "--infile"):
            if os.path.isfile(arg):
                abs_file_path = os.path.abspath(arg)
                print "Processing: ", abs_file_path 
                handleShowListArg(abs_file_path)
            else:
                print "%r is not a valid file" % arg


if __name__ == "__main__":
    main(sys.argv[1:])

