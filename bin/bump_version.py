# -*- coding: utf-8 -*-
from bin.beta import exec_cmd
from common import production


@production
def run(consumer):
    rebase_dev_cmd = "git reset --hard && git checkout dev && git pull --rebase origin dev"
    consumer.send(rebase_dev_cmd)
    consumer.send(exec_cmd(rebase_dev_cmd))

    bump_cmd = 'fastlane increment_build_number_then_commit'
    consumer.send(bump_cmd)
    exec_cmd(bump_cmd)
    consumer.send(exec_cmd('git log -1'))

    push_cmd = 'git push origin dev'
    consumer.send(push_cmd)
    consumer.send(exec_cmd(push_cmd))
