# -*- coding: utf-8 -*-
from common import cfg, production
from bin.common import exec_cmd
from subprocess import SubprocessError

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


@production
def run(consumer):
    try:
        rebase_dev_cmd = "git reset --hard && git checkout dev && git pull --rebase origin dev"
        consumer.send(rebase_dev_cmd)
        consumer.send(exec_cmd(rebase_dev_cmd))

        update_local_pods = "make update-local-pods"
        consumer.send(update_local_pods)
        consumer.send(exec_cmd(update_local_pods))

        pod_install = "pod install"
        consumer.send(pod_install)
        consumer.send(exec_cmd(pod_install))

        beta_cmd = "UNLOCK_PWD={pwd} && fastlane beta".format(pwd=cfg.get('main', 'unlock_pwd'))
        consumer.send('fastlane beta')
        consumer.send(exec_cmd(beta_cmd, True))

    except SubprocessError as error:
        consumer.send(error.__str__())

