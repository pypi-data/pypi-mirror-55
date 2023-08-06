#!/usr/bin/env python
# filename: df.py

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

from natsort import natsorted


def get_freq_df(db, collections, value, chain='heavy', match=None, normalize = False):

    # database
    if type(db) == pymongo.database.Database:
        DB = db
    elif type(db) == str:
        DB = mongodb.get_db(db)
    else:
        print ('Database not correct')
        return
    
    if type(collections) == list:
        collections = collections
    else:
        collections = [collections, ]
    
    if not match:
        match = {'chain': chain, 'prod': 'yes'}
    group = {'_id': '${}'.format(value), 'count': {'$sum': 1}}

    # initialize a dictionary that will hold all of the DataFrames we're making (one per subject)
    data = {}

        
    # iterate through each of the collections in the subject group
    for collection in collections:
        #print(collection)
        data[collection] = {}

        # get the aggregation data from MongoDB
        res = DB[collection].aggregate([{'$match': match}, {'$group': group}])

        # convert the MongoDB aggregation result into a dictionary iof V-gene counts
        for r in res:
            data[collection][r['_id']] = r['count']

    #print('')

    # construct a DataFrame from the dictionary of V-gene counts
    df = pd.DataFrame(data)
    
    if normalize:
        df = df / df.sum()
        df = df.dropna(0)

    return df