# Installation Guide

## Installing with pip

You can install the `linalg` calculator directly from PyPI:

```bash
pip install linalg
```

After installation, the `linalg` command will be available in your terminal.

## Installing with pipx

For isolated installation, you can use pipx:

```bash
pipx install linalg
```

This installs `linalg` in an isolated environment but makes the command globally available.

## Development Installation

To install the package for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/example/linalg.git
   cd linalg
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

This installs the package in editable mode along with development dependencies.

## Running Tests

After installing the development dependencies, you can run tests with:

```bash
pytest
```

Or with coverage:

```bash
pytest --cov=linalg
```