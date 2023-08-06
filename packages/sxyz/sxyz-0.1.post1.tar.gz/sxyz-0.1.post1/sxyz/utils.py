import mimetypes
from base64 import b64encode
from uuid import uuid4

from . import config
from .config import FileTypeError


def guess_filetype(filename):
    """
    :param filename: file to guess
    :return: file's mimetype on type/subtype form
    """
    return mimetypes.guess_type(filename)[0]


def check_filetype(filename):
    """
    check if the file is valid
    according: mimetype
    :param filename: file to check
    :return: True if valid, else False
    """
    guess = guess_filetype(filename)
    if guess not in config.get_key('valid_filetype'):
        raise FileTypeError('unsupported type of file: ' + guess)
    return guess


def get_file_ext(filetype):
    """
    get extname according filetype
    :param filetype: filetype (in config.get_key('valid_filetype'))
    :return: file's extend name
    """
    return {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/webp': 'webp',
        'image/gif': 'gif'
    }[filetype]


def gen_random_filename():
    return uuid4().hex


def b64encode_file(fn):
    with open(fn, 'rb') as fp:
        return _b64encode_file(fp)


def _b64encode_file(fp):
    return b64encode(fp.read()).decode('ascii')
