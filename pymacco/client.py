from hashlib import sha1

from twisted.internet import reactor
from twisted.spread import pb
from twisted.cred import credentials
from zope.interface import implements

from pymacco.interfaces import ISubject

from pymacco.common.user import LocalUserManager, RemoteUserManager
from pymacco.common.table import LocalTable, RemoteTable, LocalTableManager, \
                                 RemoteTableManager

pb.setUnjellyableForClass(LocalTable, RemoteTable)
pb.setUnjellyableForClass(LocalTableManager, RemoteTableManager)
pb.setUnjellyableForClass(LocalUserManager, RemoteUserManager)


def requireConnect(func):
    """ A decorator that raises an exception if 'self.connected' is False.
    """
    def wrapped(self, *args, **kwargs):
        if not self.connected:
            raise Exception("You must be connected before using '%s'" %
                    func.__name__)
        return func(self, *args, **kwargs)

    return wrapped


class PymaccoClient(object):
    """ The interface to a pymacco server.
    """
    implements(ISubject)

    def __init__(self):
        self.listeners = []
        self.connected = False
        self.host = None
        self.port = None
        self.users = []
        self.tables = []
        self.factory = pb.PBClientFactory()

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners:
            listener.update(event, *args, **kwargs)

    def connect(self, host, port):
        reactor.connectTCP(host, port, self.factory)
        self.connected = True
        self.host = host
        self.port = port

    def disconnect(self):
        self.factory.disconnect()
        self.connected = False
        self.host = None
        self.port = None

    def errback(self, failure):
        print "\n\nError: %s" % failure.getErrorMessage()
        print "Traceback: %s" % failure.getTraceback()

    @requireConnect
    def login(self, username, password):
        def connectedAsUser(avatar):
            """Actions to perform when connection succeeds."""
            self.avatar = avatar
            self.username = username
            self.notify('loggedIn', username)

            def gotUsers(users):
                self.users = users
                self.notify('gotUsers', users)

            def gotTables(tables):
                self.tables = tables
                self.notify('gotTables', tables)

            d = avatar.callRemote('getTables')
            d.addCallbacks(gotTables, self.errback)

            d = avatar.callRemote('getUsers')
            d.addCallbacks(gotUsers, self.errback)

        def loginFailed(reason):
            self.notify('loginFailed', username)

        hash_ = sha1(password).hexdigest()
        creds = credentials.UsernamePassword(username, hash_)
        d = self.factory.login(creds, client=None)
        d.addCallbacks(connectedAsUser, self.errback)
        return d

    @requireConnect
    def register(self, username, password):
        """Register user account on connected server."""

        def connectedAsAnonymousUser(avatar):
            """Register user account on server."""
            hash_ = sha1(password).hexdigest()
            d = avatar.callRemote('register', username, hash_)
            return d

        anon = credentials.Anonymous()
        d = self.factory.login(anon, client=None)
        d.addCallback(connectedAsAnonymousUser)
        return d

    def joinTable(self, tableID):
        def joinedTable(table):
            self.tables[tableID] = table
            self.notify('joinedTable', tableID, table)
            return table

        d = self.avatar.callRemote('joinTable', tableID)
        d.addCallback(joinedTable)
