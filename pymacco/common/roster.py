from UserDict import IterableUserDict

from twisted.spread import pb
from twisted.internet import reactor
from zope.interface import implements

from pymacco.interfaces import ISubject


# FIXME: why doesn't this work when subclassing 'dict'?
class Roster(IterableUserDict):
    """ A dictionary-like object, which combines a set of available items with
        information associated with each item.

        This class implements the ISubject interface to provide notifications
        when an entry in the roster is added, removed or changed.
    """
    implements(ISubject)

    def __init__(self):
        IterableUserDict.__init__(self)
        self.listeners = []

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners:
            listener.update(event, *args, **kwargs)


class LocalRoster(Roster, pb.Cacheable):
    """ A server-side 'master copy' of a Roster.

        Changes to the LocalRoster are relayed to registered RemoteRoster
        objects as well as to all local listeners.
    """
    def __init__(self):
        Roster.__init__(self)
        self.observers = []

    def getStateToCacheAndObserveFor(self, perspective, observer):
        self.observers.append(observer)
        state = dict((id_, getattr(item, 'info', None))
                for (id_, item) in self.items())
        print type(self), state
        return state

    def stoppedObserving(self, perspective, observer):
        self.observers.remove(observer)

    def notify(self, event, *args, **kwargs):
        # Override to provide event notification for remote observers.
        Roster.notify(self, event, *args, **kwargs)

        for observer in self.observers:
            # Event handlers are called on the next iteration of the reactor,
            # to allow the caller of this method to return a result.
            reactor.callLater(0, observer.callRemote, event, *args, **kwargs)


class RemoteRoster(Roster, pb.RemoteCache):
    """A client-side Roster, which mirrors a server-side LocalRoster object
    by tracking changes.
    """
    def setCopyableState(self, state):
        self.update(state)
