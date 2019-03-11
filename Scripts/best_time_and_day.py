import pandas as pd
from collections import Counter

def main():
    df = pd.read_table( '../data/ncbs_2019_responses.csv', sep='\t')
    cols = df.columns
    novice = df[df[cols[1]].str.contains( 'new to me') ]
    days = novice['Preferred days? (pick two)']
    days = [x.strip() for x in ','.join(days).split(',')]
    times = novice['Preferred time? (1.5 hour)']
    times = [x.strip() for x in ','.join(times).split(',')]
    cDays = Counter(days)
    cTimes = Counter(times)
    print(cDays)
    print(cTimes)

if __name__ == '__main__':
    main()
