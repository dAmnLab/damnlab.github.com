''' lab.commands - photofroggy
    Process all commands.
'''

import argparse
from lab.items import Items


class Commands(object):
    """
    Handle the dlab command.
    """
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='manage different archives used in dAmnLab\'s page')
        sub = self.parser.add_subparsers()
        Items('project', sub)
        Items('link', sub)
        Items('developer', sub)
        args = self.parser.parse_args()
        args.func(args)


