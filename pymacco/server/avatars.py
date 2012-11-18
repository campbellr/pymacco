from twisted.spread import pb
from twisted.python import log

from pymacco.server import checker, state
from pymacco.common.table import LocalTable
from pymacco.common.errors import DeniedRequest


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
        self.joinedTables = {}

    def attached(self):
        """ Called (by the Realm) when connected.
        """
        log.msg("User %s connected" % self.name)
        state.onlineUsers.userLogin(self)

    def detached(self):
        """ Called (by the Realm) when disconected.
        """
        log.msg("User %s disconnected" % self.name)
        state.onlineUsers.userLogout(self)

    def perspective_getTables(self):
        """ Return the list of tables on this server.
        """
        return state.availableTables

    def perspective_getUsers(self):
        """ Return the list of users on this server
        """
        return state.onlineUsers

    def perspective_createTable(self, tableID):
        """ Create a table with the given `tableID`.
        """
        table = LocalTable(tableID)
        # Provide table instance with a means of closing itself.
        table.close = lambda: state.availableTables.closeTable(table)
        state.availableTables.openTable(table)
        log.msg("User '%s' created table '%s'" % (self.name, tableID))
        return table

    def perspective_joinTable(self, tableID):
        """ Join the table with the given `tableID`
        """
        try:
            table = state.availableTables[tableID]
        except KeyError:
            raise DeniedRequest("No table with name '%s' exist." % tableID)

        self.joinedTables[tableID] = table
        log.msg("User '%s' joined table '%s'" % (self.name, tableID))

    def perspective_leaveTable(self, tableID):
        """ Leave the table with the given `tableID`
        """
        if tableID not in self.joinedTables:
            raise DeniedRequest("Not joined table '%s'" % tableID)

        del self.joinedTables[tableID]
        log.msg("User '%s' left table '%s'" % (self.name, tableID))
