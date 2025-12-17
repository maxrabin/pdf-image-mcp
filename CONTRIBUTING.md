# Contributing to PDF Image Extractor MCP

We welcome contributions! Please follow these steps to contribute.

## Development Setup

1.  **Fork and Clone**: Fork the repository and clone it locally.
2.  **Install uv**: Ensure you have [uv](https://github.com/astral-sh/uv) installed.
3.  **Sync Dependencies**:
    ```bash
    uv sync
    ```
4.  **Install Pre-commit Hooks**:
    ```bash
    uv run pre-commit install
    ```

## Running Tests

Run the test suite using `pytest`:

```bash
uv run pytest
```

## Linting and Type Checking

We use `ruff` for linting/formatting and `pyright` for static type checking.

```bash
# Run all pre-commit hooks
uv run pre-commit run --all-files

# Or run individually
uv run ruff check .
uv run ruff format .
uv run pyright
```

## Submitting a Pull Request

1.  Create a new branch for your feature or fix.
2.  Ensure all tests and linting checks pass.
3.  Submit a Pull Request with a clear description of your changes.
