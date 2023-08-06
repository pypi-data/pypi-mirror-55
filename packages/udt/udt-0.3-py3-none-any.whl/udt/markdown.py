from .finder import find, strip_dir
import yaml

def markdown(argv):
    root_dir = ''
    if len(argv) > 0: root_dir = argv[0]
    fps = find('*.md', root_dir)
    if len(fps):
        print(yaml.dump(fps))
    print('total: {}'.format(len(fps)))
