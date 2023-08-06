from .finder import find, strip_dir
import yaml

def ls(argv):
    suffix = argv[0] if len(argv) > 0 else '*'
    root_dir = argv[1] if len(argv) > 1 else ''
    fps = find('*.{}'.format(suffix), root_dir)
    if len(fps):
        print(yaml.dump(fps))
    print('total: {}'.format(len(fps)))
