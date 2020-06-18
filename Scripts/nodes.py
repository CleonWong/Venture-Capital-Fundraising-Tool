import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName', nargs = 1, type = str, \
                    help = "The filename of the input .csv file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output .csv file.")
args = parser.parse_args()

# Read `combinedLPs.csv` to a DataFrame:
combined_typeA_df = pd.read_csv('{}.csv'.format(args.inputFileName[0]))

typeAnodes_df = combined_typeA_df.drop(['Commitment'], axis = 1)

# Get a list of columns:
cols = list(typeAnodes_df)

# Loop and remove spaces from column names:
for col in cols:
    col_nospace = col.replace(" ", "")
    typeAnodes_df.rename(columns = {col:col_nospace}, inplace = True)

# Get list of new columns:
desiredColumnOrder = list(typeAnodes_df)

# Loop through the 4 important columns to get the desired column order:
i = 0
for col in ['label', 'type', 'country']:
    desiredColumnOrder.insert(i, desiredColumnOrder.pop(desiredColumnOrder.index(col)))
    i += 1

# Rearrange the order of the columns in typeAnodes_df:
typeAnodes_df = typeAnodes_df.reindex(columns = desiredColumnOrder)

# Remove duplicate instances under the 'label' column:
typeAnodes_df.drop_duplicates(subset = ['label'], keep = 'first', inplace = True)

# Save the .csv file (note that file name has to be an absolute path):
typeAnodes_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
