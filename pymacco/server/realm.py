from twisted.cred import checkers, portal
from twisted.spread import pb
from twisted.python import log

from zope.interface import implements

from pymacco.server.avatars import AnonymousUser, RegisteredUser


class Realm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarID, mind, *interfaces):
        assert pb.IPerspective in interfaces
        if avatarID == checkers.ANONYMOUS:
            log.msg("Received request for AnonymousUser")
            return pb.IPerspective, AnonymousUser(), lambda: None
        else:
            log.msg("Received request for RegisteredUser(%s)" % avatarID)
            avatar = RegisteredUser(avatarID)
            avatar.attached(mind)
            return pb.IPerspective, avatar, lambda: None
