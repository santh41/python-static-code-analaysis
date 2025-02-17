import subprocess

def run_radon_analysis(repo_path):
    result = subprocess.run(["radon", "cc", "-a", repo_path, "--json"], capture_output=True, text=True)
    return result.stdout
