
import argparse, yaml, pathlib, time, json
from dvclive import Live

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
parser.add_argument('--split', required=True)
args = parser.parse_args()

cfg = yaml.safe_load(open(args.config))

# minimal pseudo test – replace with real inference
live = Live()
start = time.time()
# ... run inference here ...
metrics = {"dice": 0.0, "iou": 0.0, "latency_s": time.time()-start}
for k,v in metrics.items():
    live.log_metric(k, v)
live.next_step()

# also drop a run-local copy
run_dir = pathlib.Path('outputs/runs')/time.strftime('%Y%m%d-%H%M%S_test')
run_dir.mkdir(parents=True, exist_ok=True)
(run_dir/'metrics.json').write_text(json.dumps(metrics, indent=2))
print('Wrote metrics to', run_dir)
