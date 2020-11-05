#!/usr/bin/env python3
# Written by: Hans Müller Paul
#                           NOTES:

import argparse             #pip install argparse if this library isn't already installed
from os import path
from glob import glob

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--folder', required=True, dest='f', 
                    help='[required] path to input folder containing files in CSV format'
                    )
parser.add_argument('-o', '--output', dest='o', default='processed_IRAhandle_master_data.csv',
                    help='path to output file, default = processed_IRAhandle_master_data.csv'
                    )
parser.add_argument('-p', '--preprocessed', action='store_true',
                    help='enabling this option assumes dataset only contains two columns'
                    )
parser.add_argument('-v', '--verbose', action='store_true',
                    help='initiates script running on verbose mode'
                    )

args = parser.parse_args()

def import_processed_data(input_file):
    from pandas import read_csv     #pip install pandas if this library isn't already installed
    with open(input_file, 'r') as f:
        if args.verbose:
            print(f'Dataset {input_file} successfully imported')
        tweet_df = read_csv(f, header = 0, low_memory=False)
        if args.verbose:
            print(f'Dataframe successfully generated')
    return tweet_df


def import_unprocessed_data(input_file):
    from pandas import read_csv     #pip install pandas if this library isn't already installed
    with open(input_file, 'r') as f:
        if args.verbose:
            print(f'Dataset {input_file} successfully imported')
        tweet_df = read_csv(f, header = 0, low_memory=False)
        if args.verbose:
            print(f'Dataframe successfully generated')
    remove_columns = ["external_author_id",
            "author",
            "region",
            "language",
            "publish_date",
            "harvested_date",
            "following",
            "followers",
            "updates",
            "post_type",
            "account_type",
            "retweet",
            "new_june_2018",
            "alt_external_id",
            "tweet_id",
            "article_url",
            "tco1_step1",
            "tco2_step1",
            "tco3_step1"]
    for column in remove_columns:
        del tweet_df[column]
    if args.verbose:
        print(f'{len(remove_columns)} columns successfully removed')
    return tweet_df


def mark_as_troll(master_data):
    if master_data['account_category'] == 'RightTroll' or master_data['account_category'] == 'LeftTroll':
        return 1
    else:
        return 0


def main():
    file_list = glob(args.f+'/IRAhandle_tweets_*.csv') #allows to batch-process all files on path folder
    if args.preprocessed:
        for filename in file_list:
            tweet_data = import_processed_data(filename)
            if args.verbose:
                print(f'detecting troll tweets, this may take a while')
            tweet_data['troll'] = tweet_data.apply(mark_as_troll,axis=1) #this function parallelizes for maximized efficiency
            ##Writes updated data to new file:
            if path.exists(args.o):
                tweet_data.to_csv(args.o, header=False, index=False, mode='a+')
                if args.verbose:
                    print(f'data appended exported as {args.o}')
            else:
                tweet_data.to_csv(args.o, index=False, mode='w')
                if args.verbose:
                    print(f'data successfully exported as {args.o}')

    else:
        for filename in file_list:
            tweet_data = import_unprocessed_data(filename)
            if args.verbose:
                print(f'detecting troll tweets, this may take a while')
            tweet_data['troll'] = tweet_data.apply(mark_as_troll,axis=1) #this function parallelizes for maximized efficiency
            ##Write updated data to new file:
            if path.exists(args.o):
                tweet_data.to_csv(args.o, header=False, index=False, mode='a+')
                if args.verbose:
                    print(f'data appended exported as {args.o}')
            else:
                tweet_data.to_csv(args.o, index=False, mode='w')
                if args.verbose:
                    print(f'data successfully exported as {args.o}')

    if args.verbose:
        print(f'''summary:
        {tweet_data.describe()}
        ''')

if __name__ == '__main__':
    main()

