import os
import glob
import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('indir', nargs = 1, type = pathlib.Path, \
                    help = "Input directory of rawLPs .csv files.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output .csv file.")
args = parser.parse_args()

# Check if the paths exist. If it doesn't, the script exits:
assert args.indir[0].exists(), "Input directory does not exist."

# Changes directory to the specified path:
os.chdir(args.indir[0])

# Specify the desired file extension
# and return list of all filenames with that extension:
extension = 'csv'
all_raw_typeB_filenames = sorted([i for i in glob.glob('*.{}'.format(extension))])

# Define `combined_df` as the master dataframe:
combined_typeA_df = pd.DataFrame()

# Iterate and read each rawLPs .csv file,
# add 'Commitment' as the last column,
# then concatenate `rawLPs_df` with the master `combinedLPs_df` in each iteration:
for f in all_raw_typeB_filenames:
    raw_typeB_df = pd.read_csv(f)
    raw_typeB_df['Commitment'] = f.split('.csv')[0]
    combined_typeA_df = pd.concat([combined_typeA_df, raw_typeB_df], ignore_index = True)

# Save the .csv file (note that file name has to be an absolute path):
combined_typeA_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
