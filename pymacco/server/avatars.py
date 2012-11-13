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
    pass


