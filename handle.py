''' handle.py - photofroggy
    Handle different CLI commands.
'''
from store import say, Archive

class Handler(object):
    """
    A base class that acts as an example.
    """
    
    def __init__(self, argparser, *args):
        self.cmd = None
        self.cmd = self.getcmd()
        self.parser = argparser.add_parser(self.cmd, description=self.getdescription())
        if self.isHandler():
            self.parser.set_defaults(func=self.handle)
        self.init(*args)
    
    def init(self, *args):
        """
        Override this to do stuff like hook arguments.
        """
    
    def getcmd(self):
        """
        Return the name of the command.
        """
        if self.cmd is None:
            return 'command'
        
        return self.cmd
    
    def getdescription(self):
        """
        Get the description of the command.
        """
        return 'Command description.'
    
    def isHandler(self):
        """
        Is this object one that handles commands?
        """
        return True
    
    def handle(self, args):
        """
        Handle the subcommand when called.
        """


