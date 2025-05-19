# linalg - Linear Algebra Calculator

Command-line calculator for linear algebra operations on NumPy arrays.

## Usage

```bash
linalg "{expression}" file1.npy file2.npy ...
```

Use placeholders like `{A}`, `{B}` in expressions to reference `.npy` files.

## File Naming

Files must use single uppercase letters matching placeholders:
- `A.npy` for `{A}`
- `B.npy` for `{B}`

## Piping

```bash
# Use {PIPE} placeholder for piped input
cat A.npy | linalg "{PIPE}+{B}" B.npy

# Chain operations
linalg "{A}+{B}" A.npy B.npy --npy | linalg "det({PIPE})"
```

## Examples

```bash
# Addition
linalg "{A}+{B}" A.npy B.npy

# Multiplication
linalg "{A}@{B}" A.npy B.npy

# Transpose
linalg "{A}.T" A.npy
```

## Options

```
--output, -o PATH      Output file path
--npy, -n              Use NPY format for output
--precision N          Decimal precision (default: 4)
--format, -f FMT       Output format: text, csv, npy, latex, json, table, plain
--binary-stdout        Write binary data to stdout
--version              Show version
--prompt               Display documentation for LLMs
```

## Supported Operations

- Basic: addition, subtraction, multiplication, transpose
- Matrix functions: inverse, pseudoinverse, power
- Scalar output: determinant, trace, norm, rank
- Decompositions: SVD, eigenvalues/vectors, QR, LU, Cholesky
- Matrix creation: identity, diagonal, random, zeros/ones

## Installation WIP

```bash
pip install linalg
```

### Development Installation

```bash
git clone https://github.com/example/linalg.git
cd linalg
uv venv venv
source venv/bin/activate
uv pip install -e ".[dev]"
```

Run tests:
```bash
uv run pytest
```
