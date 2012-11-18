import time
from twisted.internet import reactor
from twisted.spread import pb
from zope.interface import implements

from pymacco.interfaces import ISubject, IListener
from pymacco.common.roster import LocalRoster, RemoteRoster
from pymacco.common.errors import DeniedRequest, GameError


class Player(pb.Referenceable):

    def __init__(self, game):
        self._game = game

    def getHand(self):
        return self._game.getHand(self)

    def playCard(self, card):
        return self._game.playCard(self, card)

    remote_getHand = getHand
    remote_playCard = playCard


# Temporary mock game class for testing
class PymaccoGame(object):

    implements(ISubject)

    def __init__(self):
        self.listeners = []
        self.players = {}

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners:
            listener.update(event, *args, **kwargs)

    def start(self):
        if self.inProgress():
            raise GameError("Game in progress")

    def getState(self):
        pass

    def addPlayer(self, name):
        self.players[name] = Player(self)
        self.notify('addPlayer', name)

    def removePlayer(self, name):
        del self.players[name]
        self.notify('removePlayer', name)

    def playCard(self, player, card):
        pass


class LocalTable(pb.Cacheable):

    implements(ISubject, IListener)

    class TableClient(pb.Viewable):

        def __init__(self, table):
            self._table = table

        def view_joinGame(self, user):
            return self._table.joinGame(user)

        def view_leaveGame(self, user):
            return self._table.leaveGame(user)

    def __init__(self, id, config=None):
        if config is None:
            config = {}
        self. listeners = []
        self.id = id
        self.game = PymaccoGame()
        self.observers = {}
        self.players = []
        self.view = self.TableClient(self)

        self.config = {}
        self.config['CloseWhenEmpty'] = True
        self.config['TimeCreated'] = tuple(time.localtime())
        self.config.update(config)

    def close(self):
        """ Close the table."""
        pass

    def getStateToCacheAndObserveFor(self, perspective, observer):
        self.notify('addObserver', observer=perspective.name)
        self.observers[perspective] = observer

        state = {}
        state['id'] = self.id
        state['gamestate'] = self.game.getState()
        state['observers'] = [p.name for p in self.observers.keys()]
        state['players'] = [p.name for p in self.players]
        state['view'] = self.view

        return state

    def stoppedObservering(self, perspective, observer):
        del self.observers[perspective]

        for user in self.players:
            if perspective == user:
                self.leaveGame(perspective)
        self.notify('removeObserver', observer=perspective.name)

        if self.cofig.get('CloseWhenEmpty') and not self.observers:
            self.close()

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners:
            listener.update(event, *args, **kwargs)
        for observer in self.observers.values():
            self.notifyObserver(observer, event, *args, **kwargs)

    def notifyObserver(self, observer, event, *args, **kwargs):
        reactor.callLater(0, observer.callRemote, event, *args, **kwargs)

    def update(self, event, *args, **kwargs):
        for observer in self.observers.values():
            self.notifyObserver(observer, 'gameUpdate', event, *args, **kwargs)

    def joinGame(self, user):
        if user in self.players:
            raise DeniedRequest("Already playing in game.")

        player = self.game.addPlayer(user.name)
        self.players.append(user)
        self.notify('joinGame', player=user.name)
        return player

    def leaveGame(self, user):
        if user not in self.players:
            raise DeniedRequest("Not playing in game.")
        self.game.removePlayer(user.name)
        self.players.remove(user)
        self.notify('leaveGame', player=user.name)


class RemoteTable(pb.RemoteCache):

    implements(ISubject)

    def __init__(self):
        self.game = PymaccoGame()
        self.listeners = []
        self._view = None

    def setCopyableState(self, state):
        self.id = state['id']
        self.game.setState(state['gamestate'])
        self.observers = state['observers']
        self.players = state['players']
        for player in self.players:
            self.game.addPlayer(player)
        self._view = state['view']

    def joinGame(self, user):
        d = self.view.callRemote('joinGame', user)
        return d

    def leaveGame(self, user):
        d = self._view.callRemote('leaveGame', user)
        return d

    def attach(self, listener):
        self.listeners.append(listener)

    def detach(self, listener):
        self.listeners.remove(listener)

    def notify(self, event, *args, **kwargs):
        for listener in self.listeners:
            listener.update(event, *args, **kwargs)

    def observe_addObserver(self, observer):
        self.observers.append(observer)
        self.notify('addObserver', observer)

    def observe_removeObserver(self, observer):
        self.observers.remove(observer)
        self.notify('removeObserver', observer)

    def observe_joinGame(self, player):
        self.game.addPlayer(player)
        self.players.append(player)
        self.notify('joinGame', player)

    def observe_leaveGame(self, player):
        self.game.removePlayer(player)
        self.players.remove(player)
        self.notify('leaveGame', player)

    def observe_gameUpdate(self, event, *args, **kwargs):
        self.game.updateState(event, *args, **kwargs)


class LocalTableManager(LocalRoster):

    def openTable(self, table):
        self[table.id] = table
        self.notify('openTable', table.id)

    def closeTable(self, table):
        del self[table.id]
        self.notify('closeTable', table.id)


class RemoteTableManager(RemoteRoster):

    def observe_openTable(self, tableid):
        self[tableid] = None
        self.notify('openTable', tableid)

    def observe_closeTable(self, tableid):
        del self[tableid]
        self.notify('closeTable', tableid)
