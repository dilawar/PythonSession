"""parser_analyze.py: Parse and analyze monsson data.

Last modified: Sat Jan 18, 2014  05:01PM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import os
import sys
import re
import csv
from collections import Counter
from scipy.stats import poisson
import pandas as pd

def process(df):
    print("Processing ...")
    print(df)
    data = []
    for month in [5,6,7,8,9]:
        for year in [2004, 2005, 2006, 2007, 2008, 2009 ]:
            dfY = df[df.ix[:,2] == year]
            print(dfY)

def main(sheetpath):
    print("Opening sheets")
    df = pd.read_csv(sheetpath, header=None)
    process(df)

if __name__ == '__main__':
    sheet = sys.argv[1]
    main(sheet)
