#!/usr/bin/env python3
"""
Simple examples for using the linalg calculator.

This script creates some example matrices and shows how to use the linalg
calculator for basic operations.
"""

import os
import numpy as np
import sys
import tempfile
import subprocess

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    """Run simple examples of the linalg calculator."""
    # Create temporary directory for example matrices
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create example matrices
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        
        # Save matrices to files with correct naming convention
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        matrix_B_path = os.path.join(temp_dir, 'B.npy')
        np.save(matrix_A_path, A)
        np.save(matrix_B_path, B)
        
        # Example 1: Matrix addition
        print("Example 1: Matrix addition {A}+{B}")
        cmd = [sys.executable, "-m", "linalg", "{A}+{B}", matrix_A_path, matrix_B_path]
        subprocess.run(cmd)
        print()
        
        # Example 2: Matrix multiplication
        print("Example 2: Matrix multiplication {A}@{B}")
        cmd = [sys.executable, "-m", "linalg", "{A}@{B}", matrix_A_path, matrix_B_path]
        subprocess.run(cmd)
        print()
        
        # Example 3: Matrix transpose
        print("Example 3: Matrix transpose {A}.T")
        cmd = [sys.executable, "-m", "linalg", "{A}.T", matrix_A_path]
        subprocess.run(cmd)
        print()
        
        # Example 4: Matrix determinant
        print("Example 4: Matrix determinant det({A})")
        cmd = [sys.executable, "-m", "linalg", "det({A})", matrix_A_path]
        subprocess.run(cmd)
        print()
        
        # Example 5: Complex expression
        print("Example 5: Complex expression tr({A}@{B}.T) + det({A})")
        cmd = [sys.executable, "-m", "linalg", "tr({A}@{B}.T) + det({A})", 
               matrix_A_path, matrix_B_path]
        subprocess.run(cmd)
        print()
        
        # Example 6: Different output formats
        print("Example 6: Different output formats - LaTeX")
        cmd = [sys.executable, "-m", "linalg", "{A}", matrix_A_path, 
               "--format", "latex"]
        subprocess.run(cmd)
        print()


if __name__ == "__main__":
    main()