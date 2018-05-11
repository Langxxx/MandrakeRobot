import argparse
from build_all_frameworks import move_to_production
import subprocess

from main import cfg


def _build(path):
   subprocess.call('cd ' + path + '&& carthage build --no-skip-current --platform iOS', shell=True)


def build_component(name):
   path = cfg.get(name, 'path')
   _build(path)
   move_to_production(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='name')
    result = parser.parse_args()
    build_component(result.name)
