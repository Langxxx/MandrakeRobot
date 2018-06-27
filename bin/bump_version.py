# -*- coding: utf-8 -*-
from bin.beta import execu_cmd


def run(consumer):
    consumer.send(None)

    bump_cmd = 'fastlane increment_build_number_then_commit'
    consumer.send(bump_cmd)
    execu_cmd(bump_cmd)
    consumer.send(execu_cmd('git log -1'))

    push_cmd = 'git push origin dev'
    consumer.send(push_cmd)
    consumer.send(execu_cmd(push_cmd))

    consumer.close()
