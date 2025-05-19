#!/usr/bin/env python3

import pytest
import sys
import os
import subprocess

# Add parent directory to path to import linalg
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linalg.prompt import generate_prompt


def test_generate_prompt():
    """Test that generate_prompt returns a non-empty string with expected content."""
    prompt = generate_prompt()
    
    # Check that it's a non-empty string
    assert isinstance(prompt, str)
    assert len(prompt) > 1000  # Should be a substantial text
    
    # Check for key sections
    sections = [
        "# Linalg - Linear Algebra Command-Line Calculator",
        "## Overview",
        "## Key Features",
        "### Matrix Placeholders",
        "### Supported Operations",
        "### Output Formats",
        "### Piping Support",
        "## Complete Usage Examples",
        "## Important Notes"
    ]
    
    for section in sections:
        assert section in prompt, f"Section '{section}' not found in prompt"
    
    # Check for key features and functions
    features = [
        "{A}+{B}",
        "{A}@{B}",
        "{A}.T",
        "det({A})",
        "text",
        "csv",
        "json",
        "latex",
        "plain",
        "{PIPE}",  # Changed from --pipe to {PIPE}
        "--pretty",
        "--format"
    ]
    
    for feature in features:
        assert feature in prompt, f"Feature '{feature}' not found in prompt"


def test_prompt_command():
    """Test that the --prompt command outputs the expected prompt content."""
    # Use subprocess to run the CLI with --prompt
    cmd = [sys.executable, "-m", "linalg", "--prompt"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check that command succeeded
    assert result.returncode == 0
    
    # Check that output contains the expected content
    prompt_output = result.stdout
    
    # Check for a few key sections
    assert "# Linalg - Linear Algebra Command-Line Calculator" in prompt_output
    assert "## Key Features" in prompt_output
    assert "### Matrix Placeholders" in prompt_output
    
    # Compare with generate_prompt output (should be the same)
    expected_prompt = generate_prompt()
    assert prompt_output.strip() == expected_prompt.strip()