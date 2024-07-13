import json

from ar.table.WtTable import WtTable


class WtMysqlTable(WtTable):
    def __init__(self, config, db):
        super().__init__()
        self.db = db
        self.config = config
        self.cache = {}

    def get(self, mode=0, limit=0):
        key = 'get_' + str(mode)
        if key in self.cache:
            return self.cache[key]

        sql_str = 'select content,mode from ar_body where headId={}'.format(self.config['id'])

        if mode:
            sql_str += ' and mode={}'.format(mode)

        if limit:
            sql_str += ' limit ' + str(limit)

        with self.db.get_conn().cursor() as cur:
            cur.execute(sql_str)
            data = cur.fetchall()

        result = []
        for item in data:
            node = json.loads(item[0])
            node.update({'mode': item[1]})
            result.append(node)

        self.cache[key] = result
        return self.cache[key]

    def first(self, mode=0):
        result = self.get(mode, 1)
        if len(result) == 1:
            return result[0]
        return None
