import pandas as pd
import re

def rem_unwanted(line):
    return re.sub("\'term'|\'rel'|\'href'|\'type'|\'title'|\[|\{|\'name'|\'|\]|\,|\}",'',line).strip(' ').strip("''").strip(":")

def rem_bracket(line):
    return line.strip(')')

def arxiv_clean(df):

    #Creating a dataframe with author names and preprocessing it
    df2 = pd.DataFrame(df.author.str.split('}').tolist(), index=df.index).stack() #Cleaning author names
    df2 = pd.DataFrame(df2.apply(rem_unwanted))
    df2 = pd.DataFrame(df2.unstack().iloc[:, 0:2].to_records()).drop(columns={'index'})
    df2.columns = ['Author1', 'Author2']
    df2.Author1 = df2.Author1.str.strip(' ')
    df2.Author2 = df2.Author2.str.strip(' ')
    df2 = df2.reset_index().drop(columns='index')

    #Creating a dataframe with links to pdfs and preprocessing it
    df3 = pd.DataFrame(df.link.str.split(', ').tolist(), index=df.index).stack()
    df3 = pd.DataFrame(df3.apply(rem_unwanted, convert_dtype=True))
    df3 = df3.unstack()
    links = df3.iloc[:, [1, 4]]
    links.columns = ['textLink', 'pdfLink']
    # Cleaning topics to get subjects of articles:
    tags = pd.DataFrame(df['tag'].str.split(',').tolist())
    tags = tags.iloc[:, [0, 3, 6]].stack()
    tags = tags.apply(rem_unwanted)
    tags = tags.unstack()
    tags[0] = tags[0].str.strip()
    tags.iloc[:, 1] = tags.iloc[:, 1].str.strip()
    tags.iloc[:, 2] = tags.iloc[:, 2].str.strip()
    tags.columns = ['Topic1', 'Topic2', 'Topic3']

    # Merging all dfs
    pre0 = pd.merge(df, tags, how='inner', left_index=True, right_index=True).drop('tag', axis=1)
    pre = pd.merge(pre0, df2, how='inner', left_index=True, right_index=True).drop('author', axis=1)
    data = pd.merge(pre, links, how='inner', left_index=True, right_index=True).drop('link', axis=1)

    return data

