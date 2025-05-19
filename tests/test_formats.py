#!/usr/bin/env python3

import pytest
import numpy as np
import os
import sys
import tempfile
import json
import io
import re

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linalg.formatter import format_result


@pytest.fixture
def test_matrices():
    """Fixture to create test matrices."""
    # Create test matrices
    A = np.array([[1, 2], [3, 4]])  # 2x2 matrix
    B = np.array([[5, 6], [7, 8]])  # 2x2 matrix
    
    # Return matrices
    return {
        'A': A,
        'B': B,
        'scalar': 42.5,
        'vector': np.array([1, 2, 3])
    }


def test_csv_format(test_matrices):
    """Test the CSV output format."""
    # Test CSV output format with a matrix
    result = format_result(test_matrices['A'], format_type='csv')
    
    # Check that the result contains comma-separated values
    lines = result.strip().split('\n')
    assert len(lines) == 2  # 2x2 matrix has 2 rows
    
    # Check first row is comma-separated
    first_row = lines[0].split(',')
    assert len(first_row) == 2
    assert float(first_row[0]) == 1.0
    assert float(first_row[1]) == 2.0
    
    # Check second row is comma-separated
    second_row = lines[1].split(',')
    assert len(second_row) == 2
    assert float(second_row[0]) == 3.0
    assert float(second_row[1]) == 4.0


def test_csv_vector_format(test_matrices):
    """Test the CSV output format with a vector."""
    # Test CSV output with a vector
    result = format_result(test_matrices['vector'], format_type='csv')
    
    # Check that the result is a single line with comma-separated values
    values = result.strip().split(',')
    assert len(values) == 3
    assert float(values[0]) == 1.0
    assert float(values[1]) == 2.0
    assert float(values[2]) == 3.0


def test_latex_format(test_matrices):
    """Test the LaTeX output format."""
    # Test LaTeX output with a matrix
    result = format_result(test_matrices['A'], format_type='latex')
    
    # Check that the result is in LaTeX bmatrix format
    assert r"\begin{bmatrix}" in result
    assert r"\end{bmatrix}" in result
    
    # Check that rows are separated by \\
    assert r" \\" in result
    
    # Check that the values are in the output
    for row in test_matrices['A']:
        for val in row:
            assert str(int(val)) in result
    
    # Check that matrix entries are separated by &
    assert " & " in result


def test_latex_vector_format(test_matrices):
    """Test the LaTeX output format with a vector."""
    # Test LaTeX output with a vector
    result = format_result(test_matrices['vector'], format_type='latex')
    
    # Check for LaTeX formatting elements
    assert r"\begin{bmatrix}" in result
    assert r"\end{bmatrix}" in result
    
    # Check that all vector values are present
    for val in test_matrices['vector']:
        assert str(int(val)) in result


def test_json_format(test_matrices):
    """Test the JSON output format."""
    # Test JSON output with a matrix
    result = format_result(test_matrices['A'], format_type='json')
    
    # Parse the JSON result
    json_data = json.loads(result)
    
    # Check that the structure matches the original matrix
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    assert len(json_data[0]) == 2
    assert len(json_data[1]) == 2
    
    # Check the values
    assert json_data[0][0] == 1
    assert json_data[0][1] == 2
    assert json_data[1][0] == 3
    assert json_data[1][1] == 4


def test_json_vector_format(test_matrices):
    """Test the JSON output format with a vector."""
    # Test JSON output with a vector
    result = format_result(test_matrices['vector'], format_type='json')
    
    # Parse the JSON result
    json_data = json.loads(result)
    
    # Check that the structure matches the original vector
    assert isinstance(json_data, list)
    assert len(json_data) == 3
    
    # Check the values
    assert json_data[0] == 1
    assert json_data[1] == 2
    assert json_data[2] == 3


def test_npy_format_file_output(test_matrices):
    """Test the NPY output format with file output."""
    # Create a temporary file for NPY output
    with tempfile.NamedTemporaryFile(suffix='.npy', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Format result and write to file
        format_result(test_matrices['A'], format_type='npy', output_path=tmp_path)
        
        # Load the file and check contents
        loaded = np.load(tmp_path)
        np.testing.assert_array_equal(loaded, test_matrices['A'])
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_text_format(test_matrices):
    """Test the text output format."""
    # Test text output with a matrix
    result = format_result(test_matrices['A'], format_type='text')
    
    # Check that all values are in the text output
    for row in test_matrices['A']:
        for val in row:
            assert str(int(val)) in result
    
    # Check for numpy formatting elements like square brackets
    assert '[' in result
    assert ']' in result


def test_text_scalar_format(test_matrices):
    """Test the text output format with a scalar."""
    # Test text output with a scalar
    result = format_result(test_matrices['scalar'], format_type='text')
    
    # Check the string representation contains the value
    assert "42.5" in result


def test_table_format(test_matrices):
    """Test the table output format."""
    # Test table output with a matrix
    result = format_result(test_matrices['A'], format_type='table')
    
    # Check for "Matrix Result" title
    assert "Matrix Result" in result
    
    # Check for all values in the table
    for row in test_matrices['A']:
        for val in row:
            assert str(int(val)) in result


def test_save_to_file_with_different_formats(test_matrices):
    """Test saving to file with different formats."""
    formats = ['text', 'csv', 'latex', 'json', 'plain']
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for fmt in formats:
            # Create a temporary file for output
            output_path = os.path.join(temp_dir, f"test_output.{fmt}")
            
            # Format result and write to file
            result_str = format_result(test_matrices['A'], format_type=fmt, output_path=output_path)
            
            # Check if file exists
            assert os.path.exists(output_path)
            
            # Check if result string indicates file was saved
            assert "saved to" in result_str
            assert output_path in result_str
            
            # Read the file and check contents
            with open(output_path, 'r') as f:
                content = f.read()
                
            # Basic check: file contains the number values
            for row in test_matrices['A']:
                for val in row:
                    # For plain text and some other formats, we need to allow for decimal points
                    pattern = rf"{int(val)}(\.0)?"
                    assert re.search(pattern, content), f"Value {val} not found in {fmt} output"


def test_scalar_formats(test_matrices):
    """Test various formats with scalar values."""
    # Test scalar with different formats
    formats = ['text', 'plain', 'json']
    for fmt in formats:
        result = format_result(test_matrices['scalar'], format_type=fmt)
        assert "42.5" in result


def test_tuple_result_formatting():
    """Test formatting tuple results (like from decompositions)."""
    # Create a tuple result (similar to what might be returned from np.linalg.svd)
    U = np.array([[1, 0], [0, 1]])
    S = np.array([5, 2])
    Vt = np.array([[0, 1], [1, 0]])
    
    tuple_result = (U, S, Vt)
    
    # Test with plain format
    result = format_result(tuple_result, format_type='plain')
    
    # Check that there are component markers
    assert "COMPONENT_0" in result
    assert "COMPONENT_1" in result
    assert "COMPONENT_2" in result
    
    # Test with other formats
    formats = ['text', 'json', 'table']
    for fmt in formats:
        result = format_result(tuple_result, format_type=fmt)
        assert "Component 0" in result
        assert "Component 1" in result
        assert "Component 2" in result