''' items.py - photofroggy
    Handle an item's subcommand.
'''

from lab.handle import Handler
from lab.store import say, Archive


class Items(Handler):
    """
    Handle the item subcommand.
    """
    
    def isHandler(self):
        """
        This object shouldn't handle commands.
        """
        return False
    
    def init(self, *args):
        """
        Add subcommand handlers.
        """
        self.archive = Archive('archive/'+self.cmd + 's.json')
        sub = self.parser.add_subparsers()
        self.subs(sub)
    
    def subs(self, sub):
        """
        Hook sub command handlers
        """
        ItemAdd('add', sub, self.archive, self.cmd)
        ItemList('list', sub, self.archive, self.cmd)
        ItemRemove('remove', sub, self.archive, self.cmd)
        ItemUp('up', sub, self.archive, self.cmd)
        ItemDown('down', sub, self.archive, self.cmd)
        ItemEdit('edit', sub, self.archive, self.cmd)
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'manage the items displayed on the front page'


class ItemHandler(Handler):
    """
    Handle the add subcommand.
    """
    
    def init(self, archive, cmd):
        """
        Parse arguments.
        """
        self.archive = archive
        self.mcmd = cmd
        self.arguments()
    
    def arguments(self):
        """
        Add arguments.
        """



class ItemAdd(ItemHandler):
    """
    Handle the add subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'add an item to the list'
    
    def arguments(self):
        """
        Parse arguments.
        """
        self.parser.add_argument('--url', help='item url', required=True)
        self.parser.add_argument('--title', help='item title', required=True)
        self.parser.add_argument('--tags', help='item tags', default="")
        self.parser.add_argument('--description', help='item description', default="")
        self.parser.add_argument('--index', help='index for the item on the grid', type=int, default=0)
            
    def handle(self, args):
        """
        Handle command.
        """
        self.archive.add(args.index, [args.url, args.title, args.tags, args.description.replace('\!', '!')])


class ItemRemove(ItemHandler):
    """
    Handle the remove subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'remove a item from the list'
    
    def arguments(self):
        """
        Parse arguments.
        """
        self.parser.add_argument('item', help='title or index of the item to remove')
    
    def handle(self, args):
        """
        Handle command.
        """
        item = args.item
        removed = False

        if item.isdigit():
            removed = self.archive.remove( int( item ) )
        else:
            removed = self.archive.removeMatched( 1, item )

        if removed:
            say('Removed {0} {1} from the archive.'.format(self.mcmd, item))
        else:
            say('No such '+self.mcmd)


class ItemList(ItemHandler):
    """
    Handle the list subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'list the different items in the archive'
    
    def handle(self, args):
        """
        Handle command.
        """
        say('Current {0}s:'.format(self.mcmd))
        
        for index, item in enumerate(self.archive.items):
            say( '  {0} - {1}'.format( index, item[1] ) )


class ItemUp(ItemHandler):
    """
    Handle the remove subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'move a item up a position in the list'
    
    def arguments(self):
        """
        Parse arguments.
        """
        self.parser.add_argument('item', help='title or index of the item to move')
    
    def handle(self, args):
        """
        Handle command.
        """
        item = args.item
        index = -1
        items = len(self.archive.items)
        
        if item.isdigit():
            index = int( item )
            if index < 0 or index >= items:
                say('No such {0}. There are {1} {0}s.'.format(self.mcmd, items))
                return
        else:
            index = self.archive.find( 1, item )
            if index == -1:
                say('No such {0}.'.format(self.mcmd))
                say('Use `./dlab item list` to see archived {0}s.'.format(self.mcmd))
                return
        
        if index == 0:
            say('Item {0} is already at the top.'.format(item))
            return
        
        si = index - 1
        proj = self.archive.items[index]
        self.archive.items[index] = self.archive.items[si]
        self.archive.items[si] = proj
        self.archive.save()
        self.archive.load()
        say('Shifted item {0} up to position {1}.'.format(item, si))


class ItemDown(ItemHandler):
    """
    Handle the remove subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'move a item down a position in the list'
    
    def arguments(self):
        """
        Parse arguments.
        """
        self.parser.add_argument('item', help='title or index of the item to move')
    
    def handle(self, args):
        """
        Handle command.
        """
        item = args.item
        index = -1
        items = len(self.archive.items)
        
        if item.isdigit():
            index = int( item )
            if index < 0 or index >= items:
                say('No such {0}. There are {1} {0}s.'.format(self.mcmd, items))
                return
        else:
            index = self.archive.find( 1, item )
            if index == -1:
                say('No such '+self.mcmd+'.')
                say('Use `./dlab item list` to see archive {0}s.'.format(self.mcmd))
                return
        
        if index == items:
            say('Item {0} is already at the bottom.'.format(item))
            return
        
        si = index + 1
        proj = self.archive.items[index]
        self.archive.items[index] = self.archive.items[si]
        self.archive.items[si] = proj
        self.archive.save()
        self.archive.load()
        say('Shifted item {0} down to position {1}.'.format(item, si))


class ItemEdit(ItemHandler):
    """
    Handle the edit subcommand.
    """
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'edit an existing item'
    
    def arguments(self):
        """
        Parse arguments.
        """
        self.parser.add_argument('item', help='title or index of the item to move')
        self.parser.add_argument('--url', help='item url', default=None)
        self.parser.add_argument('--title', help='item title', default=None)
        self.parser.add_argument('--tags', help='item tags', default=None)
        self.parser.add_argument('--description', help='item description', default=None)
    
    def handle(self, args):
        """
        Handle command.
        """
        item = args.item
        index = -1
        items = len(self.archive.items)
        
        if item.isdigit():
            index = int( item )
            if index < 0 or index >= items:
                say('No such {0}. There are {1} {0}s.'.format(self.mcmd, items))
                return
        else:
            index = self.archive.find( 1, item )
            if index == -1:
                say('No such '+self.mcmd+'.')
                say('Use `./dlab {0} list` to see archived {0}s.'.format(self.mcmd))
                return
        
        item = self.archive.items[index]
        self.archive.items[index] = [
            args.url or item[0],
            args.title or item[1],
            args.tags or item[2],
            (args.description or item[3]).replace('\!', '!')]
        self.archive.save()
        self.archive.load()
        say('Saved changes to {0} {1}.'.format(self.mcmd, index))




