import pandas as pd
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName', nargs = 1, type = str, \
                    help = "The filename of the input `__edges2mode.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `__edges1mode.csv` file.")
args = parser.parse_args()


# Read `LPedges2mode.csv` to a DataFrame:
typeAedges2mode_df = pd.read_csv('{}.csv'.format(args.inputFileName[0]))

# Create a master list that contains all edges,
# where each edge is a tuple of the format (typeA_node,typeB_node):
allEdges = [(row.From, row.To) for row in typeAedges2mode_df.itertuples()]

# Create empty dictionary to populate with 1-mode edges and weights.
# Format is {'(typeA_1_node, type_2_node)' : weight}:
typeAedges1mode_dict = {}

# For every ith edge in master list `allEdges`, iterate through all subsequent
# (i+1)th to nth edges  and append to `typeAedges1mode_list` if they
# share the same VC:
for edge in allEdges:
    for j in range(allEdges.index(edge) + 1, len(allEdges)):
        if edge[1] == allEdges[j][1]:
            # Check for duplicates. Note, (A,B) and (B,A) are also duplicates:
            if not ((edge[0], allEdges[j][0]) in typeAedges1mode_dict) \
                or not ((allEdges[j][0], edge[0]) in typeAedges1mode_dict):
                typeAedges1mode_dict[(edge[0], allEdges[j][0])] = 1
            else:
                typeAedges1mode_dict[(edge[0], allEdges[j][0])] += 1

# Convert dictionary {'(LP1, LP2)' : weight}
# into list of tuples [(LP1, LP2, weight)]:
typeAedges1mode_list = [(k[0], k[1], v) for k,v in typeAedges1mode_dict.items()]

typeAedges1mode_df = pd.DataFrame(typeAedges1mode_list, columns = ['From', 'To', \
                                                                'Weight'])

# Save the .csv file (note that file name has to be an absolute path):
typeAedges1mode_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
