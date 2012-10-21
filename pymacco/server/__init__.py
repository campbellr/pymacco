from twisted.spread import pb
from twisted.cred import checkers
from twisted.cred.portal import Portal

from pymacco.server.realm import Realm

realm = Realm()
portal = Portal(realm)
# regular login
portal.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse())
# anonymous login
portal.registerChecker(checkers.AllowAnonymousAccess())

factory = pb.PBServerFactory(portal)
