# -*- coding: utf-8 -*-
import os
from common import production


@production
def run(consumer):
    cmd = []
    for file in os.listdir('./bin/'):
        if file.endswith('.py') and file != '__init__.py':
            cmd.append(file[:-3])
    consumer.send('\n'.join(cmd))

