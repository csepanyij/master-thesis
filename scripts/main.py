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

import aliases
import mining
#import networks
#import statistics

#git_repo_url = 'https://github.com/servo/servo'
#repo_name = 'servo'
#local_directory = '.'
#git_repo_dir = 'repos/{r}4analysis'.format(r=repo_name)
#sqlite_db_file = 'databases/{r}/{r}_rename.db'.format(r=repo_name)
#sqlite_db_file = 'databases/{r}/{r}.db'.format(r=repo_name)

with open('../notebooks/sampling/releases_corrected.json', 'r') as f:
    repositories = json.load(f)

c = len(repositories)
i = 0
for repo_name in repositories:
    i = i + 1
    print('\n\nMining repository {i} / {c}'.format(i=i, c=c))
    print('Current repository: {repo_name}\n'.format(repo_name=repo_name))
    git_repo_url = 'https://github.com/{r}'.format(r=repo_name)
    git_repo_dir = '../notebooks/repos/{r}4analysis'.format(r=repo_name) 
    sqlite_db_file = '../notebooks/databases/{r}/{r2}.db'.format(r=repo_name, r2=repo_name.split('/')[1])

    if not os.path.exists(git_repo_dir):
        # 1. Clone project
        print('Phase 1: Cloning repository...')
        mining.clone_repo(git_repo_dir, git_repo_url)
        print('Done.\n')
        time.sleep(3)

    if not os.path.exists(sqlite_db_file):
        # 2. Mine project
        print('Phase 2: Mining repository...\n')
        mining.mine_repo(git_repo_dir, sqlite_db_file)
        print('Done.\n')
        time.sleep(3)
        
    if os.path.exists('../notebooks/databases/{r}/disambiguation.csv'.format(r=repo_name)):
        skip_disambig = True

    if not skip_disambig:
        # 3. Disambiguate
        print('Phase 3: Disambiguating authors...\n')
        aliases.gambit_aliases(sqlite_db_file, repo_name)
        print('Done.\n')
        time.sleep(3)
        