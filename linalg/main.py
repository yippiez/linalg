#!/usr/bin/env python3
"""
Main implementation of the linalg calculator.

This module contains the core functionality of the linalg calculator,
but the CLI entry point is now in the cli.py module.
"""

import argparse
import numpy as np
import sys
from typing import List, Optional, Dict, Any, Tuple

from .parser import parse_expression
from .loader import load_matrices
from .evaluator import evaluate_expression
from .formatter import format_result


def main() -> int:
    """
    Legacy main entry point for the application.
    
    This is kept for backwards compatibility but delegates to the CLI module.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    from .cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())