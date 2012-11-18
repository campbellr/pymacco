import traceback

from twisted.internet import reactor
from twisted.protocols import basic

import pymacco

DEBUG = True


class BaseCommandProcessor(basic.LineReceiver):
    """ Protocol that implements something similar to `cmd.Cmd` for Twisted.

        Subclasses simply implement commands by creating ``do_<something>``

        For example:

        >>> class MyCommand(BaseCommandProcessor):
        >>>    def do_help(self):
        >>>        self.sendLine("My help message.")

    """
    delimiter = '\n'
    _prompt = '>>> '

    def __init__(self, factory):
        self.factory = factory

    def prompt(self):
        self.transport.write(self._prompt)

    def sendLine(self, line, prompt=True):
        basic.LineReceiver.sendLine(self, line)
        if prompt:
            self.prompt()

    def connectionMade(self):
        self.sendLine("Pymacco (version: %s)" % pymacco.getVersionString(),
                prompt=False)
        self.sendLine("Type 'help' for a list of available commands.")

    def connectionLost(self, reason):
        self.sendLine("Connection lost", prompt=False)
        if reactor.running:
            reactor.stop()

    def lineReceived(self, line):
        if not line:
            self.prompt()
            return

        commandParts = line.split()
        command = commandParts[0].lower().replace('-', '_')
        args = commandParts[1:]
        self._dispatch(command, args)

    def _dispatch(self, command, args):
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError, e:
            self.sendLine('Error: No such command.')
        else:
            try:
                method(*args)
            except TypeError, e:
                if "%s() takes" % method.__name__ in str(e):
                    self.sendLine("Invalid parameters for '%s'.\n"
                    "Run 'help %s' for proper usage." % (command, command))
            except Exception, e:
                self.sendLine('Error: ' + str(e), prompt=False)
                if DEBUG:
                    self.sendLine(traceback.format_exc())
                self.prompt()


class ExtendedCommandProcessor(BaseCommandProcessor):
    """A `BaseCommandProcessor` subclass that implements some common commands.
    """
    def do_help(self, command=None):
        """help [command]: List commands, or show help of the given command."""
        if command:
            self.sendLine(getattr(self,
                'do_' + command.replace('-', '_')).__doc__)
        else:
            commands = [cmd[len('do_'):].replace('_', '-') for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine('Valid commands:\n\t' + '\n\t'.join(commands))

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine("Quitting...", prompt=False)
        self.transport.loseConnection()


# TODO: Only display appropriate commands.
#       eg: if we're not logged in yet, it doesn't make sense to show
#       'users' or 'tables' commands
class PymaccoClientCommandProcessor(ExtendedCommandProcessor):
    def __init__(self, client):
        self.client = client

    def do_connect(self, hostname, port=8777):
        """connect <hostname> <port>: Connect to the given server.
        """
        self.client.connect(hostname, int(port))
        self.sendLine("Connected to %s." % hostname)

    def do_disconnect(self):
        """ disconnect: Disconnect from the current server.
        """
        host = self.client.host
        self.client.disconnect()
        self.sendLine("Disconnected from %s" % host)

    def do_register(self, username, password):
        """register <username> <password>: Register the given
           username/password.

            Note that you must first be registered an logged-in to start or
            join any games.
        """
        def registerSuccess(avatar):
            self.sendLine("Successfully registered.")

        d = self.client.register(username, password)
        d.addCallbacks(registerSuccess, self.errback)

    def do_login(self, username, password):
        """login <username> <password>: Log into the current server with
            the given username/password.
        """
        def loginSuccess(avatar):
            self.sendLine("Successfully logged in.")

        d = self.client.login(username, password)
        d.addCallbacks(loginSuccess, self.errback)

    def errback(self, failure):
        self.sendLine("Error: %s" % failure.getTraceback())

    def do_users(self):
        """ users: List the logged-in users.
        """
        self._getRoster('users')

    def do_tables(self):
        """ tables: List the available tables.
        """
        self._getRoster('tables')

    def do_create_table(self, name):
        """ create table <name>: Create a new table with the given name.
        """
        def createSuccess(table):
            self.sendLine("Created table '%s'." % name)

        def join(table):
            self.do_join_table(name)

        d = self.client.createTable(name)
        d.addCallback(createSuccess)
        d.addCallback(join)

    def do_join_table(self, name):
        """ join table <name>: Join the table with the given name.
        """
        def joinSuccess(table):
            self.sendLine("Joined '%s'" % name)

        d = self.client.joinTable(name)
        d.addCallbacks(joinSuccess, self.errback)

    def do_leave_table(self, name):
        """ leave table <name>: Leave the table with the given name.
        """
        def leaveSuccess():
            self.sendLine("Left table '%s'" % name)

        d = self.client.leaveTable(name)
        d.addCallbacks(leaveSuccess, self.errback)

    def _getRoster(self, name):
        entries = "\n".join(getattr(self.client, name))
        self.sendLine(entries)
