import json

from ar.common.WtArError import WtArError
from ar.table.WtTable import WtTable


class WtApiTable(WtTable):
    def __init__(self, config, db):
        super().__init__()
        self.db = db
        self.config = config
        self.cache = {}

    def get(self, mode=0, limit=0):
        key = 'get_' + str(mode)
        if key in self.cache:
            return self.cache[key]

        headers = {'accept-encoding':'gzip'}
        request_data = {'headId': self.config['id']}
        if mode:
            request_data['mode'] = mode
        if limit:
            request_data['limit'] = limit
        r = self.db.get_conn().post(self.db.get_url_prefix() + '/kb/queryBody', data=request_data, headers=headers)
        r = r.json()

        if r['code'] == 0:
            result = []
            for item in r['data']:
                node = json.loads(item['content'])
                node.update({'mode': item['mode']})
                result.append(node)
        else:
            raise WtArError('请求远程接口失败，get:{}'.format(request_data))

        self.cache[key] = result
        return self.cache[key]

    def first(self, mode=0):
        result = self.get(mode, 1)
        if len(result) == 1:
            return result[0]
        return None