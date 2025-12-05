
import os, json, yaml, pathlib
from scripts.utils.io import ensure_local_cache

CFG = yaml.safe_load(open('configs/data.yaml'))

if __name__ == '__main__':
    root = pathlib.Path('.')
    ensure_local_cache(CFG)
    print('Data cache ensured at', CFG['cache']['local_cache'])
