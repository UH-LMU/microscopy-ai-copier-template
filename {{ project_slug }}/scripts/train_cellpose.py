
import argparse, yaml, pathlib, subprocess, time, json, sys
from dvclive import Live

parser = argparse.ArgumentParser()
parser.add_argument('--config', required=True)
parser.add_argument('--tool', choices=['cellpose3','cellpose4'], required=True)
args = parser.parse_args()

cfg = yaml.safe_load(open(args.config))
run_dir = pathlib.Path('outputs/runs')/f"{time.strftime('%Y%m%d-%H%M%S')}_{args.tool}"
run_dir.mkdir(parents=True, exist_ok=True)

# snapshot
(pathlib.Path(run_dir)/'config.snapshot.yaml').write_text(open(args.config).read())

# Very thin wrapper – call cellpose CLI depending on tool
cmd = [sys.executable, '-m', 'cellpose', '--train',
       '--dir', cfg['data']['images_dir'], '--train_mask_dir', cfg['data']['labels_dir']]

if args.tool == 'cellpose3':
    cmd += ['--pretrained_model', cfg['model']['pretrained'], '--chan', str(cfg['data'].get('chan',0)), '--chan2', str(cfg['data'].get('chan2',0))]
else:
    # cellpose4 may use diameter or cpsam etc.
    if 'diameter' in cfg['data']:
        cmd += ['--diameter', str(cfg['data']['diameter'])]

cmd += ['--n_epochs', str(cfg['train']['epochs'])]

print('Running:', ' '.join(cmd))
ret = subprocess.run(cmd)

live = Live()
live.log_metric('train_exit_code', ret.returncode)
live.next_step()

(pathlib.Path(run_dir)/'exitcode.txt').write_text(str(ret.returncode))
