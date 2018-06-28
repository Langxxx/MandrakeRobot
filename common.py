from configparser import ConfigParser
from qiniu import Auth, put_file, etag
from functools import wraps
from types import GeneratorType


cfg = ConfigParser()
cfg.read('.config.ini')
mdk_path = cfg.get('Mandrake', 'path')


def upload_to_qiuniu(file, name):
    access_key = cfg.get('main', 'access_key')
    secret_key = cfg.get('main', 'secret_key')
    bucket_name = cfg.get('main', 'bucket_name')

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, name, 3600)

    ret, info = put_file(token, name, file)
    if ret['key'] == name and ret['hash'] == etag(file):
        qiniu_url = cfg.get('main', 'qiniu_base_url')
        return qiniu_url + '/' + name
    else:
        return None


class ParameterError(Exception):
    def __str__(self):
        return "miss generator"


def production(f):
    @wraps(f)
    def decorated_function(*arg, **kwargs):
        consumer = None
        for s in arg:
            if isinstance(s, GeneratorType):
                consumer = s
                break
        if consumer:
            consumer.send(None)
            f(*arg, **kwargs)
            consumer.close()
        else:
            raise ParameterError()

    return decorated_function


if __name__ == '__main__':
    upload_to_qiuniu('log', 'test_file')
