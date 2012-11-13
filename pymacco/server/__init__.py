from twisted.spread import pb
from twisted.cred import checkers
from twisted.cred.portal import Portal

# TODO: use/create a real password database
checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()

from pymacco.server.realm import Realm

realm = Realm()
portal = Portal(realm)
# regular login
portal.registerChecker(checker)
# anonymous login
portal.registerChecker(checkers.AllowAnonymousAccess())

factory = pb.PBServerFactory(portal)
