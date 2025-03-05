"""
import os
import tempfile
import git

def clone_repo(repo_url):
#    temp_dir = tempfile.mkdtemp()
#    git.Repo.clone_from(repo_url, temp_dir)
     repo_path = os.path.join("/var/tmp", repo_name)  # Store repo persistently
     git.Repo.clone_from(repo_url, repo_path)
     return temp_dir

import os
import git
from urllib.parse import urlparse

def clone_repo(repo_url):
    # Extract repository name from the URL
    repo_name = os.path.basename(urlparse(repo_url).path).replace(".git", "")
    
    # Define persistent storage path
    repo_path = os.path.join("/var/tmp", repo_name)  
    
    # Clone the repository
    git.Repo.clone_from(repo_url, repo_path)
    
    return repo_path  # Return the correct repo path

"""
import os
import shutil
import git

def clone_repo(repo_url):
    """Clones the given GitHub repository to a temporary directory."""
    repo_name = repo_url.split("/")[-1]
    repo_path = f"/var/tmp/{repo_name}"

    # If the directory exists, delete it before cloning
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    # Clone the repository
    git.Repo.clone_from(repo_url, repo_path)
    return repo_path

