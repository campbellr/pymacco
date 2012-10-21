from twisted.spread import pb


class AnonymousUser(pb.Avatar):
    """ An avatar which is only able to register an account.
    """
    def perspective_register(self, username, password):
        """ Create a user account with the specified username and password.
        """
            

