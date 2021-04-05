import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.dates as mdates
import git2net
import pathpy as pp

import networks


def plot_commit_frequency(sqlite_db_file, repo_name):
    db = sqlite3.connect(sqlite_db_file)
    max_date = datetime.strptime(pd.read_sql_query("SELECT max(committer_date) as max FROM commits", db)['max'].item(), '%Y-%m-%d %H:%M:%S')
    min_date = datetime.strptime(pd.read_sql_query("SELECT min(committer_date) as min FROM commits", db)['min'].item(), '%Y-%m-%d %H:%M:%S')

    print('Min date: ', min_date)
    print('Max date: ', max_date)

    pdCommits = pd.read_sql_query("SELECT * FROM commits", db)

    days = {(min_date+timedelta(days=x)).date() : 0 for x in range((max_date-min_date).days + 1)}

    commit_dates = pdCommits['committer_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date()).value_counts()

    for key in commit_dates.keys():
        days[key] = commit_dates.get(key)

    keys = days.keys()
    values = days.values()
    plt.figure(figsize=(20,5))
    plt.savefig('exports/{r}/commit_freq.png'.format(r=repo_name))
    #plt.bar(keys, values)


def networks_for_stats(sqlite_db_file, git_repo_dir, min_date=None, max_date=None):
    #stats = network_stats(n1)
    #stats

    db = sqlite3.connect(sqlite_db_file)
    if not max_date:
        max_date = datetime.strptime(pd.read_sql_query("SELECT max(committer_date) as max FROM commits", db)['max'].item(), '%Y-%m-%d %H:%M:%S')
    if not min_date:
        min_date = datetime.strptime(pd.read_sql_query("SELECT min(committer_date) as min FROM commits", db)['min'].item(), '%Y-%m-%d %H:%M:%S')
    #max_date = datetime.strptime('2020-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')
    #min_date = datetime.strptime('2019-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    print('Min date: ', min_date)
    print('Max date: ', max_date)

    t, node_info, edge_info = git2net.get_bipartite_network(sqlite_db_file, time_from=min_date, time_to=max_date)

    timespan = timedelta(days=30) # Timespan to be considered for the stats
    days = {(min_date+timedelta(days=x)).date() : 0 for x in range((max_date-min_date-timespan).days + 1)}
    mx, myj1, myj2, myj3, myj4, myj5 = [], [], [], [], [], []
    my1, my2, my3, my4, my5 = [], [], [], [], []

    for day in days:
        print(day.strftime('%Y-%m-%d'))
        mx.append(day)
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day+timespan, datetime.min.time())
        #n = collab_network(sqlite_db_file, git_repo_dir, t, node_info, day, day+timespan, True)
        n = networks.collab_network_jaccard(sqlite_db_file, git_repo_dir, t, node_info, start, end, True)
        stats=network_stats(n)
        myj1.append(stats['N'])
        myj2.append(stats['Network density'])
        myj3.append(stats['Clustering coeff.'])
        myj4.append(stats['Number of Components'])
        myj5.append(stats['Mean degree'])
        #n = collab_network(sqlite_db_file, git_repo_dir, t, node_info, start, end, True)
        #stats=network_stats(n, True)
        #my1.append(stats['N'])
        #my2.append(stats['Network density'])
        #my3.append(stats['Clustering coeff.'])
        #my4.append(stats['Number of Components'])
        #my5.append(stats['Mean degree'])


def network_stats(n, directed=False):
    d = {}
    N = len(n.nodes)
    
    # Node count
    d['N'] = N
    
    # Network density
    d['Network density'] = len(n.edges) / (N * (N - 1)) if N > 1 else 0
    
    # Clustering coefficient
    d['Clustering coeff.'] = pp.algorithms.statistics.avg_clustering_coefficient(n)
    
    # COnnected components
    try:
        d['Number of Components'] = len(pp.algorithms.components.connected_components(n))
    except ValueError:
        d['Number of Components'] = -1
    #d['Connected Components'] = pp.algorithms.components.connected_components(n)
    
    # Average degree
    if directed:
        d['Mean degree'] = pp.algorithms.statistics.mean_degree(n, degree='indegree')
    else:
        d['Mean degree'] = pp.algorithms.statistics.mean_degree(n, degree='degree')
    #d['Mean outdegree'] = pp.algorithms.statistics.mean_degree(n, degree='indegree')
    return d

