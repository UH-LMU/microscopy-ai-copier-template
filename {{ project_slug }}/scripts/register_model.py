
import argparse, pathlib, hashlib, csv, os, subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)
parser.add_argument('--name', required=True)
args = parser.parse_args()

p = pathlib.Path(args.path)
sha256 = hashlib.sha256(p.read_bytes()).hexdigest()
reg = pathlib.Path('models/registry.csv')
reg.parent.mkdir(parents=True, exist_ok=True)
exists = reg.exists()
with reg.open('a', newline='') as f:
    w = csv.writer(f)
    if not exists:
        w.writerow(['name','file','sha256'])
    w.writerow([args.name, str(p), sha256])

# Stage with DVC if available
try:
    subprocess.run(['dvc','add',str(p)], check=False)
except FileNotFoundError:
    pass
print('Registered', args.name, '->', p)
