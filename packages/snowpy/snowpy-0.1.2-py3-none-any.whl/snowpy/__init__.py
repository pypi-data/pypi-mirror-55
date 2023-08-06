# -*- coding: utf-8 -*-
# SnowPy (SnowPy)

__docformat__ = 'restructuredtext'
__name__="snowpy"
__distname__="snowpy"
__version__="0.1.2"
__description__= 'A Python library to upload and download data from database systems'
__author__="Sumudu Tennakoon"
__url__="https://mltoolkit.github.io/SnowPy"
__create_date__="Sat Sep 28 2019"
__last_update__="Sat Nov 16 2019"
__license__="""
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""
__doc__="""
SnowPy - A Python library to upload and download data from database systems
===========================================================++++++++++++++++++++
'SnowPy' is a Python package providing a set of user-friendly functions to 
help upload and download data from database systems such as Microsoft SQL Server,
 Snowflake, (more to come). 'SnowPy' intially realsed as data tools for the 
 mltoolkit project ((https://mltoolkit.github.io/MLToolKit)

Required Dependancies
---------------------
- Numpy
- Pandas
- PyODBC
- SQLAlchemy
- PyMLToolKit
- Snowflake-Connector-Python
- Snowflake-SQLAlchemy

Main Features
-------------
- Upload Data To Database Server
- Download Data From Database Server
- Performance Enhanced Data Transfer Functions (in progress)

Author
------
- Sumudu Tennakoon

Links
-----
Website: http://sumudu.tennakoon.net/projects/MLToolkit
Github: https://mltoolkit.github.io/SnowPy

License
-------
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

hard_dependencies = ('numpy', 'scipy', 'matplotlib', 'pandas','sklearn', 'statsmodels', 'pyodbc', 'sqlalchemy') #'snowflake') #,'re', 'tensorflow', 'catboost') #'tensorflow'
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Following packages are required but missing in the Python distribution: {}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from datetime import datetime
import gc
import traceback
import gc
import os
from timeit import default_timer as timer
import re
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# Package scripts
from snowpy.datatools import *
from snowpy.process import *

print('snowpy=={}'.format(__version__.strip()))
###############################################################################
#                           SET DISPLAY ENVIRONMENT                           #
###############################################################################
pd.set_option("display.max_columns",1000)
pd.set_option("display.max_rows",500)
pd.set_option('expand_frame_repr', False)
pd.set_option('large_repr', 'truncate')
pd.set_option('precision', 5)
###############################################################################


"""

"""


    
    