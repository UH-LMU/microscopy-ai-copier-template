
# Thin wrapper to call UH-LMU/plate-sampler if installed
import argparse, subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--strategy', default='stratified')
parser.add_argument('--out', default='data/splits/v2')
args = parser.parse_args()

cmd = [
  'python','-m','plate_sampler',
  '--strategy', args.strategy,
  '--out', args.out
]
print('Running:', ' '.join(cmd))
subprocess.run(cmd)
