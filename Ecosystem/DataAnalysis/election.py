#!/usr/bin/env python3
"""election_poisson.py: 
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import pandas
import matplotlib as mpl
# mpl.use( 'pgf' )
import matplotlib.pyplot as plt
mpl.style.use( ['bmh', 'fivethirtyeight'] )

def read_data(filename):
    df = pandas.read_csv(filename)
    #  df = df.drop(columns=['Party Name', 'Candidate Name', 'Name of State/ UT'])
    constituencies = set(df['Parliamentary Constituency'])
    print( f"[INFO ] Total {len(constituencies)} constituencies." )
    slices = []
    for constituency in constituencies:
        d = df[df['Parliamentary Constituency'] == constituency]
        d = d.sort_values(by='Total Votes Polled', ascending=False)
        totalVotes = sum(d['Total Votes Polled'])
        d['%Votes'] = 100 * d['Total Votes Polled'].values / totalVotes
        d['Rank'] = range(1, len(d)+1)
        slices.append(d)
    df = pandas.concat(slices)
    return df

def process(df):
    plt.figure(figsize=(11,7))
    ax1 = plt.subplot(2,2,1)
    rank1 = df[df['Rank'] == 1]
    rank2 = df[df['Rank'] == 2]
    rank3 = df[df['Rank'] == 3]
    ax1.plot(rank1['%Votes'].values, 'o', alpha=0.5, label = 'Winner')
    ax1.plot(rank2['%Votes'].values, 'o', alpha=0.5, label = '1st Loser')
    ax1.plot(rank3['%Votes'].values, '*', color='black', alpha=0.5, label = '2nd Loser')
    ax1.legend()
    ax1.set_ylabel( '% Votes')
    ax1.set_xlabel( 'Constituency')

    ax2 = plt.subplot(2,2,2)
    ax2.set_xlabel('%Votes')
    ax2.hist(rank1['%Votes'].values, range=(0,100), bins=20, histtype='step'
            , density=True
            , lw=2, label ='Winner')
    ax2.hist(rank2['%Votes'].values, range=(0,100), bins=20, histtype='step'
            , density=True
            , lw=2, label ='1st Loser')
    ax2.hist(rank3['%Votes'].values, range=(0,100), bins=20, histtype='step'
            , density = True
            , lw=2, label ='2nd Loser')
    ax2.legend()

    ax3 = plt.subplot(2,2,3)
    ax3.set_xlabel('%Votes')
    ax3.hist(rank1['%Votes'].values, range=(0,100), bins=20, histtype='step'
            , density=True
            , lw=2, label ='Winner')
    ax3.hist(rank2['%Votes'].values + rank3['%Votes'].values
            , range=(0,100), bins=20, histtype='step'
            , density=True
            , lw=2, label ='1st+2nd Loser')
    ax3.legend()
    plt.tight_layout(rect=(0,0,1,0.95))

def main():
    filename = sys.argv[1]
    df = read_data(filename)
    process(df)
    plt.savefig(f"{filename}.png")
    plt.show()
    plt.close()

if __name__ == '__main__':
    main()
