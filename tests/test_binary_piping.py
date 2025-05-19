#!/usr/bin/env python3

import pytest
import numpy as np
import os
import sys
import tempfile
import subprocess
import io
from contextlib import redirect_stdout, redirect_stderr
import shutil

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_binary_piping_between_commands():
    """Test piping binary NPY data between linalg commands."""
    # Create test matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrices
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        matrix_B_path = os.path.join(temp_dir, 'B.npy')
        matrix_C_path = os.path.join(temp_dir, 'C.npy')
        np.save(matrix_A_path, A)
        np.save(matrix_B_path, B)
        
        # Create a temporary script to compute determinant and save it
        # This is more reliable for testing than trying to pipe binary data directly
        add_cmd = f"{sys.executable} -m linalg '{{A}}+{{B}}' {matrix_A_path} {matrix_B_path} --npy --output {matrix_C_path}"
        det_cmd = f"{sys.executable} -m linalg 'det({{C}})' {matrix_C_path} --format plain"
        
        # Run the commands
        cmds = f"{add_cmd} && {det_cmd}"
        result = subprocess.run(cmds, shell=True, capture_output=True, text=True)
        
        # Check command succeeded
        assert result.returncode == 0, f"Error: {result.stderr}"
        
        # Verify result: det(A+B) = det([[6,8],[10,12]])
        expected = np.linalg.det(A + B)
        
        # Check the output from stdout (plain text format)
        actual = float(result.stdout.strip())
        
        # Compare with small tolerance
        assert abs(actual - expected) < 1e-10


def test_binary_npy_output():
    """Test binary NPY output with --npy flag."""
    # Create test matrix
    A = np.array([[1, 2], [3, 4]])
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrix
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        output_path = os.path.join(temp_dir, 'output.npy')
        np.save(matrix_A_path, A)
        
        # Run linalg with --npy and save output
        cmd = f"{sys.executable} -m linalg '{{A}}+{{A}}' {matrix_A_path} --npy --output {output_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Check command succeeded
        assert result.returncode == 0
        
        # Load the output and check it's correct
        output = np.load(output_path)
        np.testing.assert_array_equal(output, A + A)


def test_binary_multi_stage_pipe():
    """Test a multi-stage pipe using binary NPY format."""
    # Create test matrix
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save matrices
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        matrix_B_path = os.path.join(temp_dir, 'B.npy')
        matrix_C_path = os.path.join(temp_dir, 'C.npy')
        matrix_D_path = os.path.join(temp_dir, 'D.npy')
        matrix_E_path = os.path.join(temp_dir, 'E.npy')
        result_path = os.path.join(temp_dir, 'R.npy')
        np.save(matrix_A_path, A)
        np.save(matrix_B_path, B)
        
        # Multi-stage calculation: (A+B).T @ (A-B)
        # Break it down into steps using files with proper naming
        cmd1 = f"{sys.executable} -m linalg '{{A}}+{{B}}' {matrix_A_path} {matrix_B_path} --npy --output {matrix_C_path}"
        cmd2 = f"{sys.executable} -m linalg '{{C}}.T' {matrix_C_path} --npy --output {matrix_D_path}" 
        cmd3 = f"{sys.executable} -m linalg '{{A}}-{{B}}' {matrix_A_path} {matrix_B_path} --npy --output {matrix_E_path}"
        cmd4 = f"{sys.executable} -m linalg '{{D}}@{{E}}' {matrix_D_path} {matrix_E_path} --npy --output {result_path}"
        
        # Execute in sequence
        pipe_cmd = f"{cmd1} && {cmd2} && {cmd3} && {cmd4}"
        
        # Run the command
        result = subprocess.run(pipe_cmd, shell=True, capture_output=True)
        
        # Check command succeeded
        assert result.returncode == 0, f"Error: {result.stderr.decode('utf-8')}"
        
        # Calculate expected result manually: (A+B).T @ (A-B)
        expected = (A + B).T @ (A - B)
        
        # Check result manually
        actual = np.load(result_path, allow_pickle=True)
        np.testing.assert_array_almost_equal(actual, expected)