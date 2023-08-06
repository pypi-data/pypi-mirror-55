#! /usr/bin/env python3

import argparse
import sys

from . import backend
from . import config


def cmd_upload(file, _backend, expired_days, init_backend):
    if _backend is None:
        _backend = config.get_key('default_backend')
    if expired_days is None:
        expired_days = config.get_key('default_expired_days')
    expired_days = int(expired_days)
    be = backend.choose(_backend)
    be.load_config(config.get_config())
    if init_backend:
        be.init_remote()
    url = be.upload(file, expired_days)
    print(url)
    return True


def cmd_config(key, value, dump_default, dump_all):
    if dump_default:
        print(config.dump_default_config())
        return True
    if dump_all:
        print(config.dump_str())
        return True

    # changing configuration
    if key and value:
        config.set_key(key, value)
        config.dump_back_config_file()
        return True
    elif key and not value:
        print('{}: {}'.format(key, config.get_key(key)))
        config.dump_back_config_file()
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser('sxyz')
    parser.add_argument('-f', '--config-file', action='store',
                        help='specify configuration file')

    subparser = parser.add_subparsers(dest='command')

    subconfig = subparser.add_parser('config',
                                     help='set or get a config item')
    subconfig.add_argument('-k', '--key')
    subconfig.add_argument('-v', '--value')
    subconfig.add_argument('-d', '--dump-default', action='store_true',
                           help='dump default configurations to stdout')
    subconfig.add_argument('-a', '--dump-all', action='store_true',
                           help='dump all configurations to stdout')

    subupload = subparser.add_parser('upload', help='upload file')
    subupload.add_argument('file', help='file to upload')
    subupload.add_argument('--backend',
                           help='choose a backend [available: oss, qiniu, gitee]')
    subupload.add_argument('--expired-days',
                           help='file \'s expired days')
    subupload.add_argument('--init-backend', action='store_true',
                           help='initialize the backend')

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    if args.command == 'config' and args.dump_default:
        # User trying dump a default config file,
        # loading config file could be failed.
        cmd_config(None, None,
                   args.dump_default, None)
        sys.exit(0)
    elif args.config_file is not None:
        config.load_file(args.config_file)
    else:
        config.auto_load()

    if args.command == 'config':
        if not cmd_config(args.key, args.value,
                          args.dump_default, args.dump_all):
            subconfig.print_help()
            sys.exit(0)
    elif args.command == 'upload':
        if not cmd_upload(args.file, args.backend, args.expired_days,
                          args.init_backend):
            subconfig.print_help()
            sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('sxyz')
    parser.add_argument('-f', '--config-file', action='store',
                        help='specify configuration file')

    subparser = parser.add_subparsers(dest='command')

    subconfig = subparser.add_parser('config',
                                     help='set or get a config item')
    subconfig.add_argument('-k', '--key')
    subconfig.add_argument('-v', '--value')
    subconfig.add_argument('-d', '--dump-default', action='store_true',
                           help='dump default configurations to stdout')
    subconfig.add_argument('-a', '--dump-all', action='store_true',
                           help='dump all configurations to stdout')

    subupload = subparser.add_parser('upload', help='upload file')
    subupload.add_argument('file', help='file to upload')
    subupload.add_argument('--backend',
                           help='choose a backend [available: oss, qiniu, gitee]')
    subupload.add_argument('--expired-days',
                           help='file \'s expired days')
    subupload.add_argument('--init-backend', action='store_true',
                           help='initialize the backend')

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    if args.command == 'config' and args.dump_default:
        # User trying dump a default config file,
        # loading config file could be failed.
        cmd_config(None, None,
                   args.dump_default, None)
        sys.exit(0)
    elif args.config_file is not None:
        config.load_file(args.config_file)
    else:
        config.auto_load()

    if args.command == 'config':
        if not cmd_config(args.key, args.value,
                          args.dump_default, args.dump_all):
            subconfig.print_help()
            sys.exit(0)
    elif args.command == 'upload':
        if not cmd_upload(args.file, args.backend, args.expired_days,
                          args.init_backend):
            subconfig.print_help()
            sys.exit(0)
