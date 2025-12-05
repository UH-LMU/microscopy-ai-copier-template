
import argparse, pathlib, json
parser = argparse.ArgumentParser()
parser.add_argument('--runs', default='outputs/runs')
args = parser.parse_args()

runs = sorted(pathlib.Path(args.runs).glob('*'))
print('Found runs:')
for r in runs:
    mj = r/'metrics.json'
    if mj.exists():
        print(r.name, json.loads(mj.read_text()))
    else:
        print(r.name, '(no metrics)')
