#!/usr/bin/env python3
"""
Entry point for the linalg calculator when run from the repository root.

This is a convenience script to run the CLI from the repository root.
"""

import sys
from linalg.cli import main

if __name__ == "__main__":
    sys.exit(main())