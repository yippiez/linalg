#!/usr/bin/env python3

import pytest
import numpy as np
import os
import sys
import tempfile
import subprocess
import io
from contextlib import redirect_stdout, redirect_stderr

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linalg.loader import read_from_stdin, load_matrices
from linalg.cli import main as cli_main
from linalg.formatter import format_result


@pytest.fixture
def test_matrices():
    """Fixture to create test matrices."""
    # Create test matrices
    A = np.array([[1, 2], [3, 4]])  # 2x2 matrix
    B = np.array([[5, 6], [7, 8]])  # 2x2 matrix
    
    # Create temporary files to store matrices
    temp_dir = tempfile.mkdtemp()
    matrix_A_path = os.path.join(temp_dir, 'A.npy')
    matrix_B_path = os.path.join(temp_dir, 'B.npy')
    
    # Save matrices to files
    np.save(matrix_A_path, A)
    np.save(matrix_B_path, B)
    
    # Return matrices and paths
    yield {
        'A': A,
        'B': B,
        'matrix_A_path': matrix_A_path,
        'matrix_B_path': matrix_B_path,
        'temp_dir': temp_dir
    }
    
    # Clean up temporary files
    try:
        os.remove(matrix_A_path)
        os.remove(matrix_B_path)
        os.rmdir(temp_dir)
    except:
        pass


def test_plain_output_format(test_matrices):
    """Test the plain output format."""
    # Test plain output format with a matrix
    result = format_result(test_matrices['A'], format_type='plain', plain=True)
    
    # Check that the result is tab-separated with newlines
    lines = result.strip().split('\n')
    assert len(lines) == 2  # 2x2 matrix has 2 rows
    
    # Check first row is tab-separated
    first_row = lines[0].split('\t')
    assert len(first_row) == 2
    assert float(first_row[0]) == 1.0
    assert float(first_row[1]) == 2.0
    
    # Check second row is tab-separated
    second_row = lines[1].split('\t')
    assert len(second_row) == 2
    assert float(second_row[0]) == 3.0
    assert float(second_row[1]) == 4.0


def test_plain_scalar_output(test_matrices):
    """Test plain output format with a scalar."""
    # Test plain output with a scalar
    scalar = 42.5
    result = format_result(scalar, format_type='plain', plain=True)
    
    # Check the result is just the scalar value
    assert result.strip() == "42.5"


def test_reserved_pipe_filename(test_matrices):
    """Test that pipe.npy is a reserved filename."""
    # Create a pipe.npy file
    pipe_path = os.path.join(test_matrices['temp_dir'], 'pipe.npy')
    np.save(pipe_path, np.array([[1, 2], [3, 4]]))
    
    try:
        # Test that loading pipe.npy raises an error with the updated error message
        with pytest.raises(ValueError, match="{PIPE} placeholder"):
            load_matrices([pipe_path])
    finally:
        # Clean up
        if os.path.exists(pipe_path):
            os.remove(pipe_path)


def test_cli_with_automatic_piping():
    """Test CLI with automatic piping detection."""
    # Use a subprocess approach for more reliable stdin/stdout handling
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test matrix
        A = np.array([[1, 2], [3, 4]])
        
        # Save matrix to a temporary file
        input_path = os.path.join(temp_dir, 'input.npy')
        np.save(input_path, A)
        
        # Use shell piping to test automatic stdin detection
        # cat input.npy | python -m linalg "{PIPE}" --format plain
        cat_cmd = f"cat {input_path}"
        linalg_cmd = f"{sys.executable} -m linalg '{{PIPE}}' --format plain"
        full_cmd = f"{cat_cmd} | {linalg_cmd}"
        
        # Run the command
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
        
        # Check command succeeded
        assert result.returncode == 0
        
        # Get output and check it's in plain format
        output = result.stdout
        lines = output.strip().split('\n')
        assert len(lines) == 2  # 2x2 matrix
        
        # Check row content (tab-separated)
        first_row = lines[0].split('\t')
        assert len(first_row) == 2
        assert float(first_row[0]) == 1.0
        assert float(first_row[1]) == 2.0


def test_cli_pretty_output():
    """Test CLI with pretty output."""
    # Create test matrix
    A = np.array([[1, 2], [3, 4]])
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrix
        matrix_path = os.path.join(temp_dir, 'A.npy')
        np.save(matrix_path, A)
        
        # Use subprocess to run CLI with pretty output
        # (Using subprocess avoids issues with the mock stdin/stdout in pytest)
        cmd = [sys.executable, "-m", "linalg", "{A}", matrix_path, "--pretty"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check output
        output = result.stdout
        assert "Matrix Result" in output
        # Skip character checks since the formatting may be terminal-dependent
        assert "1" in output and "2" in output and "3" in output and "4" in output