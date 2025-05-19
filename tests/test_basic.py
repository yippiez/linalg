#!/usr/bin/env python3

import pytest
import numpy as np
import os
import sys
import tempfile

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linalg.parser import parse_expression
from linalg.loader import load_matrices
from linalg.evaluator import evaluate_expression
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
    os.remove(matrix_A_path)
    os.remove(matrix_B_path)
    os.rmdir(temp_dir)


def test_matrix_addition(test_matrices):
    """Test matrix addition."""
    # Parse expression
    ast = parse_expression("{A}+{B}")
    
    # Evaluate expression
    result = evaluate_expression(ast, {'A': test_matrices['A'], 'B': test_matrices['B']})
    
    # Check result
    expected = test_matrices['A'] + test_matrices['B']
    np.testing.assert_array_equal(result, expected)


def test_matrix_multiplication(test_matrices):
    """Test matrix multiplication."""
    # Parse expression
    ast = parse_expression("{A}@{B}")
    
    # Evaluate expression
    result = evaluate_expression(ast, {'A': test_matrices['A'], 'B': test_matrices['B']})
    
    # Check result
    expected = test_matrices['A'] @ test_matrices['B']
    np.testing.assert_array_equal(result, expected)


def test_matrix_transpose(test_matrices):
    """Test matrix transpose."""
    # Parse expression
    ast = parse_expression("{A}.T")
    
    # Evaluate expression
    result = evaluate_expression(ast, {'A': test_matrices['A'], 'B': test_matrices['B']})
    
    # Check result
    expected = test_matrices['A'].T
    np.testing.assert_array_equal(result, expected)


def test_matrix_determinant(test_matrices):
    """Test matrix determinant."""
    # Parse expression
    ast = parse_expression("det({A})")
    
    # Evaluate expression
    result = evaluate_expression(ast, {'A': test_matrices['A'], 'B': test_matrices['B']})
    
    # Check result
    expected = np.linalg.det(test_matrices['A'])
    assert result == pytest.approx(expected)


def test_complex_expression(test_matrices):
    """Test a more complex expression."""
    # Parse expression
    ast = parse_expression("tr({A}@{B}.T) + det({A})")
    
    # Evaluate expression
    result = evaluate_expression(ast, {'A': test_matrices['A'], 'B': test_matrices['B']})
    
    # Check result
    expected = np.trace(test_matrices['A'] @ test_matrices['B'].T) + np.linalg.det(test_matrices['A'])
    assert result == pytest.approx(expected)


def test_formatter(test_matrices):
    """Test the formatter."""
    # Format a matrix result
    result = format_result(test_matrices['A'], format_type='table', precision=2)
    
    # Check that the result is a string
    assert isinstance(result, str)
    
    # Check that the result contains the matrix values
    for value in test_matrices['A'].flatten():
        assert str(int(value)) in result


def test_loader():
    """Test the matrix loader with correct file naming."""
    # Create test matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # Create temporary files to store matrices
    temp_dir = tempfile.mkdtemp()
    try:
        # Correct file names
        matrix_A_path = os.path.join(temp_dir, 'A.npy')
        matrix_B_path = os.path.join(temp_dir, 'B.npy')
        np.save(matrix_A_path, A)
        np.save(matrix_B_path, B)
        
        # Test loading with correct file names
        matrices = load_matrices([matrix_A_path, matrix_B_path])
        assert 'A' in matrices
        assert 'B' in matrices
        np.testing.assert_array_equal(matrices['A'], A)
        np.testing.assert_array_equal(matrices['B'], B)
        
        # Incorrect file name
        matrix_wrong_path = os.path.join(temp_dir, 'wrong.npy')
        np.save(matrix_wrong_path, A)
        
        # Test loading with incorrect file name
        with pytest.raises(ValueError, match="File name must be a single uppercase letter"):
            load_matrices([matrix_wrong_path])
            
        # Lowercase file name
        matrix_lower_path = os.path.join(temp_dir, 'a.npy')
        np.save(matrix_lower_path, A)
        
        # Test loading with lowercase file name
        with pytest.raises(ValueError, match="File name must be a single uppercase letter"):
            load_matrices([matrix_lower_path])
    
    finally:
        # Clean up temporary files
        import shutil
        shutil.rmtree(temp_dir)