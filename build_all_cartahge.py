import os
import subprocess
import shutil
import re
import requests

from main import cfg

productor_path = cfg.get('build', 'production_path')
build_path = cfg.get('build', 'build_path')

def download_cartfile():
    file_name = 'Cartfile'
    result = requests.get("""https://raw.githubusercontent.com/bearyinnovative/Mandrake/component/Components/CarthageStore/Cartfile?token=AOcLsCSifLEzfuyY7r_JXqmplY6NCrcSks5bBookwA%3D%3D""")
    if result.status_code != 200:
        print('can not get cartfile')
        return
    with open(file_name, 'wt') as f:
        f.write(result.text)


def build_framework():
    carthage_output = subprocess.check_output('carthage bootstrap --platform iOS --use-ssh', shell=True)
    carthage_output = carthage_output.decode('utf-8')
    all_frameworks = re.findall('Checking out (.*?) at \"(.*?)\"\n', carthage_output)
    return all_frameworks


def zipit(folders, zip_filename):
    import zipfile
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)

    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))

    zip_file.close()


def move_to_production(path):
    for relpath, dirs, files in os.walk(path):
        if relpath.endswith('framework'):
            framework_dir = relpath
            dSYM_dir = framework_dir + '.dSYM'
            zip_file = framework_dir + '.zip'
            zipit([framework_dir, dSYM_dir], zip_file)

            des = os.path.join(productor_path, zip_file.split(os.sep)[-1])
            try:
                os.remove(des)
            except OSError:
                pass
            finally:
                shutil.move(zip_file, productor_path)


def build_cartahge():
    download_cartfile()
    build_framework()
    move_to_production(build_path)

