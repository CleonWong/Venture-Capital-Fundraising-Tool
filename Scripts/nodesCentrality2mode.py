import networkx as net
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pathlib
import argparse

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName1', nargs = 1, type = str, \
                    help = "The filename of the input `__edges2mode.csv` file.")
parser.add_argument('inputFileName2', nargs = 1, type = str, \
                    help = "The filename of the input `__nodes.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `__nodesCentrality2mode.csv` file.")
args = parser.parse_args()


# Read `LPedges2mode.csv` to a DataFrame:
typeAedges2mode_df = pd.read_csv('{}.csv'.format(args.inputFileName1[0]))

# Create a master list that contains all edges,
# where each edge is a tuple of the format (LP,VC):
allEdges = [(row.From, row.To) for row in typeAedges2mode_df.itertuples()]

# Create the network graph object:
graph2mode = net.Graph()
graph2mode.add_edges_from(allEdges)

# Compute the various centralities, return a dictionary of {node:Xcentrality}:
degCentrality = net.degree(graph2mode)
eigCentrality = net.eigenvector_centrality(graph2mode)
reachCentrality = dict([(n, net.local_reaching_centrality(graph2mode, n)) \
                        for n in graph2mode.nodes()])

# Read 'LPnodes.csv` to a DataFrame:
typeAnodesCentrality2mode_df = pd.read_csv('{}.csv'.format(args.inputFileName2[0]))

# Add 3 new columns for the 3 centralities, mapping from their respective dicts:
typeAnodesCentrality2mode_df['degree'] = \
    typeAnodesCentrality2mode_df['label'].map(degCentrality)
typeAnodesCentrality2mode_df['eigenvector'] = \
    typeAnodesCentrality2mode_df['label'].map(eigCentrality)
typeAnodesCentrality2mode_df['reach'] = \
    typeAnodesCentrality2mode_df['label'].map(reachCentrality)

# Iterate through every row in `LPnodesCentrality1mode_df`,
# if the cell in the `eigenvector` column is NaN,
# replace the cell in `degree` column with NaN
for i in typeAnodesCentrality2mode_df.index:
    if pd.isnull(typeAnodesCentrality2mode_df.loc[i, 'eigenvector']):
        typeAnodesCentrality2mode_df.loc[i, 'degree'] = np.nan

# Normalise each centrality measure by dividing by the largest value of the
# respective centrality:
maxDegCen = typeAnodesCentrality2mode_df['degree'].max()
maxEigCen = typeAnodesCentrality2mode_df['eigenvector'].max()
maxReachCen = typeAnodesCentrality2mode_df['reach'].max()
typeAnodesCentrality2mode_df.loc[:, 'degree'] *= (1 / maxDegCen)
typeAnodesCentrality2mode_df.loc[:, 'eigenvector'] *= (1 / maxEigCen)
typeAnodesCentrality2mode_df.loc[:, 'reach'] *= (1 / maxReachCen)

# Save the .csv file (note that file name has to be an absolute path):
typeAnodesCentrality2mode_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
