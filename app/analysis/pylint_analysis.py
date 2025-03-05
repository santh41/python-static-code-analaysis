"""
import subprocess

def run_pylint_analysis(repo_path):
    result = subprocess.run(["pylint", repo_path, "--output-format=json"], capture_output=True, text=True)
    return result.stdout
"""

import os
import subprocess
import tempfile

def run_pylint(repo_path):
    """Runs pylint on the given repository path and returns formatted output."""
    if not os.path.exists(repo_path):
        return "Error: Repository path does not exist."

    output_file = tempfile.NamedTemporaryFile(delete=False)
    output_path = output_file.name
    output_file.close()

    pylint_command = [
        "pylint",
        repo_path,
        "--output-format=json"
    ]

    try:
        subprocess.run(pylint_command, stdout=open(output_path, "w"), stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        return "Error: Pylint encountered an issue."

    # Read the output
    with open(output_path, "r") as f:
        pylint_results = f.read()

    os.remove(output_path)
    return pylint_results

