from pymacco.common.roster import LocalRoster, RemoteRoster


class LocalTableManager(LocalRoster):

    def openTable(self, table):
        self[table.id] = table
        self.notify('openTable', table.id)

    def closeTable(self, table):
        del self[table.id]
        self.notify('closeTable', table.id)


class RemoteTableManager(RemoteRoster):

    def observe_openTable(self, tableid):
        self[tableid] = None
        self.notify('openTable', tableid)

    def observe_closeTable(self, tableid):
        del self[tableid]
        self.notify('closeTable', tableid)
