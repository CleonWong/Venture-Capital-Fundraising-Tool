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
                    help = "The filename of the input `__edges1mode.csv` file.")
parser.add_argument('inputFileName2', nargs = 1, type = str, \
                    help = "The filename of the input `__nodes.csv` file.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output `__nodesCentrality1mode.csv` file.")
args = parser.parse_args()

# Read `LPedges1mode.csv` to a DataFrame:
typeAedges1mode_df = pd.read_csv('{}.csv'.format(args.inputFileName1[0]))

# Create a master list that contains all edges,
# where each edge is a tuple of the format (LP,VC):
allEdges = [(row.From, row.To) for row in typeAedges1mode_df.itertuples()]

# Create the network graph object:
graph1mode = net.Graph()
graph1mode.add_edges_from(allEdges)

# Compute the various centralities, return a dictionary of {node:Xcentrality}:
degCentrality = net.degree(graph1mode)
eigCentrality = net.eigenvector_centrality(graph1mode)
reachCentrality = dict([(n, net.local_reaching_centrality(graph1mode, n)) \
                        for n in graph1mode.nodes()])

# Read 'LPnodes.csv` to a DataFrame:
typeAnodesCentrality1mode_df = pd.read_csv('{}.csv'.format(args.inputFileName2[0]))

# Add 3 new columns for the 3 centralities, mapping from their respective dicts:
typeAnodesCentrality1mode_df['degree'] = \
    typeAnodesCentrality1mode_df['label'].map(degCentrality, na_action = 'ignore')
typeAnodesCentrality1mode_df['eigenvector'] = \
    typeAnodesCentrality1mode_df['label'].map(eigCentrality, na_action = 'ignore')
typeAnodesCentrality1mode_df['reach'] = \
    typeAnodesCentrality1mode_df['label'].map(reachCentrality, na_action = 'ignore')

# Iterate through every row in `typeAnodesCentrality1mode_df`,
# if the cell in the `eigenvector` column is NaN,
# replace the cell in `degree` column with NaN
for i in typeAnodesCentrality1mode_df.index:
    if pd.isnull(typeAnodesCentrality1mode_df.loc[i, 'eigenvector']):
        typeAnodesCentrality1mode_df.loc[i, 'degree'] = np.nan

# Normalise degree centrality by dividing each centrality measure by the largest
# degree centrality:
maxDegCen = typeAnodesCentrality1mode_df['degree'].max()
maxEigCen = typeAnodesCentrality1mode_df['eigenvector'].max()
maxReachCen = typeAnodesCentrality1mode_df['reach'].max()
typeAnodesCentrality1mode_df.loc[:, 'degree'] *= (1 / maxDegCen)
typeAnodesCentrality1mode_df.loc[:, 'eigenvector'] *= (1 / maxEigCen)
typeAnodesCentrality1mode_df.loc[:, 'reach'] *= (1 / maxReachCen)

# Save the .csv file (note that file name has to be an absolute path):
typeAnodesCentrality1mode_df.to_csv("{}.csv".format(args.outputFileName[0]), index = False)
