import subprocess

def run_bandit_analysis(repo_path):
    result = subprocess.run(["bandit", "-r", repo_path, "-f", "json"], capture_output=True, text=True)
    return result.stdout
