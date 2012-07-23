''' projects.py - photofroggy
    Handle the project subcommand.
'''

from handle import Handler
from store import say, Archive


class Projects(Handler):
    """
    Handle the project subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'project'
        """
        return 'project'
    
    def isHandler(self):
        """
        This object shouldn't handle commands.
        """
        return False
    
    def init(self, *args):
        """
        Add subcommand handlers.
        """
        self.archive = Archive('projects.json')
        sub = self.parser.add_subparsers()
        self.add = ProjectAdd(sub, self.archive)
        self.list = ProjectList(sub, self.archive)
        self.remove = ProjectRemove(sub, self.archive)
        self.up = ProjectUp(sub, self.archive)
        self.down = ProjectDown(sub, self.archive)
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'manage the projects displayed on the front page'
    

class ProjectAdd(Handler):
    """
    Handle the add subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'add'
        """
        return 'add'
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'add a project to the projects displayed on the front page'
    
    def init(self, archive):
        """
        Parse arguments.
        """
        self.archive = archive
        self.parser.add_argument('--url', help='project url', required=True)
        self.parser.add_argument('--title', help='project title', required=True)
        self.parser.add_argument('--tags', help='project tags', default="")
        self.parser.add_argument('--description', help='project description', required=True)
        self.parser.add_argument('--index', help='index for the project on the grid', type=int, default=0)
            
    def handle(self, args):
        """
        Handle command.
        """
        self.archive.add(args.index, [args.url, args.title, args.tags, args.description])


class ProjectRemove(Handler):
    """
    Handle the remove subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'remove'
        """
        return 'remove'
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'remove a project from the featured projects'
    
    def init(self, archive):
        """
        Parse arguments.
        """
        self.archive = archive
        self.parser.add_argument('project', help='title or index of the project to remove')
    
    def handle(self, args):
        """
        Handle command.
        """
        project = args.project
        removed = False

        if project.isdigit():
            removed = self.archive.remove( int( project ) )
        else:
            removed = self.archive.removeItem( 1, project )

        if removed:
            say('Removed project {0} from the archive.'.format(project))
        else:
            say('No such project')


class ProjectList(Handler):
    """
    Handle the list subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'list'
        """
        return 'list'
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'list the different projects in the archive'
    
    def init(self, archive):
        """
        Parse arguments.
        """
        self.archive = archive
    
    def handle(self, args):
        """
        Handle command.
        """
        say('Current posts:')
        
        for index, project in enumerate(self.archive.items):
            say( '  {0} - {1}'.format( index, project[1] ) )


class ProjectUp(Handler):
    """
    Handle the remove subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'up'
        """
        return 'up'
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'move a project up a position in the featured projects'
    
    def init(self, archive):
        """
        Parse arguments.
        """
        self.archive = archive
        self.parser.add_argument('project', help='title or index of the project to move')
    
    def handle(self, args):
        """
        Handle command.
        """
        project = args.project
        index = -1
        projects = len(self.archive.items)
        
        if project.isdigit():
            index = int( project )
            if index < 0 or index >= projects:
                say('No such project. There are {0} projects.'.format(projects))
                return
        else:
            index = self.archive.find( 1, project )
            if index == -1:
                say('No such project.')
                say('Use `./dlab project list` to see archived projects.')
                return
        
        if index == 0:
            say('Project {0} is already at the top.'.format(project))
            return
        
        si = index - 1
        proj = self.archive.items[index]
        self.archive.items[index] = self.archive.items[si]
        self.archive.items[si] = proj
        self.archive.save()
        self.archive.load()
        say('Shifted project {0} up to position {1}.'.format(project, si))


class ProjectDown(Handler):
    """
    Handle the remove subcommand.
    """
    
    def getcmd(self):
        """
        Returns 'down'
        """
        return 'down'
    
    def getdescription(self):
        """
        Returns the command description.
        """
        return 'move a project down a position in the featured projects'
    
    def init(self, archive):
        """
        Parse arguments.
        """
        self.archive = archive
        self.parser.add_argument('project', help='title or index of the project to move')
    
    def handle(self, args):
        """
        Handle command.
        """
        project = args.project
        index = -1
        projects = len(self.archive.items)
        
        if project.isdigit():
            index = int( project )
            if index < 0 or index >= projects:
                say('No such project. There are {0} projects.'.format(projects))
                return
        else:
            index = self.archive.find( 1, project )
            if index == -1:
                say('No such project.')
                say('Use `./dlab project list` to see archived projects.')
                return
        
        if index == projects:
            say('Project {0} is already at the bottom.'.format(project))
            return
        
        si = index + 1
        proj = self.archive.items[index]
        self.archive.items[index] = self.archive.items[si]
        self.archive.items[si] = proj
        self.archive.save()
        self.archive.load()
        say('Shifted project {0} down to position {1}.'.format(project, si))



