from twisted.spread import pb
from twisted.python import log


from pymacco.server import checker


class AnonymousUser(pb.Avatar):
    """ An avatar which is only able to register an account.
    """
    def perspective_register(self, username, password):
        """ Create a user account with the specified username and password.
        """
        log.msg("Registering user: %s" % username)
        checker.addUser(username, password)


class RegisteredUser(pb.Avatar):
    def __init__(self, name):
        self.name = name

    def attached(self):
        """ Called (by the Realm) when connected.
        """
        log.msg("User %s connected" % self.name)

    def detached(self):
        """ Called (by the Realm) when disconected.
        """
        log.msg("User %s disconnected" % self.name)

    def perspective_getGames(self):
        """ Return the list of games on this server.
        """
        pass

    def perspective_getUsers(self):
        """ Return the list of users on this server
        """
        pass

    def perspective_joinGame(self, gameID):
        """ Join the game with the given `gameID`
        """
        pass

    def perspective_leaveGame(self, gameID):
        """ Leave the game with the given `gameID`
        """
        pass
