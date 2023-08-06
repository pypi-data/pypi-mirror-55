"""
https://pyyaml.org/wiki/PyYAMLDocumentation
"""

from .finder import find
import yaml

def _read_yaml(yaml_file):
    with open(yaml_file) as f:
        d = yaml.load(f.read(), Loader=yaml.FullLoader)
    return d

def yml(argv):
    root_dir = ''
    if len(argv) > 0: root_dir = argv[0]
    fps = find('*.yaml', root_dir)
    if len(fps):
        print(yaml.dump(fps))
    print('total: {}'.format(len(fps)))
