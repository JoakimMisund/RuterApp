# -*- coding: utf-8 -*-

import urllib
import sys


def getHtml(URL):
    """Returns a string containing the html code received from the provided url.
       The function can be used to retrive any file from an server. It can cause the 
       program to exit if the call to urllib.urlopen fails.
    Input:
        URL
           String containing the url to be queried
    Output:
        HTML
           String containing the html received from the server
    """
    try:
        URL = URL.encode('utf-8')
        text = urllib.urlopen(URL).read().decode("utf-8")
        return text
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        print "Failed to retrive an url with urllib.urlopen!!"
        print "Are you sure that you are connected to the internet?"
        print "Exiting!"
        exit(-1)


