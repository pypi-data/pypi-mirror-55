#!/usr/bin/env python
# filename: mangodb.py


#
# Copyright (c) 2015 Bryan Briney
# License: The MIT license (http://opensource.org/licenses/MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import platform
import os
import subprocess as sp
import sys

from pymongo import MongoClient

from . import log

if sys.version_info[0] > 2:
    STR_TYPES = [str, ]
else:
    STR_TYPES = [str, unicode]










def list_dbs(ip='localhost', port=27017, user=None, connect=True, hint=None):
    '''
    Returns a list of Databases.
    .. note:
        Both ``user`` and ``password`` are required when connecting to a MongoDB
        database that has authentication enabled.
    Arguments:
        db (str): Name of the MongoDB database. Required.
        ip (str): IP address of the MongoDB server. Default is ``localhost``.
        port (int): Port of the MongoDB server. Default is ``27017``.
        user (str): Username, if authentication is enabled on the MongoDB database.
            Default is ``None``, which results in requesting the connection
            without authentication.
        password (str): Password, if authentication is enabled on the MongoDB database.
            Default is ``None``, which results in requesting the connection
            without authentication.
            
        hint (str): substring found in database name, if used only list of 
            databases that contain the substring will returned
    '''
    
    #Darwin says "you shall not connect!"
    if platform.system().lower() == 'darwin':
        connect = False
    else:
        connect = True
    
    # check for user and pass, if so: make uri, import urllib, return dbs
    if user and password:
        import urllib
        pwd = urllib.quote_plus(password)
        uri = 'mongodb://{}:{}@{}:{}'.format(user, pwd, ip, port)
        #check to see if hint was passed in and return list of dbs with hint
        if hint and type(hint) == str:
            ls = MongoClient(uri, connect=connect).list_database_names()
            return [d for d in ls if hint.upper() in d.upper()]
        #otherwise return a list of all dbs
        else:
            return MongoClient(uri, connect=connect).list_database_names()
        
    #otherwise no user or pass required    
    else:
        #check to see if hint was passed in and return list of dbs with hint
        if hint and type(hint) == str:
            ls = MongoClient(ip, port, connect=connect).list_database_names()
            return [d for d in ls if hint.upper() in d.upper()]
        #otherwise return a list of all dbs
        else:
            return MongoClient(ip, port, connect=connect).list_database_names()