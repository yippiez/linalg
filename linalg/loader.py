#!/usr/bin/env python3

import os
import numpy as np
import sys
from typing import List, Dict, Any, Optional


def load_matrices(file_paths: List[str], stdin_data: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Load NumPy arrays from .npy files and assign them to placeholders.
    
    Args:
        file_paths: List of file paths to .npy files
        stdin_data: Data from stdin when using piping (optional)
        
    Returns:
        Dictionary mapping placeholder names to NumPy arrays
    """
    matrices = {}
    
    # Check for reserved pipe.npy filename
    for file_path in file_paths:
        if os.path.basename(file_path) == "pipe.npy":
            raise ValueError("'pipe.npy' is a reserved filename for piping operations. "
                            "Use {PIPE} placeholder to access data from stdin.")
    
    # If stdin_data is provided, assign it to placeholder PIPE
    if stdin_data is not None:
        matrices["PIPE"] = stdin_data
    
    # Process regular files
    for file_path in file_paths:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check file extension
        if not file_path.endswith(".npy"):
            raise ValueError(f"File must be a .npy file: {file_path}")
        
        # Extract the file name without path and extension
        file_name = os.path.basename(file_path)
        placeholder_name = os.path.splitext(file_name)[0]
        
        # Check if the placeholder name is valid (single uppercase letter)
        if not (len(placeholder_name) == 1 and placeholder_name.isalpha() and placeholder_name.isupper()):
            raise ValueError(f"File name must be a single uppercase letter followed by .npy (e.g., A.npy): {file_path}")
        
        try:
            # Load the NumPy array
            matrix = np.load(file_path, allow_pickle=True)
            
            # Assign to placeholder
            matrices[placeholder_name] = matrix
            
        except Exception as e:
            raise ValueError(f"Error loading {file_path}: {str(e)}")
    
    return matrices


def read_from_stdin() -> Optional[np.ndarray]:
    """Read a NumPy array from stdin.
    
    Always tries to parse as binary NPY first, then falls back to text parsing.
    
    Returns:
        NumPy array from stdin or None if stdin is not available
    """
    # Check if stdin has data available
    if not sys.stdin.isatty():
        try:
            # Read binary data from stdin
            stdin_bytes = sys.stdin.buffer.read()
            
            # If stdin is empty, return None
            if not stdin_bytes:
                return None
                
            # Try to load as a NumPy array
            try:
                # First try to load as a .npy file
                from io import BytesIO
                return np.load(BytesIO(stdin_bytes))
            except Exception as e:
                # If that fails, try to load as plain text
                try:
                    from io import StringIO
                    text = stdin_bytes.decode('utf-8')
                    return np.loadtxt(StringIO(text))
                except Exception as text_e:
                    raise ValueError(f"Failed to parse input as NPY or text: {str(text_e)}")
        except Exception as e:
            raise ValueError(f"Error reading from stdin: {str(e)}")
    
    return None