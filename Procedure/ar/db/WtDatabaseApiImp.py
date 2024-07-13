import requests

from ar.common.WtArError import WtArError
from ar.db.WtDatabaseImp import WtDatabaseImp

from ar.table.WtApiTable import WtApiTable


class WtDatabaseApiImp(WtDatabaseImp):
    def __init__(self):
        self.db_config = {}
        self.table_dict = {}

    def set_db_info(self, config):
        """
        配置数据库连接信息
        :param config: dict
        """
        self.db_config = config

    def get_conn(self):
        return requests

    def get_url_prefix(self):
        return self.db_config['url']

    def close(self):
        """
        关闭数据库链接，并且清理缓存
        """
        self.table_dict = {}

    def get_table(self, category, sub):
        """
        获取数据库表头信息
        :param category: 对应excel
        :param sub: 对应sheet
        :return: 返回表头信息和对应id
        """
        key = category + '##' + sub
        if key not in self.table_dict:
            self.table_dict[key] = WtApiTable(self.__load_head(category, sub), self)

        return self.table_dict[key]

    def __load_head(self, category, sub):
        """
        获取数据库表头信息
        :param category: 对应excel
        :param sub: 对应sheet
        :return: 返回表头信息和对应id
        """
        
        headers = {'accept-encoding':'gzip'}
        r = self.get_conn().post(self.get_url_prefix() + '/kb/queryHead', data={'category': category, 'sub': sub}, headers=headers)
        r = r.json()
        if r['code'] == 0:
            return {
                'id': r['headId'],
                'category': category,
                'sub': sub,
            }
        else:
            raise WtArError('请求远程接口失败，{}-{}'.format(category, sub))