#print(network_stats(n1))


def save_stats_plot(repo_name, mx, myj1, myj2, myj3, myj4, myj5):
    fig = plt.figure(figsize=(6, 4), dpi=80)
    gs = fig.add_gridspec(2, 2, hspace=0.2, wspace=0.18)
    (ax1, ax2), (ax3, ax4) = gs.subplots(sharex=True)
    #fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True)
    myFmt = mdates.DateFormatter('%Y-%m')
    gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
    #fig.suptitle('{repo_name} network stats around major event (2020-08-11)'.format(repo_name=repo_name))
    
    ax1.set_title('Node count')
    #ax1.plot(mx, my1, label = "N (m)", color = "#212AA5")
    ax1.plot(mx, myj1, label = "N (mj)", color = "#7B9FF2")
    #ax1.plot(wx, wy1, label = "N (w)", color = "#9E1711")
    #ax1.plot(wx, wyj1, label = "N (wj)", color = "#D65D72")
    ax1.axvline(x=datetime(2020, 1, 15), color='black', ls='--')
    ax1.axvline(x=datetime(2020, 8, 11), color='black', ls='--')
    ax1.xaxis.set_major_formatter(myFmt)
    #ax1.legend()
    
    ax4.set_title('Network density')
    #ax4.plot(mx, my2, label = "Network density (m)", color = "#212AA5")
    ax4.plot(mx, myj2, label = "Network density (mj)", color = "#7B9FF2")
    #ax4.plot(wx, wy2, label = "Network density (weekly)", color = "#9E1711")
    #ax4.plot(wx, wyj2, label = "Network density (weekly, jaccard)", color = "#D65D72")
    ax4.axvline(x=datetime(2020, 1, 15), color='black', ls='--')
    ax4.axvline(x=datetime(2020, 8, 11), color='black', ls='--')
    ax4.xaxis.set_major_formatter(myFmt)
    #ax4.legend()
    
    ax3.set_title('Clustering coefficient')
    #ax3.plot(mx, my3, label = "Clustering coeff. (m)", color = "#212AA5")
    ax3.plot(mx, myj3, label = "Clustering coeff. (mj)", color = "#7B9FF2")
    #ax3.plot(wx, wy3, label = "Clustering coeff. (weekly)", color = "#9E1711")
    #ax3.plot(wx, wyj3, label = "Clustering coeff. (weekly, jaccard)", color = "#D65D72")
    ax3.axvline(x=datetime(2020, 1, 15), color='black', ls='--')
    ax3.axvline(x=datetime(2020, 8, 11), color='black', ls='--')
    ax3.xaxis.set_major_formatter(myFmt)
    #ax3.legend()
    
    #ax4.plot(mx, my4, label = "Number of Components (monthly)", color = "#212AA5")
    #ax4.plot(mx, myj4, label = "Number of Components (monthly, jaccard)", color = "#7B9FF2")
    #ax4.plot(wx, wy4, label = "Number of Components (weekly)", color = "#9E1711")
    #ax4.plot(wx, wyj4, label = "Number of Components (weekly, jaccard)", color = "#D65D72")
    #ax4.legend()
    
    ax2.set_title('Mean degree')
    #ax2.plot(mx, my5, label = "Mean degree (m)", color = "#212AA5")
    ax2.plot(mx, myj5, label = "Mean degree (mj)", color = "#7B9FF2")
    #ax2.plot(wx, wy5, label = "Mean degree (w)", color = "#9E1711")
    #ax2.plot(wx, wyj5, label = "Mean degree (wj)", color = "#D65D72")
    ax2.axvline(x=datetime(2020, 1, 15), color='black', ls='--')
    ax2.axvline(x=datetime(2020, 8, 11), color='black', ls='--')
    ax2.xaxis.set_major_formatter(myFmt)
    #ax2.legend()
    
    plt.savefig('exports/{r}/network_stats.png'.format(r=repo_name))
    fig.autofmt_xdate()