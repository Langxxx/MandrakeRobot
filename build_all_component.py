from build_component import build_component


def build_all_component():
    for name in ['MandrakeLib', 'MandrakeMisc', 'MDKMessage', 'MDKDiscardableList', 'MDKContact', 'MDKMe']:
        build_component(name)

