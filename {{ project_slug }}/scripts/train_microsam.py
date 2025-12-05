
import argparse, yaml, pathlib, time, json
from dvclive import Live

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
args = parser.parse_args()

cfg = yaml.safe_load(open(args.config))
run_dir = pathlib.Path('outputs/runs')/f"{time.strftime('%Y%m%d-%H%M%S')}_microsam"
run_dir.mkdir(parents=True, exist_ok=True)

# Placeholder: wire your micro-SAM finetuning here
metrics = {"train_loss": 0.0}

live = Live()
for k,v in metrics.items():
    live.log_metric(k, v)
live.next_step()

(run_dir/'config.snapshot.yaml').write_text(open(args.config).read())
(run_dir/'metrics.json').write_text(json.dumps(metrics, indent=2))
print('Wrote placeholder run to', run_dir)
