import subprocess

def run_pylint_analysis(repo_path):
    result = subprocess.run(["pylint", repo_path, "--output-format=json"], capture_output=True, text=True)
    return result.stdout
