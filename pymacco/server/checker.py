import os

from twisted.cred import checkers


class FilePasswordDB(checkers.FilePasswordDB):
    """ A file-based, text-based username/password database.

        The only difference between this and the Twisted version
        is that this also has the ability to add a user to the database.
    """
    def __init__(self, *args, **kwargs):
        checkers.FilePasswordDB.__init__(self, *args, **kwargs)
        if not os.path.isfile(self.filename):
            self._createEmptyFile()

    def addUser(self, username, password):
        f = open(self.filename, 'a')
        try:
            row = [username, password][::not self.ufield or -1]
            line = self.delim.join(row)
            f.write(line + '\n')
        finally:
            f.close()

    def _createEmptyFile(self):
        f = open(self.filename, 'w')
        try:
            f.write('')
            f.flush()
        finally:
            f.close()
