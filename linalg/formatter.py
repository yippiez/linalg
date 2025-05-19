#!/usr/bin/env python3

import numpy as np
import os
import json
import csv
import sys
from typing import Dict, Any, Union, List, Tuple, Optional
from rich.console import Console
from rich.table import Table


# Type for results of evaluation
Result = Union[np.ndarray, float, Tuple[Any, ...]]


class Formatter:
    """Formatter for matrix calculation results."""
    
    def __init__(
        self,
        precision: int = 4,
        threshold: float = 1e-10,
        show_info: bool = False,
        plain: bool = False
    ):
        self.precision = precision
        self.threshold = threshold
        self.show_info = show_info
        self.plain = plain
        # Fixed the theme issue
        self.console = Console(color_system=None if plain else "auto")
    
    def format(
        self,
        result: Result,
        format_type: str,
        output_path: Optional[str] = None,
        save_components: bool = False,
        write_to_stdout: bool = False
    ) -> str:
        """Format a calculation result.
        
        Args:
            result: The result to format
            format_type: The format type (text, csv, npy, latex, json, table, plain)
            output_path: The output file path (if any)
            save_components: Whether to save tuple components separately
            write_to_stdout: Whether to write binary data to stdout (for piping)
            
        Returns:
            The formatted result string
        """
        # For binary output formats with piping, write directly to stdout
        if format_type == 'npy' and write_to_stdout and not output_path:
            # Save to stdout buffer without seeking position (which fails in pipes)
            from io import BytesIO
            buffer = BytesIO()
            np.save(buffer, result)
            sys.stdout.buffer.write(buffer.getvalue())
            sys.stdout.buffer.flush()
            return ""  # Return empty string since output was written directly
            
        # Determine the result type
        if isinstance(result, np.ndarray):
            return self._format_array(result, format_type, output_path)
        elif isinstance(result, (int, float, np.number)):
            return self._format_scalar(result, format_type, output_path)
        elif isinstance(result, tuple):
            return self._format_tuple(result, format_type, output_path, save_components)
        else:
            raise ValueError(f"Unsupported result type: {type(result)}")
    
    def _format_array(
        self,
        array: np.ndarray,
        format_type: str,
        output_path: Optional[str]
    ) -> str:
        """Format a NumPy array result."""
        # Apply threshold to small values
        array = np.where(np.abs(array) < self.threshold, 0, array)
        
        # Save to file if output path is provided
        if output_path:
            if format_type == 'npy':
                np.save(output_path, array)
                return f"Array saved to {output_path}"
            elif format_type in ['text', 'csv', 'latex', 'json', 'table', 'plain']:
                return self._save_array_to_file(array, format_type, output_path)
        
        # Create formatted string
        if format_type == 'text':
            return np.array2string(array, precision=self.precision, suppress_small=True)
        elif format_type == 'csv':
            return self._array_to_csv_str(array)
        elif format_type == 'latex':
            return self._array_to_latex(array)
        elif format_type == 'json':
            return self._array_to_json(array)
        elif format_type == 'table':
            return self._array_to_table(array)
        elif format_type == 'plain':
            return self._array_to_plain(array)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def _format_scalar(
        self,
        scalar: Union[int, float, np.number],
        format_type: str,
        output_path: Optional[str]
    ) -> str:
        """Format a scalar result."""
        # Apply threshold to small values
        if abs(scalar) < self.threshold:
            scalar = 0
        
        # Format as string
        formatted = f"{scalar:.{self.precision}g}"
        
        # Save to file if output path is provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(formatted)
            return f"Scalar saved to {output_path}"
        
        return formatted
    
    def _format_tuple(
        self,
        tuple_result: Tuple[Any, ...],
        format_type: str,
        output_path: Optional[str],
        save_components: bool
    ) -> str:
        """Format a tuple result (e.g., from decompositions)."""
        if save_components and output_path:
            # Save each component separately
            base_path, ext = os.path.splitext(output_path)
            if not ext:
                ext = '.npy' if format_type == 'npy' else '.txt'
            
            for i, component in enumerate(tuple_result):
                component_path = f"{base_path}_{i}{ext}"
                if isinstance(component, np.ndarray):
                    if format_type == 'npy':
                        np.save(component_path, component)
                    else:
                        self._save_array_to_file(component, format_type, component_path)
                else:
                    with open(component_path, 'w') as f:
                        f.write(str(component))
            
            return f"Components saved to {base_path}_*{ext}"
        
        # Format as string
        result_parts = []
        for i, component in enumerate(tuple_result):
            if isinstance(component, np.ndarray):
                component_str = self._format_array(component, format_type, None)
            else:
                component_str = str(component)
            
            if format_type == 'plain':
                # Simple separator for plain format
                result_parts.append(f"COMPONENT_{i}")
                result_parts.append(component_str)
            else:
                result_parts.append(f"Component {i}:\n{component_str}")
        
        return "\n\n".join(result_parts)
    
    def _array_to_csv_str(self, array: np.ndarray) -> str:
        """Convert a NumPy array to a CSV string."""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        if array.ndim == 1:
            writer.writerow(array)
        else:
            writer.writerows(array)
        
        return output.getvalue()
    
    def _array_to_latex(self, array: np.ndarray) -> str:
        """Convert a NumPy array to a LaTeX representation."""
        if array.ndim == 1:
            array = array.reshape(1, -1)
        
        rows = []
        rows.append(r"\begin{bmatrix}")
        
        for row in array:
            row_str = " & ".join([f"{x:.{self.precision}g}" for x in row])
            rows.append(row_str + r" \\")
        
        rows.append(r"\end{bmatrix}")
        return "\n".join(rows)
    
    def _array_to_json(self, array: np.ndarray) -> str:
        """Convert a NumPy array to a JSON string."""
        return json.dumps(array.tolist(), indent=2)
    
    def _array_to_plain(self, array: np.ndarray) -> str:
        """Convert a NumPy array to a plain text format suitable for piping."""
        if array.ndim == 1:
            # For 1D arrays, one value per line
            return "\n".join([f"{x:.{self.precision}g}" for x in array])
        else:
            # For 2D+ arrays, tab-separated values with newlines between rows
            rows = []
            for row in array:
                rows.append("\t".join([f"{x:.{self.precision}g}" for x in row]))
            return "\n".join(rows)
    
    def _array_to_table(self, array: np.ndarray) -> str:
        """Convert a NumPy array to a pretty-printed table."""
        import io
        output = io.StringIO()
        console = Console(file=output, width=120, color_system=self.console.color_system)
        
        table = Table(title="Matrix Result")
        
        # Add columns
        if array.ndim == 1:
            for i in range(array.shape[0]):
                table.add_column(f"[{i}]")
            
            table.add_row(*[f"{x:.{self.precision}g}" for x in array])
        else:
            # Add column headers
            for i in range(array.shape[1]):
                table.add_column(f"[{i}]")
            
            # Add rows
            for i, row in enumerate(array):
                table.add_row(*[f"{x:.{self.precision}g}" for x in row])
        
        console.print(table)
        
        # Add matrix info if requested
        if self.show_info:
            console.print(f"\nShape: {array.shape}")
            if array.ndim == 2:
                console.print(f"Rank: {np.linalg.matrix_rank(array)}")
                if array.shape[0] == array.shape[1]:  # Square matrix
                    console.print(f"Determinant: {np.linalg.det(array):.{self.precision}g}")
                    console.print(f"Trace: {np.trace(array):.{self.precision}g}")
            
            console.print(f"Min: {np.min(array):.{self.precision}g}")
            console.print(f"Max: {np.max(array):.{self.precision}g}")
            console.print(f"Mean: {np.mean(array):.{self.precision}g}")
            console.print(f"Std: {np.std(array):.{self.precision}g}")
        
        return output.getvalue()
    
    def _save_array_to_file(
        self,
        array: np.ndarray,
        format_type: str,
        output_path: str
    ) -> str:
        """Save a NumPy array to a file."""
        if format_type == 'text':
            np.savetxt(output_path, array, fmt=f'%.{self.precision}g')
        elif format_type == 'csv':
            np.savetxt(output_path, array, fmt=f'%.{self.precision}g', delimiter=',')
        elif format_type == 'latex':
            with open(output_path, 'w') as f:
                f.write(self._array_to_latex(array))
        elif format_type == 'json':
            with open(output_path, 'w') as f:
                json.dump(array.tolist(), f, indent=2)
        elif format_type == 'table':
            with open(output_path, 'w') as f:
                f.write(self._array_to_table(array))
        elif format_type == 'plain':
            with open(output_path, 'w') as f:
                f.write(self._array_to_plain(array))
        
        return f"Array saved to {output_path}"


def format_result(
    result: Result,
    format_type: str = 'table',
    precision: int = 4,
    threshold: float = 1e-10,
    show_info: bool = False,
    output_path: Optional[str] = None,
    save_components: bool = False,
    plain: bool = False,
    write_to_stdout: bool = False
) -> str:
    """Format a calculation result.
    
    Args:
        result: The result to format
        format_type: The format type (text, csv, npy, latex, json, table, plain)
        precision: Decimal precision for display
        threshold: Hide values below this threshold
        show_info: Whether to show additional information about matrices
        output_path: The output file path (if any)
        save_components: Whether to save tuple components separately
        plain: Whether to use plain formatting (no colors, simplified output)
        write_to_stdout: Whether to write binary data to stdout (for piping)
        
    Returns:
        The formatted result string
    """
    formatter = Formatter(precision, threshold, show_info, plain)
    return formatter.format(result, format_type, output_path, save_components, write_to_stdout)