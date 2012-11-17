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

    def connectionMade(self):
        self.sendLine("Pymacco (version: %s)" % pymacco.getVersionString())
        self.sendLine("Type 'help' for a list of available commands.")
        self.prompt()

    def connectionLost(self, reason):
        self.sendLine("Connection lost")
        if reactor.running:
            reactor.stop()

    def lineReceived(self, line):
        if not line:
            self.prompt()
            return

        commandParts = line.split()
        command = commandParts[0].lower()
        args = commandParts[1:]
        self._dispatch(command, args)

    def _dispatch(self, command, args):
        try:
            method = getattr(self, 'do_' + command)
        except AttributeError, e:
            self.sendLine('Error: No such command.')
            self.prompt()
        else:
            try:
                method(*args)
            except TypeError, e:
                if "%s() takes" % method.__name__ in str(e):
                    self.sendLine("Invalid parameters for '%s'.\n"
                    "Run 'help %s' for proper usage." % (command, command))
                    self.prompt()
            except Exception, e:
                self.sendLine('Error: ' + str(e))
                if DEBUG:
                    self.sendLine(traceback.format_exc())
                self.prompt()


class ExtendedCommandProcessor(BaseCommandProcessor):
    """A `BaseCommandProcessor` subclass that implements some common commands.
    """
    def do_help(self, command=None):
        """help [command]: List commands, or show help of the given command."""
        if command:
            self.sendLine(getattr(self, 'do_' + command).__doc__)
        else:
            commands = [cmd[len('do_'):] for cmd in dir(self)
                        if cmd.startswith('do_')]
            self.sendLine('Valid commands: ' + ' '.join(commands))

        self.prompt()

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine("Quitting...")
        self.transport.loseConnection()


class PymaccoClientCommandProcessor(ExtendedCommandProcessor):
    def __init__(self, client):
        self.client = client

    def do_connect(self, hostname, port=8777):
        """connect <hostname> <port>: Connect to the given server.
        """
        self.client.connect(hostname, int(port))
        self.sendLine("Connected to %s." % hostname)
        self.prompt()

    def do_disconnect(self):
        """ disconnect: Disconnect from the current server.
        """
        host = self.client.host
        self.client.disconnect()
        self.sendLine("Disconnected from %s" % host)
        self.prompt()

    def do_register(self, username, password):
        """register <username> <password>: Register the given
           username/password.

            Note that you must first be registered an logged-in to start or
            join any games.
        """
        def registerSuccess(avatar):
            self.sendLine("Successfully registered.")
            self.prompt()

        def registerFailed(failure):
            self.sendLine("Registration failed: %s" % \
                    failure.getErrorMessage())
            self.prompt()

        d = self.client.register(username, password)
        d.addCallback(registerSuccess)
        d.addErrback(registerFailed)

    def do_login(self, username, password):
        """login <username> <password>: Log into the current server with
            the given username/password.
        """
        def loginSuccess(avatar):
            self.sendLine("Successfully logged in.")
            self.prompt()

        def loginFailed(failure):
            self.sendLine("Login failed: %s" % failure.getTraceback())
            self.prompt()

        d = self.client.login(username, password)
        d.addCallback(loginSuccess)
        d.addErrback(loginFailed)

    def do_users(self):
        """ users: List the logged-in users.
        """
        users = "\n".join(self.client.users)
        self.sendLine(users)
        self.prompt()
