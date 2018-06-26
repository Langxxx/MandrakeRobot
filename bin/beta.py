# -*- coding: utf-8 -*-
from common import cfg
import subprocess


def execu_cmd(cmd):
    mdk_path = cfg.get('Mandrake', 'path')
    _cmd = "cd {path} && {cmd}".format(path=mdk_path, cmd=cmd)
    return subprocess.check_output(_cmd, shell=True)


def run(consumer):
    consumer.send(None)

    try:
        rebase_dev_cmd = "git reset --hard && git checkout dev && git pull --rebase origin dev"
        consumer.send(execu_cmd(rebase_dev_cmd))

        update_local_pods = "make update_local_pods"
        consumer.send(execu_cmd(update_local_pods))

        beta_cmd = 'export UNLOCK_PWD={pwd} && fastlane beta'
        consumer.send(execu_cmd(beta_cmd))

    except subprocess.SubprocessError as error:
        consumer.send(error.__str__())

    consumer.close()
