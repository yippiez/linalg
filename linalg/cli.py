#!/usr/bin/env python3
"""
Command-line interface for the linalg calculator.

This module provides the main entry point for the linalg CLI tool.
"""

import sys
import argparse
from typing import List, Optional

from .parser import parse_expression
from .loader import load_matrices, read_from_stdin
from .evaluator import evaluate_expression
from .formatter import format_result
from .prompt import generate_prompt


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Linear algebra calculator for operations on NumPy arrays",
        prog="linalg",
    )
    
    # Add the prompt command that can be used independently
    parser.add_argument(
        "--prompt",
        action="store_true",
        help="Display comprehensive documentation for use with LLMs"
    )
    
    # Make expression and files optional so --prompt can be used alone
    parser.add_argument(
        "expression", 
        type=str,
        nargs="?",  # Make expression optional
        help="Expression string with placeholders like {A}, {B}, or {P} for piped input"
    )
    
    parser.add_argument(
        "files",
        nargs="*",
        help="NumPy .npy files to use as inputs"
    )
    
    # Removed the --pipe flag as stdin is now automatically detected
    # and made available as {PIPE} placeholder
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: print to console)"
    )
    
    parser.add_argument(
        "--npy", "-n",
        action="store_true",
        help="Use NPY format for output, writes binary data directly to stdout when piping between linalg commands"
    )
    
    parser.add_argument(
        "--precision",
        type=int,
        default=4,
        help="Decimal precision (default: 4)"
    )
    
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["text", "csv", "npy", "latex", "json", "table", "plain"],
        default="plain",  # Changed default from 'table' to 'plain'
        help="Output format (default: plain)"
    )
    
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Use pretty table output with colors (overrides --format to 'table')"
    )
    
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed execution"
    )
    
    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=1e-10,
        help="Hide values below threshold (default: 1e-10)"
    )
    
    parser.add_argument(
        "--components", "-c",
        action="store_true",
        help="For tuple outputs, save components separately"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
        help="Show version number and exit"
    )
    
    return parser


def get_version() -> str:
    """Get the current version of the package."""
    from importlib.metadata import version
    try:
        return version("linalg")
    except:
        return "0.1.0"  # Fallback for development


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    try:
        # Check if --prompt is specified
        if parsed_args.prompt:
            print(generate_prompt())
            return 0
            
        # Check if required arguments are present for normal operation
        if parsed_args.expression is None:
            parser.print_help()
            return 1
            
        # Always try to read from stdin if available
        stdin_data = read_from_stdin()
        if stdin_data is not None and parsed_args.verbose:
            print("Data detected from stdin, available as {PIPE} placeholder")
        
        # If no files provided and no stdin data, show help
        if not parsed_args.files and stdin_data is None:
            parser.print_help()
            return 1
        
        # Load matrices from files
        if parsed_args.verbose:
            print(f"Loading matrices from {len(parsed_args.files)} files...")
        matrices = load_matrices(parsed_args.files, stdin_data)
        
        # Parse the expression
        if parsed_args.verbose:
            print(f"Parsing expression: {parsed_args.expression}")
        ast = parse_expression(parsed_args.expression)
        
        # Evaluate the expression
        if parsed_args.verbose:
            print("Evaluating expression...")
        result = evaluate_expression(ast, matrices)
        
        # Format and output the result
        if parsed_args.verbose:
            print("Formatting result...")
            
        # Determine the output format
        format_type = parsed_args.format
        
        # If npy flag is set and no format is specified, use npy format
        if parsed_args.npy and format_type == 'plain':
            format_type = 'npy'
            
        # If pretty flag is set, override format_type to 'table'
        if parsed_args.pretty:
            format_type = 'table'
            
        # Determine if we should use plain mode (default) or pretty mode
        use_plain = format_type == 'plain' or (format_type == 'table' and not parsed_args.pretty)
            
        output = format_result(
            result,
            format_type=format_type,
            precision=parsed_args.precision,
            threshold=parsed_args.threshold,
            show_info=False,  # --info option removed
            output_path=parsed_args.output,
            save_components=parsed_args.components,
            plain=use_plain,
            write_to_stdout=(parsed_args.npy and format_type == 'npy')
        )
        
        # Print or save the result
        if parsed_args.output:
            if parsed_args.verbose:
                print(f"Result saved to {parsed_args.output}")
        else:
            # Output will be empty string if binary data was written directly to stdout
            if output:
                print(output)
            
        return 0
    
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())