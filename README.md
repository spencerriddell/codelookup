# CodeLookup: Client-side Shiny for Python (Shinylive)

This repository hosts a client-side dashboard built with [Shiny for Python](https://shiny.posit.co/py/) and [Shinylive](https://shinylive.io/), published via GitHub Pages. It generates SAS code snippets for codelookup workflows.

## Quick start

- App code lives in `app/app.py`.
- Build static site with:
  ```bash
  pip install -r requirements.txt
  python -m shinylive export app docs
  ```
- Enable Pages: Settings → Pages → Source: `Deploy from a branch`, Branch: `main`, Folder: `/docs`.

## Local development

Run locally (serverful) for faster iteration:
```bash
pip install -r requirements.txt
python -m shiny run --reload app/app.py
```

## Notes

- Shinylive runs fully in the browser; avoid native-extension packages that won't work in WebAssembly.
- Replace the placeholder SAS generation logic in `app/app.py` with your actual codelookup code.

## CI/CD

The workflow `.github/workflows/deploy-shinylive.yml`:
- Installs dependencies
- Builds `docs/` with Shinylive on every push to `main`
- Publishes via GitHub Pages (`docs/`)

Visit: `https://spencerriddell.github.io/codelookup/`
