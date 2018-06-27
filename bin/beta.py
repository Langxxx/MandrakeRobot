# -*- coding: utf-8 -*-
from common import cfg
import subprocess
import os


def execu_cmd(cmd, log_as_file=False):
    mdk_path = cfg.get('Mandrake', 'path')
    if log_as_file:
        current_dir_path = os.getcwd()
        log_path = current_dir_path + '/log'
        _cmd = cmd + " > {log}".format(log=log_path)
        subprocess.call(_cmd, shell=True, cwd=mdk_path)
        with open('log', 'r') as f:
            text = f.read()
            if text.find('fastlane finished with errors'):
                return 'fastlane finished with errors'
            else:
                return 'fastlane finished suceessful'
    else:
        out_log = subprocess.check_output(cmd, shell=True, \
                                          stderr=subprocess.STDOUT, \
                                          cwd=mdk_path)
        return out_log.decode('utf-8')


# def fastlane_cmd(cmd):
    # mdk_path = cfg.get('Mandrake', 'path')
    # current_dir_path = os.getcwd()
    # log_path = current_dir_path + '/log'
    # _cmd = cmd + " > {log}".format(log=log_path)
    # subprocess.call(_cmd, shell=True, cwd=mdk_path)
    # with open('log', 'r') as f:
        # text = f.read()
        # if text.find('fastlane finished with errors'):
            # return 'fastlane finished with errors'
        # else:
            # return 'fastlane finished suceessful'


def run(consumer):
    consumer.send(None)

    try:
        # rebase_dev_cmd = "git reset --hard && git checkout dev && git pull --rebase origin dev"
        # consumer.send(rebase_dev_cmd)
        # consumer.send(execu_cmd(rebase_dev_cmd))

        # update_local_pods = "make update-local-pods"
        # consumer.send(update_local_pods)
        # consumer.send(execu_cmd(update_local_pods))

        # pod_install = "pod install"
        # consumer.send(pod_install)
        # consumer.send(execu_cmd(pod_install))

        beta_cmd = "UNLOCK_PWD={pwd} && fastlane beta".format(pwd=cfg.get('main', 'unlock_pwd'))
        consumer.send('fastlane beta')
        consumer.send(execu_cmd(beta_cmd, True))

    except subprocess.SubprocessError as error:
        consumer.send(error.__str__())

    consumer.close()
