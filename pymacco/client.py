from hashlib import sha1

from twisted.internet import reactor
from twisted.spread import pb
from twisted.cred import credentials
from zope.interface import implements

from pymacco.interfaces import ISubject


def requireConnect(func):
    """ A decorator that raises an exception if 'self.connected' is False.
    """
    def wrapped(self, *args, **kwargs):
        if not self.connected:
            raise Exception("You must be connected before using '%s'" %
                    func.__name__)
        func(self, *args, **kwargs)

    return wrapped


class PymaccoClient(object):
    """ The interface to a pymacco server.
    """
    implements(ISubject)

    def __init__(self):
        self.listeners = []
        self.connected = False
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

    def disconnect(self):
        self.factory.disconnect()
        self.connected = False

    @requireConnect
    def login(self, username, password):
        def connectedAsUser(avatar):
            """Actions to perform when connection succeeds."""
            self.avatar = avatar
            self.username = username
            self.notify('loggedIn', username)

        hash_ = sha1(password).hexdigest()
        creds = credentials.UsernamePassword(username, hash_)
        d = self.factory.login(creds, client=None)
        d.addCallback(connectedAsUser)
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