import os
import time
import subprocess
from common import mdk_path, upload_to_qiuniu


def exec_cmd(cmd, log_as_file=False):
    if log_as_file:
        current_dir_path = os.getcwd()
        log_path = current_dir_path + '/log'
        _cmd = cmd + " > {log}".format(log=log_path)
        subprocess.call(_cmd, shell=True, cwd=mdk_path)
        with open('log', 'r') as f:
            text = f.read()
            if text.find('fastlane finished with errors'):
                current_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
                url = upload_to_qiuniu('./log', current_time + '.log')
                if url:
                    return 'fastlane finished with errors\n log url: ' + url
                else:
                    return 'fastlane finished with error and log upload failure'
            else:
                return 'fastlane finished suceessful'
    else:
        out_log = subprocess.check_output(cmd, shell=True,
                                          stderr=subprocess.STDOUT,
                                          cwd=mdk_path)
        return out_log.decode('utf-8')
