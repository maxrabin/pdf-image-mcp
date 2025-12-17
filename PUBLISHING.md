# Publishing Guide

## Setup (One-time)

1.  Log in to [PyPI](https://pypi.org/).
2.  Go to **Account Settings** -> **Publishing**.
3.  Add a **New pending publisher**:
    *   **Project**: `pdf-image-extractor-mcp`
    *   **Owner**: `maxrabin`
    *   **Repo**: `pdf-image-mcp`
    *   **Workflow**: `release.yml`
    *   **Environment**: `pypi`

## Releasing a New Version

1.  **Bump Version**:
    Update `version` in `pyproject.toml`:
    ```toml
    [project]
    version = "0.1.1" # Change this
    ```

2.  **Commit & Push**:
    ```bash
    git add pyproject.toml
    git commit -m "chore: bump version to 0.1.1"
    git push
    ```

3.  **Create Release**:
    *   Go to GitHub Repo -> **Releases** -> **Draft a new release**.
    *   Tag: `v0.1.1` (Match your version).
    *   Click **Publish release**.

The `release.yml` workflow will automatically handle the rest.
