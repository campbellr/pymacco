import traceback

from twisted.internet import reactor
from twisted.protocols import basic


class BaseCommandProcessor(basic.LineReceiver):
    """ Protocol that implements something similar to `cmd.Cmd` for Twisted.

        Subclasses simply implement commands by creating ``do_<something>``

        For example:

        >>> class MyCommand(BaseCommandProcessor):
        >>>    def do_help(self):
        >>>        self.sendLine("My help message.")

    """
    delimiter = '\n'
    prompt = '>>> '

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.sendLine("Pymacco client console. Type 'help' for help.")
        self.transport.write(self.prompt)

    def connectionLost(self, reason):
        self.sendLine("Connection lost")
        if reactor.running:
            reactor.stop()

    def lineReceived(self, line):
        if not line:
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
        else:
            try:
                method(*args)
            except Exception, e:
                self.sendLine('Error: ' + str(e))
                self.sendLine(traceback.format_exc())


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

        self.sendLine(self.prompt)

    def do_quit(self):
        """quit: Quit this session"""
        self.sendLine("Quitting...")
        self.transport.loseConnection()


class PymaccoClientCommandProcessor(ExtendedCommandProcessor):
    def __init__(self, client):
        self.client = client

    def do_connect(self, hostname, port):
        """connect <hostname> <port>: Connect to the given server.
        """
        self.client.connect(hostname, int(port))
        self.sendLine("Connected.")
        self.transport.write(self.prompt)

    def do_register(self, username, password):
        """register <username> <password>: Register the given
           username/password.

            Note that you must first be registered an logged-in to start or
            join any games.
        """
        def registerSuccess(avatar):
            self.sendLine("Successfully registered.")
            self.transport.write(self.prompt)

        def registerFailed(reasons):
            self.sendLine("Registration failed.")
            self.transport.write(self.prompt)

        d = self.client.register(username, password)
        d.addCallback(registerSuccess)
        d.addErrback(registerFailed)

    def do_login(self, username, password):
        """login <username> <password>: log into the current server with
            the given username/password.
        """
        def loginSuccess(avatar):
            self.sendLine("Successfully logged in.")
            self.transport.write(self.prompt)

        def loginFailed(reasons):
            self.sendLine("Login failed.")
            self.transport.write(self.prompt)

        d = self.client.login(username, password)
        d.addCallback(loginSuccess)
        d.addErrback(loginFailed)
