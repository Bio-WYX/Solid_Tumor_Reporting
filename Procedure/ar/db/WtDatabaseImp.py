import abc


class WtDatabaseImp:
    @abc.abstractmethod
    def set_db_info(self, config):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def get_table(self, category, sub):
        pass
