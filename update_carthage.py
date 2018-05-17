import argparse
import subprocess

import re

from build_all_cartahge import download_cartfile, move_to_production, build_path


def build_carthage(names):
    cmd = 'carthage update {names} --platform iOS --use-ssh'.format(names=names)
    carthage_output = subprocess.check_output(cmd, shell=True)
    carthage_output = carthage_output.decode('utf-8')
    all_frameworks = re.findall('Checking out (.*?) at \"(.*?)\"\n', carthage_output)
    return all_frameworks


def update_carthage(names):
    names = ' '.join(names.split(',')).strip()
    if not names:
        raise argparse.ArgumentError(message='miss framework name eg: A,B,C')

    download_cartfile()
    build_carthage(names)
    move_to_production(build_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='names')
    result = parser.parse_args()
    update_carthage(result.names)
