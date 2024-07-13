from ar.common.WtArError import WtArError
from ar.db.WtDatabase import WtDatabase
from configs import config


db = None

if not db:
    if WtDatabase().isinstance():
        raise WtArError('database has been instanced')
    
    default_db_config = {
        'mysql': {
            'host': '192.168.0.102',
            'user': '***',
            'passwd': '***',
            'db': 'ar',
            'port': 3307,
            'charset': 'utf8'
        },
        'api': {
            'url': 'http://127.0.0.1:8016/api/v1/web'
        }
    }

    db_type = config.db_type

    WtDatabase().instance(db_type, {**default_db_config[db_type], **config.db_config[db_type]})
    db = WtDatabase()