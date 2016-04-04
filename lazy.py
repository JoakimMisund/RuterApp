# -*- coding: utf-8 -*-

import time, os, re, cPickle as pick


### 4.4 ###
class BufferEntry(object):
    """ Class that contains information required to buffer online requests.
    
    Attributes:
        __content: The result of calling the buffered function
        __timeStamp: The time the buffered function was called, or the time the content was retrived. 
    """
    
    def __init__(self, content, timeStamp=time.time()):
        self.__content = content
        self.__timeStamp = timeStamp

    def isObsolete(self):
        """Check if the content the buffer holds is outdated/obsolete.
        This is checked by comparing the current time to the saved timeStamp.
        A entry is obsolete if the difference between the timeStamp and the current time is more than 6 hours,
        or 21600 seconds.

        Return:
            Boolean value indicating whether the entry is obsolete"""
        if( abs( self.__timeStamp - time.time()) > 21600 ):
            return True
        return False

    def getContent(self):
        return self.__content
        
    content = property(fget=getContent)

class Lazy(object):
    """Buffers the result of consecutive calls with the same argument to a given function."""
    def __init__(self, func, savefileName='buffersave.lazy'):

        self.func = func
        self.savefileName = savefileName
        
        self.buffer = {}
        self.readBufferFromDisk()

    def __call__(self, arg, timeStamp=time.time()):
        """Returns the result from calling the saved function on the provided argument.
        If this has been done the last 6 hours, for the same argument, the buffered result is returned."""
            
        #We have a buffered result with this argument
        if arg in self.buffer:

            bufferEntry = self.buffer[arg]

            if bufferEntry.isObsolete():
                self.buffer.pop(arg)
                print("Buffer is obsolete, throwing it away")
            else:
                print "I have a copy of it!"
                return bufferEntry.content

        print u"I have to retrive the page!: {0}".format(arg)
        content = self.func(arg)

        self.buffer[arg] = BufferEntry(content, timeStamp)

        #A new entry has been added, in order not to loose informating the buffer is saved right away
        self.saveBuffer();

        return content

    def saveBuffer(self):
        """Saves the buffer, a dictionary, to disk. Uses cPickle"""
        with open(self.savefileName, 'wb') as f:
            pick.dump(self.buffer, f);

    def readBufferFromDisk(self):
        """Read a buffer from the disk if the file containing it exists"""
        if os.path.exists(self.savefileName):
            with open(self.savefileName) as f:
                self.buffer = pick.load(f)

