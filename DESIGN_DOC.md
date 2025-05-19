# Linear Algebra Calculator Design Document

## 1. Overview

`linalg` is a command-line calculator designed to perform linear algebra operations on NumPy arrays stored in `.npy` files. It uses a flexible expression syntax with placeholders to represent matrices and provides a wide range of linear algebra operations.

### Basic Usage
```
linalg "{expression}" file1.npy file2.npy ...
```

Where `{expression}` contains placeholders like `{A}`, `{B}` that are substituted with the contents of the corresponding `.npy` files.

## 2. Core Functionality

### Placeholder System
- Files associate with placeholders in order of appearance (A, B, C, etc.)
- Example: `linalg "{A}+{B}" matrix1.npy matrix2.npy`
  - A = contents of matrix1.npy
  - B = contents of matrix2.npy

### Expression Parsing
- Tokenize the expression
- Build an Abstract Syntax Tree (AST)
- Evaluate the tree recursively
- Handle errors at each evaluation step

## 3. Implementation Architecture

### Components
1. **Parser**: 
   - Tokenizes expression
   - Builds AST
   - Validates syntax

2. **Loader**:
   - Loads NumPy arrays from files
   - Validates dimensions

3. **Evaluator**:
   - Recursively evaluates expression tree
   - Applies operations
   - Handles errors

4. **Formatter**:
   - Detects output type
   - Formats results appropriately
   - Generates requested output format

5. **CLI Interface**:
   - Handles arguments
   - Manages program flow

### Expression Tree Node Types
- Binary operations (addition, multiplication, etc.)
- Unary operations (transpose, negation)
- Function calls (determinant, inverse, etc.)
- Matrix references (placeholders)
- Constants (for scalar operations)

## 4. Command Line Interface

### Arguments
- Required: expression string
- Required: at least one .npy file
- Optional flags:

| Flag | Description | Default |
|------|-------------|---------|
| `--output/-o` | Output file path | Print to console |
| `--precision/-p` | Decimal precision | 4 |
| `--format/-f` | Output format (text, csv, npy, latex, json, table) | table |
| `--info/-i` | Show information about matrices | False |
| `--verbose/-v` | Show detailed execution | False |
| `--threshold/-t` | Hide values below threshold | 1e-10 |
| `--components/-c` | For tuple outputs, save components separately | False |

## 5. Supported Operations

### Matrix/Array Output Operations
- Addition: `{A}+{B}`
- Subtraction: `{A}-{B}`
- Matrix multiplication: `{A}@{B}`
- Element-wise multiplication: `{A}*{B}`
- Transpose: `{A}.T`
- Inverse: `inv({A})`
- Pseudoinverse: `pinv({A})`
- Matrix power: `{A}^n` or `matrix_power({A},n)`
- Element-wise functions: `exp({A})`, `sin({A})`, etc.

### Scalar Output Operations
- Determinant: `det({A})`
- Trace: `trace({A})` or `tr({A})`
- Norm: `norm({A})`
- Rank: `rank({A})`
- Condition number: `cond({A})`
- Sum/Product: `sum({A})`, `prod({A})`
- Mean/Std: `mean({A})`, `std({A})`

### Tuple/Multiple Output Operations
- SVD: `svd({A})`
- Eigenvalues/vectors: `eig({A})`
- QR decomposition: `qr({A})`
- LU decomposition: `lu({A})`
- Cholesky decomposition: `cholesky({A})`
- Solve linear system: `solve({A},{B})`
- Least squares: `lstsq({A},{B})`

### Matrix Creation Operations
- Identity: `eye(n)`
- Diagonal: `diag({A})`
- Random: `rand(m,n)`
- Zeros/Ones: `zeros(m,n)`, `ones(m,n)`

## 6. Output Handling

### Output Types
- Arrays: Formatted matrices
- Scalars: Single values with precision
- Tuples: Multiple components labeled appropriately

### Format Options
- `table`: Pretty-printed tables (default)
- `csv`: Comma-separated values
- `npy`: NumPy binary file
- `latex`: LaTeX representation
- `json`: JSON format

### Display Features
- Precision control
- Value thresholding
- Compact display for large matrices

## 7. Test Cases

Below are example test cases to validate the functionality of `linalg`:

### Basic Operations

```bash
# Matrix addition
linalg "{A}+{B}" matrix1.npy matrix2.npy

# Matrix multiplication
linalg "{A}@{B}" matrix1.npy matrix2.npy

# Transpose
linalg "{A}.T" matrix1.npy

# Element-wise operations
linalg "{A}*{B}" matrix1.npy matrix2.npy
```

### Scalar Output Operations

```bash
# Determinant
linalg "det({A})" matrix1.npy

# Trace
linalg "tr({A})" matrix1.npy

# Norm
linalg "norm({A})" matrix1.npy
```

### Tuple/Multiple Output Operations

```bash
# SVD decomposition
linalg "svd({A})" matrix1.npy

# Eigenvalues and eigenvectors
linalg "eig({A})" matrix1.npy

# QR decomposition
linalg "qr({A})" matrix1.npy
```

### Complex Expressions

```bash
# Solve system of equations
linalg "solve({A},{B})" coefficients.npy constants.npy

# Matrix inverse composition
linalg "inv({A})@{B}" matrix1.npy matrix2.npy

# Complex operation chain
linalg "tr({A}@{B}.T) + det({C})" matrix1.npy matrix2.npy matrix3.npy

# Matrix equation
linalg "{A}@{X}={B}" A.npy B.npy
```

### Output Format Examples

```bash
# Save result as NPY file
linalg "{A}@{B}" matrix1.npy matrix2.npy -o result.npy

# Generate LaTeX output
linalg "eig({A})" matrix1.npy --format latex

# View as formatted table with custom precision
linalg "svd({A})" matrix1.npy --format table --precision 6

# Save multiple components
linalg "svd({A})" matrix1.npy --components --output svd_components
```

### Error Handling Cases

```bash
# Dimension mismatch
linalg "{A}+{B}" 3x3matrix.npy 4x4matrix.npy

# Non-invertible matrix
linalg "inv({A})" singular_matrix.npy

# Invalid expression
linalg "{A}@@{B}" matrix1.npy matrix2.npy

# Missing files
linalg "{A}+{B}" existing.npy nonexistent.npy
```

### Specialized Cases

```bash
# Matrix information
linalg "{A}" matrix1.npy --info

# Large matrix display
linalg "{A}" large_matrix.npy --format table

# Compare results
linalg "{A}@{B} - {C}" matrix1.npy matrix2.npy expected.npy
```

These test cases cover the range of functionality and help validate that the calculator works correctly in various scenarios.
