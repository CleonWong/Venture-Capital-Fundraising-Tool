import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName', nargs = 1, type = str, \
                    help = "The filename of the input `__nodesCentrality2mode.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `target__2mode.csv` file.")
args = parser.parse_args()


# Read `LPedges2mode.csv` to a DataFrame:
typeAnodesCentrality2mode_df = pd.read_csv('{}.csv'.format(args.inputFileName[0]))

# Weights for degree, eigenvector and reach metrics.
# Note that the weight should sum to 1:
w1 = 1/3
w2 = 1/3
w3 = 1/3

typeAnodesCentrality2mode_df['weightedSum'] = \
      (w1 * typeAnodesCentrality2mode_df.degree) \
    + (w2 * typeAnodesCentrality2mode_df.eigenvector) \
    + (w3 * typeAnodesCentrality2mode_df.reach)

# For clarity:
targetTypeA_2mode_df = typeAnodesCentrality2mode_df

# Sort `targetTypeA_2mode_df` based on `weightedSum` column in descending order:
targetTypeA_2mode_df.sort_values('weightedSum', inplace = True, ascending = False)

# Save the .csv file (note that file name has to be an absolute path):
targetTypeA_2mode_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
