# Linear Algebra Calculator

A command-line calculator for performing linear algebra operations on NumPy arrays stored in `.npy` files.

## Basic Usage

```bash
linalg "{expression}" file1.npy file2.npy ...
```

Where `{expression}` contains placeholders like `{A}`, `{B}` that are substituted with the contents of the corresponding `.npy` files.

## File Naming Requirement

The `.npy` files must be named with a single uppercase letter corresponding to the placeholder used in the expression:
- `A.npy` for placeholder `{A}`
- `B.npy` for placeholder `{B}`
- etc.

This naming convention is enforced to ensure clarity and prevent ambiguity in expressions.

## Output Formats

By default, `linalg` outputs results in plain text format, which is easily parseable by other tools:

```
# Matrix output (tab-separated)
1.2345  6.7890
2.3456  7.8901

# Vector output (one per line)
1.2345
6.7890

# Scalar output
1.2345
```

For a more visually pleasing output, use the `--pretty` flag:

```
$ linalg "{A}+{B}" A.npy B.npy --pretty

Matrix Result
┏━━━━━┳━━━━━┓
┃ [0] ┃ [1] ┃
┡━━━━━╇━━━━━┩
│ 6   │ 8   │
│ 10  │ 12  │
└─────┴─────┘
```

## Piping Support

The calculator supports piping for chaining operations:

```bash
# Pipe a matrix into linalg and use the {PIPE} placeholder
cat A.npy | linalg "{PIPE}+{B}" B.npy

# Chain operations by piping results between linalg commands
linalg "{A}+{B}" A.npy B.npy --npy | linalg "det({PIPE})"

# Use the output with other command-line tools
linalg "inv({A})" A.npy | awk '{print $1}'
```

Notes:
- Stdin data is automatically detected without any flags
- Piped input is available as the `{PIPE}` placeholder
- Use `--npy` for binary NPY output format, useful for piping between linalg commands
- Use `--binary-stdout` to write binary data directly to stdout
- `pipe.npy` is a reserved filename and cannot be used directly

## Examples

```bash
# Matrix addition
linalg "{A}+{B}" A.npy B.npy

# Matrix multiplication
linalg "{A}@{B}" A.npy B.npy

# Transpose
linalg "{A}.T" A.npy

# Determinant
linalg "det({A})" A.npy

# Complex expression with piped input
cat A.npy | linalg "tr({PIPE}@{B}.T) + det({PIPE})" B.npy
```

## Options

```
--output, -o PATH      Output file path (default: print to console)
--npy, -n              Use NPY format for output, useful for piping between linalg commands
--precision N          Decimal precision (default: 4)
--format, -f FMT       Output format: text, csv, npy, latex, json, table, plain (default: plain)
--pretty               Use pretty table output with colors
--binary-stdout        Write binary data directly to stdout (for piping npy files)
--info, -i             Show information about matrices
--verbose, -v          Show detailed execution
--threshold, -t N      Hide values below threshold (default: 1e-10)
--components, -c       For tuple outputs, save components separately
--version              Show version number and exit
--prompt               Display comprehensive documentation for use with LLMs
```

## Features

- Supports a wide range of linear algebra operations
- Flexible expression syntax with placeholder system
- Plain text output by default for better tool integration
- Multiple output formats (plain, csv, npy, latex, json, table)
- Full piping support for Unix-style composition
- Precision control and value thresholding
- Detailed output information and verbose execution mode

## Supported Operations

- Basic operations: addition, subtraction, multiplication, transpose
- Matrix functions: inverse, pseudoinverse, power
- Scalar output: determinant, trace, norm, rank, condition number
- Decompositions: SVD, eigenvalues/vectors, QR, LU, Cholesky
- Matrix creation: identity, diagonal, random, zeros/ones

See the design document for a complete list of supported operations.