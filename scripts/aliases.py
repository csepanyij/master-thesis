import sqlite3
import gambit
import pandas as pd

def gambit_aliases(sqlite_db_file, repo_name):
    con = sqlite3.connect(sqlite_db_file)

    # Query the db
    data = pd.read_sql("""SELECT * FROM commits""", con)
    aliases = data[['author_name', 'author_email']]
    aliases = aliases.rename(columns={'author_email': 'alias_email', 'author_name': 'alias_name'})
    aliases = aliases.drop_duplicates()
    authors = gambit.disambiguate_aliases(aliases)
    authors.to_csv('../notebooks/databases/{r}/disambiguation.csv'.format(r=repo_name))

    for index, row in data.iterrows():
        #print(index, row['author_name'])
        if len(authors[(authors.alias_name == row['author_name']) & (authors.alias_email == row['author_email'])]['author_id']) == 1:
            auth_id = authors[(authors.alias_name == row['author_name']) & (authors.alias_email == row['author_email'])]['author_id'].values[0]
            data.loc[index, 'author_name'] = auth_id
        else:
            raise ValueError
            
    data.to_sql('commits', con, if_exists='replace')