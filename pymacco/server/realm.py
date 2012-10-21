from twisted.cred import checkers, portal
from twisted.spread import pb
from zope.interface import implements

from pymacco.avatars import AnonymousUser, RegisteredUser


class Realm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarID, mind, *interfaces):
        assert pb.IPerspective in interfaces
        if avatarID == checkers.ANONYMOUS:
            return pb.IPerspective, AnonymousUser(), lambda: None
        else:
            avatar = RegisteredUser(avatarID)
            avatar.attached(mind)
            return pb.IPerspective, avatar, lambda: None
