# Microscopy AI Copier Template

A reproducible, text-first template for microscopy image analysis projects using **Cellpose 3**, **Cellpose 4 (SAM)**, and **micro‑SAM**.

Key features:
- **Pixi multi-environments** for clean isolation:
  - `cellpose3-*` (Python 3.10, `cellpose < 4.0`)
  - `cellpose4-*` (Python 3.11, `cellpose >= 4.0`, SAM support)
  - `microsam-*` (annotation & finetuning with micro‑SAM)
  - CPU/CUDA variants for each tool
- **DVC** to version large data/models locally or in **Allas (S3)**.
- **DVCLive** metrics and text manifests for runs/reports.
- **Napari** launcher that sets `PLATE_PROJECT_ROOT` so your
  [`napari-plate-navigator`](https://github.com/UH-LMU/napari-plate-navigator) can look up roots in `configs/data.yaml`.
- Optional **Slurm** script (`jobs/puhti.slurm`) to run on CSC Puhti.

---

## 1) Prerequisites

- **Git**
- **Copier** (to generate a new project from this template):
  ```bash
  pipx install copier    # or: pip install copier
  ```
- **Pixi** (environment & task runner):
  ```bash
  # Windows (PowerShell):
  irm -useb https://pixi.sh/install.ps1 | iex
  # macOS/Linux:
  curl -fsSL https://pixi.sh/install.sh | bash
  ```
- **DVC** (installed per-project via Pixi; no global install needed).

> GPU users: ensure your workstation/HPC has a compatible CUDA stack if you plan to use the `*-cuda` environments.

---

## 2) Generate a project from this template

You can **copy locally** or via the **GitHub URL**, both shown below.

### Option A — From local clone
```bash
git clone https://github.com/UH-LMU/microscopy-ai-copier-template.git
copier copy ./microscopy-ai-copier-template my-microscopy-project
cd my-microscopy-project
```

### Option B — Directly from GitHub (no local clone)
```bash
copier copy gh:UH-LMU/microscopy-ai-copier-template my-microscopy-project
cd my-microscopy-project
```

Copier will ask:
- `project_name`, `project_slug`
- whether to include DVC and Slurm files
- default storage backend (`local` or `s3`)
- Allas S3 bucket/endpoint (if you chose `s3`)
- default accelerator (`cpu` or `cuda`)

---

## 3) Project Layout

```
my-microscopy-project/
├─ pixi.toml                  # multi-env setup & tasks
├─ .env.example               # S3/Allas credentials (copy to .env)
├─ configs/
│  ├─ project.yaml            # global metadata, formats (.tiff/.czi), channels
│  ├─ data.yaml               # storage & paths (local/s3)
│  ├─ train.cellpose3.yaml    # hyperparams for Cellpose 3
│  ├─ train.cellpose4.yaml    # hyperparams for Cellpose 4 (+SAM)
│  └─ train.microsam.yaml     # hyperparams for micro-SAM finetuning
├─ data/
│  ├─ manifest.csv            # per-image URIs/metadata
│  └─ splits/v1/{train,val,test}.csv
├─ annotations/
│  ├─ labels/                 # masks (gitignored; track via DVC)
│  └─ meta/labels.csv         # text manifest pointing to masks
├─ models/                    # checkpoints (gitignored; track via DVC)
├─ scripts/                   # wrappers (test/train/evaluate, io helpers)
├─ jobs/
│  └─ puhti.slurm
├─ outputs/
│  ├─ runs/                   # per-run artifacts & metrics
│  └─ reports/
└─ dvc.yaml                   # optional stages/metrics (if DVC enabled)
```

---

## 4) Choose and install an environment

This template defines **separate Pixi environments** per tool and backend (CPU/CUDA). Examples:

- Cellpose 4 + CPU:
  ```bash
  pixi install -e cellpose4-cpu
  ```
- Cellpose 4 + CUDA:
  ```bash
  pixi install -e cellpose4-cuda
  ```
- Cellpose 3 + CPU:
  ```bash
  pixi install -e cellpose3-cpu
  ```
- micro‑SAM + CUDA:
  ```bash
  pixi install -e microsam-cuda
  ```

> You can run tasks with `-e <env>` **without** entering the shell.  
> If you want an interactive shell:
> ```bash
> pixi shell -e cellpose4-cuda
> ```

---

## 5) Configure storage (Local or Allas/S3)

### Local-only workflow
Keep your large files under `data/local/` and `annotations/labels/` and **do not commit** them to Git (already gitignored). If you want versioning, use DVC with a **local remote** or just use DVC cache.

### Allas (S3) workflow
1. Copy creds:
   ```bash
   cp .env.example .env
   # Edit .env: S3_ENDPOINT, S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   ```
2. Initialize the default DVC remote (one-time):
   ```bash
   pixi run dvc:init
   ```
3. Sync artifacts:
   ```bash
   pixi run dvc:push   # upload large files to Allas
   pixi run dvc:pull   # download large files from Allas
   ```

> Sensitive values are stored in `.dvc/config.local` (Git‑ignored).  
> DVC uses S3-compatible endpoints for Allas.

---

## 6) Common tasks

> In all examples below, **add `-e <env>`** to select the tool stack (e.g., `-e cellpose4-cpu`).

### Check the environment
```bash
pixi run -e cellpose4-cpu check
```

### Fetch pretrained checkpoints
```bash
# SAM vit-b (~375 MB) -> models/pretrained/
pixi run -e microsam-cpu fetch:sam-vitb

# Cellpose cyto3 -> models/pretrained/
pixi run -e cellpose3-cpu fetch:cp-cyto3
```

### Prepare / validate local cache (optional)
```bash
pixi run -e cellpose4-cpu python scripts/prepare_data.py
```

### Test a model on the test split
```bash
pixi run -e cellpose4-cpu test --split data/splits/v1/test.csv
```
This writes DVCLive metrics and a `metrics.json` into `outputs/runs/<timestamp>_test/`.

### Train (Cellpose 3 or 4)
```bash
# Cellpose 3
pixi run -e cellpose3-cpu train:cp3

# Cellpose 4 + SAM
pixi run -e cellpose4-cuda train:cp4
```

### Train (micro‑SAM finetuning)
```bash
pixi run -e microsam-cuda train:microsam
```

### Evaluate past runs
```bash
pixi run -e cellpose4-cpu evaluate
# Optional with DVC:
dvc metrics show
dvc metrics diff
```

### Browse with napari (preloaded project context)
```bash
# Sets PLATE_PROJECT_ROOT="." and launches napari
pixi run -e microsam-cpu browse
pixi run -e microsam-cpu browse-test
```

---

## 7) Slurm (Puhti) example

Edit `jobs/puhti.slurm` as needed, then:

```bash
sbatch jobs/puhti.slurm
```

The script uses the `cellpose4-cuda` environment and runs `train:cp4`.  
Adjust partition, account, time, and module loads per your CSC setup.

---

## 8) Data & annotations manifests

- **Images:** list them in `data/manifest.csv` with `uri` as `file://…` or `s3://…`.  
- **Splits:** `data/splits/v1/{train,val,test}.csv` hold the IDs used by tasks.  
- **Masks:** `annotations/meta/labels.csv` points from `image_id` → `label_uri`.

Store large files (images/masks/models) out of Git; use DVC to version/push if needed.

---

## 9) Tips & customization

- Pin CUDA/PyTorch versions per cluster/workstation by adjusting the `pixi.toml` envs.
- Add extra pretrained models to `scripts/fetch_pretrained.py`.
- Integrate your [`plate-sampler`](https://github.com/UH-LMU/plate-sampler) via `scripts/plate_sampler_wrapper.py` to create stratified splits.
- If your department policy requires environments from a fixed path (e.g., `C:\hyapp\pixi_envs`), configure Pixi’s environment directory globally or install with `--path` (see Pixi docs).

---

## 10) Support / Contributions

Issues and PRs welcome:  
https://github.com/UH-LMU/microscopy-ai-copier-template
