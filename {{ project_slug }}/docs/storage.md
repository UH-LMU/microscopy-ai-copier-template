
# Storage Options (Local & Allas S3)

## Local
- Use `file://` URIs and keep large data in `data/local/` (gitignored).

## Allas (S3-compatible)
1. Ensure you have S3 credentials and endpoint (often `https://a3s.fi`).
2. Configure the DVC remote (one-time):

```bash
pixi run dvc:init
```

This creates a default remote named `allas` at `s3://$S3_BUCKET/$PIXI_PROJECT_NAME` and sets the endpoint.

3. Push/pull:

```bash
pixi run dvc:push
pixi run dvc:pull
```

> Keep secrets out of Git. DVC stores access keys locally (`.dvc/config.local`).
