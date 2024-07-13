from ar.common.WtArError import WtArError
from ar.db.WtDatabaseApiImp import WtDatabaseApiImp
from ar.db.WtDatabaseMysqlImp import WtDatabaseMysqlImp
from ar.common.singleton import singleton

"""
数据库实例，用于获取知识库中的所有数据
数据库结构：
WtDatabase -> WtTable

具体结构同Excel，
category 对应单个excel
sub      对应单个sheet 
"""


@singleton
class WtDatabase:
    def __init__(self):
        self.db_imp = None
        
    def isinstance(self):
        return self.db_imp != None

    def instance(self, t, config):
        """
        配置数据库连接信息
        :param t: str
        :param config: dict
        """

        if t == 'mysql':
            self.db_imp = WtDatabaseMysqlImp()
        elif t == 'api':
            self.db_imp = WtDatabaseApiImp()
        else:
            raise WtArError('无效类型：{}'.format(t))

        self.db_imp.set_db_info(config)

    def close(self):
        if self.db_imp:
            self.db_imp.close()
        else:
            raise WtArError('database not instance')

    def get_table(self, category, sub):
        """
        获取数据库表
        :param category: str 数据库名称，和Excel对应
        :param sub: str 表格名称，和sheet对应
        :return: WtTable
        """
        if self.db_imp:
            return self.db_imp.get_table(category, sub)
        else:
            raise WtArError('database not instance')



