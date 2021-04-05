import os
import shutil
import git2net
import pygit2 as git2
from pathlib import Path


def clone_repo(git_repo_dir, git_repo_url, delete_existing=True):
    if os.path.exists(git_repo_dir) and delete_existing:
        shutil.rmtree(git_repo_dir)

    repo = git2.clone_repository(git_repo_url, git_repo_dir) # Clones a non-bare repository
    return repo


def mine_repo(git_repo_dir, sqlite_db_file, max_modifications=100, delete_existing=False):
    # Remove database if exists
    if os.path.exists(sqlite_db_file):
        if delete_existing:
            os.remove(sqlite_db_file)
    else:
        Path(os.path.dirname(os.path.abspath(sqlite_db_file))).mkdir(parents=True, exist_ok=True)
        #os.mkdir(os.path.dirname(os.path.abspath(sqlite_db_file)))
    
    #print(git_repo_dir)
    #print(sqlite_db_file)
        
    git2net.mine_git_repo(git_repo_dir, sqlite_db_file, max_modifications=max_modifications, no_of_processes=7)
    git2net.mining_state_summary(git_repo_dir, sqlite_db_file)