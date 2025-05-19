#!/usr/bin/env python3
"""
Module execution entry point for the linalg package.

This allows running the package directly via `python -m linalg`.
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())