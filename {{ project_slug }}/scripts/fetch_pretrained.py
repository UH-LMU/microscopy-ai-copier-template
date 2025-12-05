
import argparse, pathlib, urllib.request, os

URLS = {
  'sam_vit_b': 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth',
  'cellpose_cyto3': 'https://raw.githubusercontent.com/mouseland/cellpose/main/models/cyto3'  # small pointer example
}

parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True, choices=list(URLS.keys()))
parser.add_argument('--dest', required=True)
args = parser.parse_args()

dest = pathlib.Path(args.dest)
dest.mkdir(parents=True, exist_ok=True)

url = URLS[args.model]
name = url.split('/')[-1]
fp = dest/name
print('Downloading', url, '->', fp)
urllib.request.urlretrieve(url, fp)
print('Done')
