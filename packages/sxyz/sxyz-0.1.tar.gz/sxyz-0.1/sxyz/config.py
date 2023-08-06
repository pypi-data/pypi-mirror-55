import json
import os


class FileTypeError(BaseException):
    pass


class ConfigError(BaseException):
    pass


# TODO configuration class

def gen_default_config():
    return {
        'general': {
            'default_backend': 'oss',
            'default_expired_days': 0,
            'expired_days_options': [0, 1, 3, 5, 7],
            'valid_filetype': ['image/jpeg', 'image/png', 'image/webp', 'image/gif'],
        },
        'oss': {
            'domain': None,
            'bktname': None,
            'endpoint': None,
            'access_key': None,
            'secret': None,
            'https': False,
        },
        'qiniu': {
            'domain': None,
            'bktname': None,
            'access_key': None,
            'secret': None,
            'https': False
        },
        'gitee': {
            'access_token': None,
            'username': None,
            'repo': None
        }
    }


def auto_load():
    for f in find_path:
        if os.path.exists(f):
            load_file(f)
            return
    raise ConfigError('no configuration file found')


def default_expired_days():
    return get_config()['general']['default_expired_days']


def expired_days_options():
    return get_config()['general']['expired_days_options']


def load_file(fn):
    global _config_file
    if _config_file is not None:
        raise ConfigError(
            'attempting to load multiple config files: {}'.format(fn))
    _config_file = fn
    with open(fn) as fp:
        _load(fp)


def dump_file(fn):
    with open(fn, 'w') as fp:
        _dump(fp)


def load_str(s):
    get_config().update(json.loads(s))


def dump_str():
    return json.dumps(get_config(),
                      indent=4, ensure_ascii=False)


def dump_default_config():
    return json.dumps(gen_default_config(),
                      indent=4, ensure_ascii=False)


def dump_back_config_file():
    if _config_file is None:
        raise ConfigError('no config file using')
    dump_file(_config_file)


def _load(fp):
    get_config().update(json.load(fp))


def _dump(fp):
    json.dump(get_config(), fp,
              sort_keys=True, indent=4, ensure_ascii=False)


def check_and_split_key(key):
    """
    Check if :param key: is valid.
    :return: Then return (subconfig, key) tuple if it's a subconfig key(colon-divied),
    or return (key, None) tuple if it's a general key.
    """
    if ':' in key:
        try:
            sub, key1 = key.split(':')
            _ = get_config()[sub][key1]  # get test
        except (KeyError, ValueError):
            raise ConfigError('error config key: {}'.format(key))
        return sub, key1
    else:
        try:
            _ = get_config()['general'][key]  # get test
        except (KeyError, ValueError):
            raise ConfigError('error config key: {}'.format(key))
        return key, None


def get_config():
    return _config


def set_key(k, v):
    sub, key = check_and_split_key(k)
    if key is None:
        key = sub
        sub = 'general'

        # process special value
        if k == 'expired_days_options':
            v = v.split(',')
            v = map(lambda s: s.strip(), v)
            v = filter(lambda s: s, v)
            v = list(v)
        elif k == 'valid_filetype':
            v = v.split(',')
            v = map(lambda s: s.strip(), v)
            v = filter(lambda s: s, v)
            v = list(v)
    get_config()[sub][key] = v


def get_key(k):
    sub, key = check_and_split_key(k)
    if key is None:
        key = sub
        sub = 'general'

        v = get_config()[sub][key]
        # process special value
        if k == 'expired_days_options':
            v = map(lambda i: str(i), v)
            return ', '.join(v)
        elif k == 'valid_filetype':
            return ', '.join(v)
    return get_config()[sub][key]


find_path = [
    'sxyz.json',
]

_config_file = None
_config = gen_default_config()


def use_default_config(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _config
        tmp = _config
        _config = gen_default_config()
        f(*args, **kwargs)
        _config = tmp

    return wrapper


@use_default_config
def test_get_key():
    assert get_key('expired_days_options') == '1, 3, 5, 7'


@use_default_config
def test_set_key():
    set_key('oss:secret', 'secret1')
    assert get_key('oss:secret') == 'secret1'
    set_key('expired_days_options', '1,2,3,4')
    assert get_key('expired_days_options') == '1, 2, 3, 4'


def test_dump():
    s = '''{
    "general": {
        "default_backend": "oss",
        "default_expired_days": 1,
        "expired_days_options": [
            1,
            3,
            5,
            7
        ],
        "valid_filetype": [
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif"
        ]
    },
    "oss": {
        "domain": null,
        "bktname": null,
        "endpoint": null,
        "access_key": null,
        "secret": null,
        "https": false
    },
    "qiniu": {},
    "gitee": {}
}'''
    from io import StringIO

    fp = StringIO()
    _dump(fp)
    fp.seek(0)
    # print(s)
    # print(fp.read())
    assert fp.read() == s


@use_default_config
def test_load():
    from io import StringIO
    s = '''{
        "general": {
            "default_backend": "gitee",
            "default_expired_days": 2,
            "expired_days_options": [1, 2],
            "valid_filetype": ["image/gif"]
        },
        "oss": {
            "domain": "domain1",
            "bktname": "bktname",
            "endpoint": null,
            "access_key": null,
            "secret": null,
            "https": false
        },
        "qiniu": {},
        "gitee": {}
    }'''

    fp = StringIO(s)
    _load(fp)
    assert get_key('default_backend') == 'gitee'
    assert get_key('default_expired_days') == 2
    assert get_key('expired_days_options') == '1, 2'
    assert get_key('valid_filetype') == 'image/gif'
    assert get_key('oss:domain') == 'domain1'


if __name__ == '__main__':
    test_get_key()
    test_set_key()
    # test_dump()
    test_load()
