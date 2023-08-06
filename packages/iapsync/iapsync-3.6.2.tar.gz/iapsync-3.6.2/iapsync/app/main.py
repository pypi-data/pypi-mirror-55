#! /usr/bin/env python3

import argparse
from iapsync.model.product import XML_NAMESPACE
from iapsync.app.actions import actions
from iapsync.utils.args import extract_params
from iapsync.utils.mail import send_notify_mail
from iapsync.config.config import APP_VER
from iapsync.utils.version import check_new_version


def main():
    ''' Entry point '''
    parser = argparse.ArgumentParser(
        description='''iapsync({appVersion})
    关于mode：
        -m sync: fetch from api defined by --config-file, generate itmsp package, for uploading to itunesconnect
        -m verify: first do the work of sync mode, then verify generated itmsp package by sync mode
        -m upload: first do the work of verify, then upload generated itmsp package to itunes connect by sync mode
        '''.format(appVersion=APP_VER),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-c', '--config-file')
    parser.add_argument('-m', '--mode', choices=['sync', 'verify', 'upload'])
    parser.add_argument('-e', '--target-env', default='all', type=str, choices=['dev', 'sim', 'prod'])
    parser.add_argument('--force-update', default=False, type=bool)
    parser.add_argument('--send-mail', default=False, type=bool)
    parser.add_argument('--skip-appstore', default=False, type=bool, help='使用本地目录已有的数据，可以加快sync操作的速度')
    parser.add_argument('--itms', type=str, default='', help='path to iTMSTransporter binary')
    parser.add_argument('--log-level', default='informational', choices=['off', 'detailed', 'informational', 'critical', 'eXtreme'], type=str)
    parser.add_argument('--skip-mode', default='none', choices=['sync', 'verify', 'upload', 'none'])
    parser.add_argument('--sock-port', default='none', help='Local socket server port, used to upload things to appsync, optional.')
    parser.add_argument('--task-id', default='none', help='Task identifier, optional.')
    parser.add_argument('--output-dir', default='none', help='Directory to put temporaty files.')
    parser.add_argument('--lock-file', default='none', help='File to lock upload, making it serial.')
    parser.add_argument('--fix-screenshots', default=False, type=bool)
    parser.add_argument('--ceil-price', default=False, type=bool)
    parser.add_argument('--dry-run', default=False, type=bool)
    parser.add_argument('-v', '--verbose', default=False, type=bool)
    parser = parser.parse_args()

    new_version = check_new_version()
    if new_version:
        print('New version(%s) available!' % new_version)
    params = extract_params(parser)
    steps = actions[parser.mode]
    agg_ret = None
    for step in steps:
        agg_ret = step(params, {'namespaces': {'x': XML_NAMESPACE}}, agg_ret)
    # 邮件通知
    if params['send_mail'] and not params['dry_run']:
        print('Send mail...')
        send_notify_mail(agg_ret, params)
    else:
        print('No send mail.')
