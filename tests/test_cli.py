#!/usr/bin/env python3

import pytest
import numpy as np
import os
import sys
import tempfile
import subprocess

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_cli_with_correct_file_names():
    """Test the CLI with correctly named files."""
    # Create test matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrices with correct file names
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        matrix_B_path = os.path.join(temp_dir, 'B.npy')
        np.save(matrix_A_path, A)
        np.save(matrix_B_path, B)
        
        # Run CLI command for matrix addition
        cmd = [sys.executable, "-m", "linalg", "{A}+{B}", matrix_A_path, matrix_B_path, "--format", "text"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check command succeeded
        assert result.returncode == 0
        
        # Check output contains the expected result (6, 8, 10, 12)
        for val in ["6", "8", "10", "12"]:
            assert val in result.stdout


def test_cli_with_incorrect_file_name():
    """Test the CLI with incorrectly named files."""
    # Create test matrix
    A = np.array([[1, 2], [3, 4]])
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrix with incorrect file name
        matrix_wrong_path = os.path.join(temp_dir, 'wrong.npy')
        np.save(matrix_wrong_path, A)
        
        # Run CLI command
        cmd = [sys.executable, "-m", "linalg", "{A}", matrix_wrong_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check command failed
        assert result.returncode != 0
        
        # Check error message is in stderr, not stdout
        assert "File name must be a single uppercase letter" in result.stderr


def test_cli_with_lowercase_file_name():
    """Test the CLI with lowercase file names."""
    # Create test matrix
    A = np.array([[1, 2], [3, 4]])
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrix with lowercase file name
        matrix_lower_path = os.path.join(temp_dir, 'a.npy')
        np.save(matrix_lower_path, A)
        
        # Run CLI command
        cmd = [sys.executable, "-m", "linalg", "{A}", matrix_lower_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check command failed
        assert result.returncode != 0
        
        # Check error message is in stderr, not stdout
        assert "File name must be a single uppercase letter" in result.stderr