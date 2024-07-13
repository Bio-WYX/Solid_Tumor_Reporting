import pymysql

from ar.common.WtArError import WtArError
from ar.db.WtDatabaseImp import WtDatabaseImp
from ar.table.WtMysqlTable import WtMysqlTable


class WtDatabaseMysqlImp(WtDatabaseImp):
    def __init__(self):
        self.conn = None
        self.db_config = {}
        self.table_dict = {}

    def set_db_info(self, config):
        """
        配置数据库连接信息
        :param config: dict
        """
        self.db_config = config

    def get_conn(self):
        """
        获取数据库链接
        :return: object
        """
        if not self.conn:
            self.conn = pymysql.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                passwd=self.db_config['passwd'],
                db=self.db_config['db'],
                port=self.db_config['port'],
                charset=self.db_config['charset']
            )
        return self.conn

    def close(self):
        """
        关闭数据库链接，并且清理缓存
        """
        if not self.conn:
            self.conn.close()
            self.conn = None

        self.table_dict = {}

    def get_table(self, category, sub):
        """
        获取数据库表
        :param category: 对应excel
        :param sub: 对应sheet
        :return: 返回表实例
        """
        key = category+'##'+sub
        if key not in self.table_dict:
            self.table_dict[key] = WtMysqlTable(self.__load_head(category, sub), self)

        return self.table_dict[key]

    def __load_head(self, category, sub):
        """
        获取数据库表头信息
        :param category: 对应excel
        :param sub: 对应sheet
        :return: 返回表头信息和对应id
        """
        with self.get_conn().cursor() as cur:
            sql_str = 'select id from ar_head where category = %s and sub = %s limit 1'
            cur.execute(sql_str, (category,sub))
            head = cur.fetchone()

            if not head:
                raise WtArError('未找到数据表，{}-{}'.format(category, sub))

            return {
                'id': head[0],
                'category': category,
                'sub': sub,
            }