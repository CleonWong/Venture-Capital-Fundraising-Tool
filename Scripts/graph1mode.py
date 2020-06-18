import networkx as net
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pathlib
import argparse
# For colourmapping:
import matplotlib.cm as cmx
import matplotlib.colors as colors

# Take in arguments from the Command Line:
parser = argparse.ArgumentParser(description = "Input and output directories.")
parser.add_argument('inputFileName1', nargs = 1, type = str, \
                    help = "The filename of the input `__edges1mode.csv`.")
parser.add_argument('inputFileName2', nargs = 1, type = str, \
                    help = "The filename of the input `__nodesTagged.csv`.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output graph.")
args = parser.parse_args()


# Read `__edges1mode.csv` and `__nodesTagged.csv` to DataFrames:
edges1mode_df = pd.read_csv('{}.csv'.format(args.inputFileName1[0]))
nodesTagged_df = pd.read_csv('{}.csv'.format(args.inputFileName2[0]))

# Extract location info from `nodesTagged_df` into a dict of {node:location}:
locAttribute = dict()
for row in nodesTagged_df.itertuples():
    locAttribute[row.label] = row.location

# Create a list that contains all edges,
# where each edge is a tuple of the format (LP,VC):
edges1mode_list = [(row.From, row.To) for row in edges1mode_df.itertuples()]

# Create a list that contains all nodes from `nodesTagged_df`:
nodesTagged_list = [row.label for row in nodesTagged_df.itertuples()]

# Create the network graph object:
graph1mode = net.Graph()
graph1mode.add_edges_from(edges1mode_list)
graph1mode.add_nodes_from(nodesTagged_list) # Note: adding nodes manually will
# add the nodes that are not in the edge list (i.e. nodes that have no links to
# any other nodes in the graph).
net.set_node_attributes(graph1mode, locAttribute, 'location')

# Create node fill colours based on location:
uniqueLoc_temp = nodesTagged_df['location'].unique()
uniqueLoc = dict(zip(uniqueLoc_temp, [i for i in range(len(uniqueLoc_temp))]))
node_fillcolours = [uniqueLoc[graph1mode.nodes[n]['location']] for n in nodesTagged_list]

# Color mapping:
cmap = plt.cm.rainbow # Define the colormap.
cmaplist = [cmap(i) for i in range(cmap.N)] # Extract all colors the cmap into a list of rgb colours.
cmapHexList = [mpl.colors.rgb2hex(rgb) for rgb in cmaplist] # Convert rgb to hexcode.
bounds = np.linspace(start = 0, stop = cmap.N - 1, num = len(uniqueLoc_temp), dtype = int)
cmapHexListToUse = [cmapHexList[i] for i in bounds]

# Plotting the graph:
fig = plt.figure(constrained_layout = True, figsize = (12, 12))
fig.suptitle("Network Graph (1-mode)", weight = 'bold', y = 0.98)
ax = fig.add_subplot(1,1,1)

pos = net.spring_layout(graph1mode, k = 0.20, iterations = 25)

i = 0
for location in uniqueLoc_temp:
    nodelist = []
    for node, data in graph1mode.nodes.data('location'):
        if data == location:
            nodelist.append(node)
    net.draw_networkx_nodes(graph1mode, pos = pos, ax = ax, nodelist = nodelist, node_color = cmapHexListToUse[i], node_size = 60, linewidths = 1, edgecolors = 'k', label = location)
    i += 1

net.draw_networkx_edges(graph1mode, pos = pos, ax = ax, width = 0.5, edge_color = 'k')
ax.legend(loc = 'lower right', edgecolor = '#000000', scatterpoints = 1, \
            fontsize = 10, frameon = True)


# Save the graphs in .jpg and .svg formats
# (note that file names have to be absolute paths):
plt.axis('off')
plt.savefig(fname = '{}.png'.format(args.outputFileName[0]), dpi = 600, \
            format = 'png', transparent = False)
plt.savefig(fname = '{}.svg'.format(args.outputFileName[0]), dpi = 600, \
            format = 'svg', transparent = True)
