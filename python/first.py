import pygit2 as git2
import os
import shutil
import git2net
import pathpy as pp


git_repo_url = 'https://github.com/gotec/git2net.git'
local_directory = '.'
git_repo_dir = '../git2net'

# if os.path.exists(git_repo_dir):
#     shutil.rmtree(git_repo_dir)

#repo = git2.clone_repository(git_repo_url, git_repo_dir) # Clones a non-bare repository

sqlite_db_file = 'git2net.db'

# Remove database if exists
if os.path.exists(sqlite_db_file):
    os.remove(sqlite_db_file)

max_modifications = 1
#max_modifications = 5
    
git2net.mine_git_repo(git_repo_dir, sqlite_db_file, max_modifications=max_modifications)

git2net.mining_state_summary(git_repo_dir, sqlite_db_file)

t, node_info, edge_info = git2net.get_coediting_network(sqlite_db_file)
t

n = pp.Network.from_temporal_network(t)

colour_map = {'author': '#73D2DE', 'file': '#2E5EAA'}
node_color = {node: colour_map[node_info['class'][node]] for node in n.nodes}
pp.visualisation.plot(n, node_color=node_color)