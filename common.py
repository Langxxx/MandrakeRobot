from configparser import ConfigParser
from qiniu import Auth, put_file, etag


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


if __name__ == '__main__':
    upload_to_qiuniu('log', 'test_file')
