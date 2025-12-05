
#!/bin/bash
#SBATCH --job-name={{ project_slug }}-train
#SBATCH --partition=gpu
#SBATCH --time=04:00:00
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G

set -euo pipefail

# Load pixi if available in environment, otherwise use module loads here
# module load pytorch

# Example: run cellpose4 training with CUDA env
pixi run -e cellpose4-cuda train:cp4
