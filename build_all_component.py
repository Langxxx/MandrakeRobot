import build_component
from . import *

def build_all_component():
    for name in ['MandrakeLib', 'MandrakeMisc', 'MDKMessage', 'MDKDiscardableList', 'MDKContact', 'MDKMe']:
        path = cfg.get(name, 'path')
        build_component(path)
