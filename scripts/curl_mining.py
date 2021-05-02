import pygit2 as git2
import os
import shutil
import git2net
import pathpy as pp
import sqlite3
import pandas as pd
from datetime import date, datetime, timedelta
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.dates as mdates
import json 
import math
import copy
import networkx
import gambit
import time
from pathlib import Path

repo_name = 'curl/curl'

git_repo_url = 'https://github.com/{r}'.format(r=repo_name)
git_repo_dir = '../notebooks/repos/{r}4analysis'.format(r=repo_name) 
sqlite_db_file = '../notebooks/databases/{r}/{r2}.db'.format(r=repo_name, r2=repo_name.split('/')[1])

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
        
    git2net.mine_git_repo(git_repo_dir, sqlite_db_file, max_modifications=max_modifications)
    #git2net.mining_state_summary(git_repo_dir, sqlite_db_file)

#clone_repo(git_repo_dir, git_repo_url)
mine_repo(git_repo_dir, sqlite_db_file)