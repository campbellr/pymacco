from roster import LocalRoster, RemoteRoster


class LocalUserManager(LocalRoster):

    def userLogin(self, user):
        self[user.name] = user
        self.notify('userLogin', username=user.name)

    def userLogout(self, user):
        del self[user.name]
        self.notify('userLogout', username=user.name)


class RemoteUserManager(RemoteRoster):

    def observe_userLogin(self, username, info):
        self[username] = info
        self.notify('userLogin', username=username)

    def observe_userLogout(self, username):
        del self[username]
        self.notify('userLogout', username=username)

