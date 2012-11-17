from twisted.spread import pb


class DeniedRequest(pb.Error):
    """ Raised by the server in response to a bad request."""
