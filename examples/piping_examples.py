#!/usr/bin/env python3
"""
Examples of using linalg with piping.

This script demonstrates how to use the linalg CLI tool with piping.
It creates example matrices and shows various piping operations.
"""

import os
import numpy as np
import tempfile
import subprocess
from pathlib import Path


def save_example_matrices(directory: str) -> dict:
    """Save example matrices to a directory.
    
    Args:
        directory: Directory to save matrices to
        
    Returns:
        Dictionary of matrix paths
    """
    # Create example matrices
    A = np.array([[1, 2], [3, 4]])  # 2x2 matrix
    B = np.array([[5, 6], [7, 8]])  # 2x2 matrix
    
    # Save matrices to files
    A_path = os.path.join(directory, 'A.npy')
    B_path = os.path.join(directory, 'B.npy')
    np.save(A_path, A)
    np.save(B_path, B)
    
    return {
        'A': A_path,
        'B': B_path
    }


def run_command(command: list, input_data: bytes = None) -> str:
    """Run a command and return the output.
    
    Args:
        command: Command to run
        input_data: Optional input data for stdin
        
    Returns:
        Command output
    """
    print(f"Running: {' '.join(command)}")
    
    result = subprocess.run(
        command,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )
    
    return result.stdout.decode('utf-8').strip()


def main():
    """Run piping examples."""
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Save example matrices
        matrix_paths = save_example_matrices(temp_dir)
        A_path = matrix_paths['A']
        B_path = matrix_paths['B']
        
        # Find the linalg executable
        # In a real project this would be just 'linalg' once installed
        linalg_path = str(Path(__file__).parent.parent / ".venv" / "bin" / "linalg")
        
        print("\n----- Basic Examples -----")
        
        # Example 1: Using plain format for pipeable output
        print("\nExample 1: Using plain format for easier parsing")
        output = run_command([linalg_path, "{A}+{B}", A_path, B_path, "--plain"])
        print(f"Output:\n{output}")
        
        print("\n----- Piping Examples -----")
        
        # Example 2: Pipe a numpy array into linalg
        print("\nExample 2: Piping data into linalg")
        with open(A_path, 'rb') as f:
            input_data = f.read()
        
        output = run_command(
            [linalg_path, "{PIPE}+{B}", B_path, "--plain"],
            input_data=input_data
        )
        print(f"Output:\n{output}")
        
        # Example 3: Chain operations by piping between linalg commands
        print("\nExample 3: Chaining linalg operations (simulation)")
        print("In a real terminal, you would run:")
        print(f"{linalg_path} '{{A}}+{{B}}' {A_path} {B_path} --npy | "
              f"{linalg_path} 'det({{PIPE}})'")
        
        # We'll simulate this for demonstration
        # First command: A+B in binary format
        cmd1 = [linalg_path, "{A}+{B}", A_path, B_path, "--npy"]
        result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, check=True)
        
        # Second command: det(PIPE) 
        cmd2 = [linalg_path, "det({PIPE})", "--plain"]
        result2 = subprocess.run(cmd2, input=result1.stdout, stdout=subprocess.PIPE, check=True)
        
        print(f"Output: {result2.stdout.decode('utf-8').strip()}")
        
        # Example 4: Error when using pipe.npy (reserved filename)
        print("\nExample 4: Using reserved filename 'pipe.npy' (should error)")
        # Create a pipe.npy file
        pipe_path = os.path.join(temp_dir, 'pipe.npy')
        np.save(pipe_path, np.array([[1, 2], [3, 4]]))
        
        try:
            output = run_command([linalg_path, "{A}", pipe_path])
            print(f"Output:\n{output}")
        except subprocess.CalledProcessError as e:
            print(f"Expected error: {e.stderr.decode('utf-8').strip()}")


if __name__ == "__main__":
    main()