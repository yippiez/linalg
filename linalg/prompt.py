#!/usr/bin/env python3
"""
Prompt generation for linalg.

This module provides detailed information about linalg features
in a format optimized for Large Language Models.
"""

def generate_prompt() -> str:
    """
    Generate a detailed prompt about linalg for use with LLMs.
    
    Returns:
        A string containing the prompt with detailed information
        about all linalg features, formats, and examples.
    """
    return f"""
# Linalg - Linear Algebra Command-Line Calculator

## Overview
Linalg is a command-line calculator for linear algebra operations on NumPy arrays. It allows you to:
- Load matrices from .npy files
- Parse and evaluate expressions with placeholders
- Perform various linear algebra operations
- Format and output results in multiple formats
- Pipe results between commands
- Use complex expressions with operators and functions

## Key Features

### Matrix Placeholders
- Single uppercase letter placeholders like `{{A}}`, `{{B}}`, `{{C}}` represent .npy files
- Filename must match placeholder (e.g., A.npy for `{{A}}`)
- Special placeholder `{{PIPE}}` for piped input (automatically detected)

### Supported Operations

#### Arithmetic Operations
- Addition: `{{A}}+{{B}}`
- Subtraction: `{{A}}-{{B}}`
- Multiplication: `{{A}}*{{B}}` (element-wise)
- Division: `{{A}}/{{B}}` (element-wise)
- Matrix multiplication: `{{A}}@{{B}}`
- Power: `{{A}}**2` or `{{A}}^2`

#### Matrix Properties and Attributes
- Transpose: `{{A}}.T`
- Inverse: `{{A}}.I` (equivalent to `inv({{A}})`)
- Conjugate transpose: `{{A}}.H`
- Shape: `{{A}}.shape`
- Size: `{{A}}.size`
- Norm: `{{A}}.norm` or `norm({{A}})`

#### Linear Algebra Functions
- Determinant: `det({{A}})`
- Trace: `tr({{A}})` or `trace({{A}})`
- Eigenvalues: `eig({{A}})`
- Singular value decomposition: `svd({{A}})`
- LU decomposition: `lu({{A}})`
- QR decomposition: `qr({{A}})`
- Rank: `rank({{A}})`
- Condition number: `cond({{A}})`

#### Element-wise Functions
- Absolute value: `abs({{A}})`
- Exponential: `exp({{A}})`
- Natural logarithm: `log({{A}})`
- Square root: `sqrt({{A}})`
- Sine: `sin({{A}})`
- Cosine: `cos({{A}})`
- Tangent: `tan({{A}})`

#### Reduction Operations
- Sum of all elements: `sum({{A}})`
- Product of all elements: `prod({{A}})`
- Minimum value: `min({{A}})`
- Maximum value: `max({{A}})`
- Mean value: `mean({{A}})`
- Standard deviation: `std({{A}})`

### Output Formats
- `plain`: Simple text format (default) - tab-separated values, ideal for piping
- `text`: NumPy's default string representation
- `table`: Pretty-printed table with formatting (use `--pretty` for colors)
- `csv`: Comma-separated values
- `json`: JSON array format
- `latex`: LaTeX bmatrix format for use in papers/documents
- `npy`: Binary NumPy format (when saving to file or using `--binary-stdout` or `--npy`)

### Piping Support
- Stdin data is automatically detected without needing any flags
- Access piped data with `{{PIPE}}` placeholder
- Basic example: `cat A.npy | linalg "{{PIPE}}.T" --format plain`
- Pipe outputs between linalg commands:
  ```bash
  # Text-based piping (default)
  linalg "{{A}}+{{B}}" A.npy B.npy --format plain | linalg "det({{PIPE}})"
  
  # Binary piping with the --npy flag (more efficient for matrix data)
  linalg "{{A}}+{{B}}" A.npy B.npy --npy | linalg "det({{PIPE}})" --npy
  ```

## Complete Usage Examples

### Basic Matrix Operations
```bash
# Matrix addition
linalg "{{A}}+{{B}}" A.npy B.npy

# Matrix multiplication
linalg "{{A}}@{{B}}" A.npy B.npy

# Transpose
linalg "{{A}}.T" A.npy

# Determinant
linalg "det({{A}})" A.npy
```

### Complex Expressions
```bash
# Compute (A + B)^T @ (A - B)
linalg "({{A}}+{{B}}).T@({{A}}-{{B}})" A.npy B.npy

# Compute trace of A^2 + det(B)
linalg "tr({{A}}@{{A}}) + det({{B}})" A.npy B.npy

# Frobenius norm of A-B
linalg "norm({{A}}-{{B}})" A.npy B.npy
```

### Output Format Examples
```bash
# Output as CSV
linalg "{{A}}" A.npy --format csv

# Output as LaTeX
linalg "{{A}}" A.npy --format latex

# Output as JSON
linalg "{{A}}" A.npy --format json

# Pretty-printed table with colors
linalg "{{A}}" A.npy --pretty

# Save to .npy file
linalg "{{A}}+{{B}}" A.npy B.npy --format npy --output result.npy
```

### Piping Examples
```bash
# Pipe matrix A to linalg, transpose it, and format as plain text
cat A.npy | linalg "{{PIPE}}.T" --format plain

# Chain operations: (A+B).T then calculate determinant using text-based piping
linalg "{{A}}+{{B}}" A.npy B.npy --format plain | linalg "det({{PIPE}})"

# Same operation using binary piping for better performance with large matrices
linalg "{{A}}+{{B}}" A.npy B.npy --npy | linalg "{{PIPE}}.T" --npy | linalg "det({{PIPE}})" --npy

# Multi-step calculation: svd(A), extract and use U component
linalg "svd({{A}})" A.npy --format plain | grep -A5 "COMPONENT_0" | tail -n +2 | linalg "{{PIPE}}@{{PIPE}}.T"

# Complex calculation using temporary files: (A+B).T @ (A-B)
linalg "{{A}}+{{B}}" A.npy B.npy --npy --output C.npy
linalg "{{C}}.T" C.npy --npy --output D.npy
linalg "{{A}}-{{B}}" A.npy B.npy --npy --output E.npy
linalg "{{D}}@{{E}}" D.npy E.npy --npy
```

### Advanced Features
```bash
# Show matrix information (shape, rank, etc.)
linalg "{{A}}" A.npy --info

# Set precision for numeric display
linalg "{{A}}" A.npy --precision 6

# Set threshold to hide small values
linalg "{{A}}" A.npy --threshold 1e-8

# Save SVD components separately
linalg "svd({{A}})" A.npy --components --output svd_result
# Creates svd_result_0.npy, svd_result_1.npy, svd_result_2.npy

# Verbose output for debugging
linalg "{{A}}+{{B}}" A.npy B.npy --verbose
```

## Important Notes
1. File names must match placeholders (e.g., A.npy for {{A}})
2. 'pipe.npy' is a reserved filename, use {{PIPE}} placeholder instead for stdin data
3. Default output is plain format for better piping
4. Use --pretty for colored, formatted table output
5. The command automatically detects data from stdin and makes it available as {{PIPE}}

## Tips for Expression Construction
- Expressions follow standard mathematical notation
- Functions apply to the entire matrix or element-wise where appropriate
- Parentheses control order of operations
- Matrix attributes are accessed with dot notation
- Matrices can be combined with scalars in operations
- Use appropriate error handling for invalid operations
"""