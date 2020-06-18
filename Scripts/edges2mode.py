import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName', nargs = 1, type = str, \
                    help = "The filename of the input `combined__.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `__edges2mode.csv` file.")
args = parser.parse_args()


# Read `combinedLPs.csv` to a DataFrame:
combined_typeA_df = pd.read_csv('{}.csv'.format(args.inputFileName[0]))

# Initialise `typeAedges2mode_df` as an empty DataFrame,
typeAedges2mode_df = pd.DataFrame()

# Add the columns 'Limited Partner Type' and 'Commitment'
# from `combined_typeA_df` to `typeAedges2mode_df`:
typeAedges2mode_df = \
    typeAedges2mode_df.assign(**{c: combined_typeA_df[c].to_numpy() \
                            for c in ('label', 'Commitment')})
typeAedges2mode_df.rename( \
                columns = {'label':'From', 'Commitment':'To'}, \
                inplace = True)

# Save the .csv file (note that file name has to be an absolute path):
typeAedges2mode_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
