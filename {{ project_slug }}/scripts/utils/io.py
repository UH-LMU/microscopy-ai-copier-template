
import os, shutil, pathlib, json
from typing import Dict

try:
    import fsspec
except ImportError:
    fsspec = None


def ensure_local_cache(cfg: Dict):
    cache = pathlib.Path(cfg['cache']['local_cache'])
    cache.mkdir(parents=True, exist_ok=True)


def open_uri(uri: str, mode='rb'):
    if uri.startswith('s3://') or uri.startswith('file://'):
        if fsspec is None:
            raise RuntimeError('fsspec is required for non-local URIs')
        fs, path = fsspec.core.url_to_fs(uri)
        return fs.open(path, mode)
    p = pathlib.Path(uri)
    return open(p, mode)

