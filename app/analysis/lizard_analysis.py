import subprocess

def run_lizard_analysis(repo_path):
    result = subprocess.run(["lizard", repo_path, "--json"], capture_output=True, text=True)
    return result.stdout
