# -*- coding: utf-8 -*-
import os
# from common import mdk_path


def run(consumer):
    consumer.send(None)
    cmd = []
    for file in os.listdir('./bin/'):
        if file.endswith('.py') and file != '__init__.py':
            cmd.append(file[:-3])
    consumer.send('\n'.join(cmd))
    consumer.close()

