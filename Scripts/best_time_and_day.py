import pandas as pd

def main():
    df = pd.read_table( '../data/ncbs_2019_responses.csv', sep=','
            , quotechar='"')
    print(df)

if __name__ == '__main__':
    main()
