def full_help():
    print """
    showScrape Usage

    SYNOPSIS
        showScrape.py [-s ] title seasonNumber episodeNumber [-i] file

    DESCRIPTION
        Search for television show magnet links on thepiratebay.se. A search may be for a single show name season episode number. Alternatively, a list file, one title season and episode number per line. If a magnet link is found, the the episode number will be incremented in the file. To prevent IP blocking there is a one minute delay between urlrequests.

    OPTIONS
        -s, --search title seasonNumber episodeNumber
            Perform a single search.

        -i, --infile input_file
            Search for each title seasonNumber episodeNumber entry (one per line) in the provided file.

        -h Display this help.
    """
