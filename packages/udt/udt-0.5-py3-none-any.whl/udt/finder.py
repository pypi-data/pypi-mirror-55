import glob
from os import path

def find(file_pattern, root_dir=''):
    return glob.glob(path.join(root_dir, '**', file_pattern), recursive=True)

def strip_dir(fps):
    return [path.basename(fp) for fp in fps]
