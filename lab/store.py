#!/usr/bin/python
import sys
import json

"""
Helper classes and functions for the blog.
This is part of my ongoing effort to overcomplicate
everything in the world ever.
"""


def say(msg):
    """
    Write msg to stdout.
    Don't forget to flush!
    """
    sys.stdout.write('>> ' + msg + '\n')
    sys.stdout.flush()


class Archive(object):
    """
    Represents an archive
    """
    
    def __init__(self, path='archive.json'):
        self.path = path
        self.items = []
        self.load()
    
    def load(self):
        """
        Load the archive from our entries file.
        Resulting data is stored in self.items.
        """
        f = open(self.path, 'r')
        d = f.read()
        f.close()
        self.items = json.loads(d)
    
    def save(self):
        """
        Save the archive to our entries file.
        """
        f = open(self.path, 'w')
        f.write(json.dumps(self.items))
        f.close()
    
    def add(self, index, item):
        """
        Add a new item to the archive.
        """
        self.items.insert( index, item )
        self.save()
        self.load()
    
    def get(self, index=0):
        """
        Get the archive entry at the given index.
        If no entry is found, None is returned.
        """
        if len(self.items) <= index:
            return None
        
        return self.items[index]
    
    def remove(self, index=0):
        """
        Remove the archive entry at the given index.
        Return True on success, False on failure.
        """
        entry = self.get(index)
        
        if entry is None:
            return False
        
        self.items.pop(index)
        self.save()
        self.load()
        
        return True
    
    def find(self, matchi, match):
        """
        Find an archive entry by the title of the entry.
        Returns the index. -1 is not found.
        """
        match = match.lower()
        
        for index, item in enumerate(self.items):
            if item[matchi].lower() == match:
                return index
        
        return -1
    
    def removeMatched(self, matchi, match):
        """
        Find and remove an archive entry with the given item.
        Returns a boolean.
        """
        index = self.find(matchi, match)
        
        if index == -1:
            return False
        
        return self.remove(index)

