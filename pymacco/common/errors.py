from twisted.spread import pb


class DeniedRequest(pb.Error):
    """ Raised by the server in response to a bad request."""


class GameError(pb.Error):
    """ Raised by a game in response to a invalid request."""
