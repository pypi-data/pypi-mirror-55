#!/usr/bin/env python
# filename: plot.py

import itertools
import os
import sys

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from abutils.utils import mongodb
from abutils.utils import color

import pymongo
from tqdm import tqdm

from natsort import natsorted

from .df import get_freq_df

def df_freq_barplot(df, cols=None):

    #get the columns
    if not cols:
        cols = list(df.columns)

    #melt the df
    df = df.melt(id_vars='index', value_vars=cols)

    #plot
    sns.barplot(data = df, x='index', y='value', hue='variable')
    
    
def QuickDataCheck(db, collections=None, index=False, values=None, match=None):
    # This function will quickly allow you to check the sequencing data of a database
    # database
    if type(db) == pymongo.database.Database:
        DB = db
    elif type(db) == str:
        DB = mongodb.get_db(db)
    else:
        print ('Database not correct')
        return
    
    if collections is None:
        colls = mongodb.get_collections(DB)
    else:
        colls = collections
    
    #index the collections if applicable 
    if index:
        print('Indexing Collections...')
        for collection in tqdm(colls):
            DB[collection].create_index([('chain', 1),
                                         ('prod', 1), 
                                         ('v_gene.gene', 1), 
                                         ('cdr3_len', 1)], 
                                        name='productive heavychain cdr3_len', 
                                        default_language='english')
    #if there is a set values, then use those
    if values:
        print('Getting data...')
        dfs = [get_freq_df(DB, colls, value, normalize=True, match=match) for value in values]

    else:
        print('Getting data...')
        values = ['v_gene.gene', 'cdr3_len']
        dfs = [get_freq_df(DB, colls, value, normalize=True, match=match) for value in values]
    
    #now plot the figures for each value
    for df, value in zip(dfs, values):
        print('-----------')
        print(value)
        print('-----------')
        for collection in df.columns:
            print(collection)
            #Try to plot the value unless the requested value is invalid
            try:
                df2 = pd.DataFrame(df[collection]).reset_index().melt(id_vars='index', value_vars=df.columns)
                try:
                    fam = [d.split('-')[0] for d in df2['index']]
                    df2['fam'] = fam
                except AttributeError:
                    None

                plt.figure(figsize=[12,4])
                try:
                    g = sns.barplot(data = df2, x='index', y='value', hue='fam', dodge=False) 
                except ValueError:
                    g = sns.barplot(data = df2, x='index', y='value', dodge=False)
                try:
                    g.get_legend().remove()
                except AttributeError:
                    None
                plt.xticks(rotation=90)
                plt.tight_layout()
                plt.show()
                print(' ')
            except ValueError:
                print('The value you requested is in valid')

