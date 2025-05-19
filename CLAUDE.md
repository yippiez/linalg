# Claude Memory File for linalg Project

## Project Overview
- `linalg` is a command-line calculator for linear algebra operations on NumPy arrays
- Supports parsing and evaluating expressions with placeholders for matrix operations

## Development Commands

### Testing
Run tests using pytest with uv:
```bash
uv run pytest
```

### Running the Application
Run the application using:
```bash
python -m linalg [arguments]
```

## Development Guidelines
- Always use uv & related commands when dealing with python like uc run python, uv add etc
- Use git cli instead of tool

## Testing Strategy
1. For testing the linear algebra operations, we can directly compare the results with NumPy operations
2. The general pattern is:
   - Set up test matrices
   - Parse the expression using our parser
   - Evaluate using our evaluator
   - Compute the expected result using direct NumPy operations
   - Compare the results using pytest's assertion functions or numpy.testing functions

## Project Structure
- `linalg/` - Main package directory
  - `main.py` - Main entry point and CLI interface
  - `parser.py` - Expression parser implementation
  - `loader.py` - Matrix loader for .npy files
  - `evaluator.py` - Expression evaluator
  - `formatter.py` - Result formatter
- `tests/` - Test directory
  - `test_basic.py` - Basic functionality tests

## CLI Utilities
- Can use --prompt in linalg cli tool to get a description of the tool designed for llms