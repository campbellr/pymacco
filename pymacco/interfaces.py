from zope.interface import Interface


class ISubject(Interface):
    """ISubject defines methods required for observation of an object."""

    def attach(self, observer):
        """Add observer to list of observers.
        """

    def detach(self, observer):
        """Remove observer from list of observers.
        """

    def notify(self, event, *args, **kwargs):
        """Inform all observers that state has been changed by event.
        """


class IListener(Interface):
    """IListener defines methods required by observers of an ISubject."""

    def update(self, event, *args, **kwargs):
        """Called by ISubject being observed."""
