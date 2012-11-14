import os

from twisted.spread import pb
from twisted.cred import checkers
from twisted.cred.portal import Portal

from pymacco.server.checker import FilePasswordDB

# TODO: make the password db location configurable
checker = FilePasswordDB(os.path.expanduser('~/.pymacco.db'), cache=True)

from pymacco.server.realm import Realm

realm = Realm()
portal = Portal(realm)
# regular login
portal.registerChecker(checker)
# anonymous login
portal.registerChecker(checkers.AllowAnonymousAccess())

factory = pb.PBServerFactory(portal)
