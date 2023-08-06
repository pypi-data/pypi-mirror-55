import os

import oss2
import qiniu
import requests

from . import config
from . import utils


class BackendError(BaseException):
    pass


class Backend:

    def load_config(self, conf: dict) -> None:
        """
        load config from :param conf:
        :param conf: configurations including the needed configurations
        """
        raise NotImplementedError

    def init_remote(self):
        """
        init the remote storage, such as setup expiration rules
        """
        raise NotImplementedError

    def upload(self, filename: str, expire_days=None) -> str:
        """
        upload the file :param filename: and return its url
        :param filename: filename to upload
        :param expire_days: expire days
        :return: generated url
        """
        raise NotImplementedError


class OSS(Backend):

    def __init__(self):
        self.auth = None
        self.bucket = None
        self.domain = None
        self.https = False

    @property
    def protocol(self):
        return 'https' if self.https else 'http'

    def load_config(self, conf: dict) -> None:
        """
        full configuration:
        {'oss': {
            'domain': 'str optional',
            'bktname': 'str required',
            'endpoint': 'str required',
            'access_key': 'str required',
            'secret': 'str required',
            'https': 'bool optional'
        }}
        :param conf: global configuration
        """
        conf = conf.get('oss')
        if conf is None:
            raise BackendError('no oss config specified')

        conf = {k: v for k, v in conf.items() if v is not None}  # remove None
        domain = conf.get('domain')
        https = conf.get('https', False)
        try:
            bktname = conf['bktname']
            endpoint = conf['endpoint']
            access_key = conf['access_key']
            secret = conf['secret']
        except KeyError as e:
            raise BackendError('\'{}\' is required in oss config'.format(e.args[0]))

        if domain is None:
            domain = bktname + '.' + endpoint
        self.https = https
        self.domain = domain
        self.auth = oss2.Auth(access_key, secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bktname)

    def init_remote(self):
        rules = []
        for day in config.expired_days_options():
            if day == 0:
                continue
            rule = oss2.models.LifecycleRule(
                'expire_{}'.format(day),
                self.gen_expire_prefix(day),
                status=oss2.models.LifecycleRule.ENABLED,
                expiration=oss2.models.LifecycleExpiration(days=day)
            )
            rules.append(rule)
        self.bucket.put_bucket_lifecycle(oss2.models.BucketLifecycle(rules))

    def upload(self, filename: str, expire_days=None):
        if expire_days is None:
            expire_days = config.default_expired_days()
        assert expire_days is not None
        options = config.expired_days_options()
        if expire_days not in config.expired_days_options():
            raise BackendError(
                '{} is not in expired days options {}'.format(expire_days, options))

        filetype = utils.check_filetype(filename)
        headers = oss2.CaseInsensitiveDict({'ContentType': filetype})
        filekey = 'sxyz/{}/{}'.format(
            self.gen_expire_prefix(expire_days),
            utils.gen_random_filename()
        )
        self.bucket.put_object_from_file(filekey, filename, headers=headers)
        return '{}://{}/{}'.format(self.protocol, self.domain, filekey)

    @staticmethod
    def gen_expire_prefix(expire_days):
        return '{}'.format(expire_days)


class Qiniu(Backend):

    def __init__(self):
        self.auth = None
        self.bkt_mgr = None
        self.https = False
        self.domain = None
        self.bktname = None

    @property
    def protocol(self):
        return 'https' if self.https else 'http'

    def load_config(self, conf: dict) -> None:
        """
        funn configuration:
        { 'qiniu': {
            'domain': 'str',
            'bktname': 'str',
            'access_key': 'str',
            'secret': 'str',
            'https': 'bool'
        }}
        :param conf: global configurations
        """
        conf = conf.get('qiniu')
        if conf is None:
            raise BackendError('no qiniu config specified')

        conf = {k: v for k, v in conf.items() if v is not None}  # remove None
        https = conf.get('https', False)
        try:
            domain = conf['domain']
            bktname = conf['bktname']
            access_key = conf['access_key']
            secret = conf['secret']
        except KeyError as e:
            raise BackendError('\'{}\' is required in qiniu config'.format(e.args[0]))
        self.https = https
        self.domain = domain
        self.bktname = bktname
        self.auth = qiniu.Auth(access_key, secret)
        self.bkt_mgr = qiniu.BucketManager(self.auth)

    def init_remote(self):
        pass

    def upload(self, filename: str, expire_days=None) -> str:
        if expire_days is None:
            expire_days = config.default_expired_days()
        assert expire_days is not None
        options = config.expired_days_options()
        if expire_days not in options:
            raise BackendError(
                '{} is not in expired days options {}'.format(expire_days, options))

        filetype = utils.check_filetype(filename)
        filekey = 'sxyz/{}'.format(utils.gen_random_filename())
        upload_token = self.auth.upload_token(self.bktname, filekey, 300)
        ret, info = qiniu.put_file(upload_token, filekey, filename, mime_type=filetype)
        if info.status_code != 200:
            raise BackendError('upload file error ({}): {}'.format(filename, info.error))
        self.set_expired_days(filekey, expire_days)
        return '{}://{}/{}'.format(self.protocol, self.domain, filekey)

    def set_expired_days(self, filekey, days):
        if int(days) == 0:
            return
        ret, info = self.bkt_mgr.delete_after_days(self.bktname, filekey, str(days))
        if info.status_code != 200:
            raise BackendError('set expired days error ({}): {}'.format(filekey, info.error))

    @staticmethod
    def gen_expire_prefix(expire_days):
        return '{}'.format(expire_days)


class Gitee(Backend):
    baseurl = 'https://gitee.com/api'

    def __init__(self):
        self.token = None
        self.username = None
        self.repo = None

    def init_remote(self):
        pass

    def load_config(self, conf: dict) -> None:
        """
        full configurations:
        {
            'access_token': 'token',
            'username': 'username',
            'repo': 'repo'
        }
        :param conf: configuration dict
        """
        conf = conf.get('gitee')
        if conf is None:
            raise BackendError('no gitee config specified')

        try:
            token = conf['access_token']
            username = conf['username']
            repo = conf['repo']
        except KeyError as e:
            raise BackendError('\'{}\' is required in gitee config'.format(e.args[0]))
        self.token = token
        self.username = username
        self.repo = repo

    def upload(self, filename: str, expire_days=None) -> str:
        filetype = utils.check_filetype(filename)
        localname = os.path.basename(filename)  # file name in local
        remotename = 'sxyz/{}.{}'.format(
            utils.gen_random_filename(),
            utils.get_file_ext(filetype)
        )
        content = utils.b64encode_file(filename)
        resp = requests.post(
            '{}/v5/repos/{}/{}/contents/{}'.format(self.baseurl, self.username, self.repo, remotename),
            data={
                'access_token': self.token,
                'content': content,
                'message': 'upload {}'.format(localname)
            }
        )
        resp.raise_for_status()
        return resp.json()['content']['download_url']


def choose(backend):
    if backend == 'oss':
        return OSS()
    elif backend == 'gitee':
        return Gitee()
    elif backend == 'qiniu':
        return Qiniu()
    else:
        raise BackendError('unsupported backend: {}'.format(backend))


if __name__ == '__main__':
    pass
