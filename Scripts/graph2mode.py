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
                    help = "The filename of the input `__edges2mode.csv`.")
parser.add_argument('inputFileName2', nargs = 1, type = str, \
                    help = "The filename of the input `__nodesTagged.csv`.")
parser.add_argument('outputFileName', nargs = 1, type = str, \
                    help = "The filename of the output graph.")
parser.add_argument('typeBnode', nargs = 1, type = str, \
                    help = "Type-B node in the network.")

args = parser.parse_args()


# Read `__edges2mode.csv` and `__nodesTagged.csv` to DataFrames:
edges2mode_df = pd.read_csv('{}.csv'.format(args.inputFileName1[0]))
typeAnodesTagged_df = pd.read_csv('{}.csv'.format(args.inputFileName2[0]))

# Extract location info from `nodesTagged_df` into a dict of {node:location}:
locAttribute = dict()
for row in typeAnodesTagged_df.itertuples():
    locAttribute[row.label] = row.location

# Create a list that contains all edges,
# where each edge is a tuple of the format (LP,VC):
edges2mode_list = [(row.From, row.To) for row in edges2mode_df.itertuples()]

# Create a list that contains all nodes from `nodesTagged_df`:
typeAnodesTagged_list = [row.label for row in typeAnodesTagged_df.itertuples()]

# Create the network graph object:
graph2mode = net.Graph()
graph2mode.add_edges_from(edges2mode_list)
graph2mode.add_nodes_from(typeAnodesTagged_list) # Note: adding nodes manually will
# add the nodes that are not in the edge list (i.e. nodes that have no links to
# any other nodes in the graph).
net.set_node_attributes(graph2mode, locAttribute, 'location')

# Create node fill colours based on location:
uniqueLoc_temp = typeAnodesTagged_df['location'].unique()
uniqueLoc = dict(zip(uniqueLoc_temp, [i for i in range(len(uniqueLoc_temp))]))
node_fillcolours = [uniqueLoc[graph2mode.nodes[n]['location']] for n in typeAnodesTagged_list]

# Color mapping:
cmap = plt.cm.rainbow # Define the colormap.
cmaplist = [cmap(i) for i in range(cmap.N)] # Extract all colors the cmap into a list of rgb colours.
cmapHexList = [mpl.colors.rgb2hex(rgb) for rgb in cmaplist] # Convert rgb to hexcode.
bounds = np.linspace(start = 0, stop = cmap.N - 1, num = len(uniqueLoc_temp), dtype = int)
cmapHexListToUse = [cmapHexList[i] for i in bounds]

# Plotting the graph:
fig = plt.figure(constrained_layout = True, figsize = (12, 12))
fig.suptitle("Network Graph (2-mode)", weight = 'bold', y = 0.98)
ax = fig.add_subplot(1,1,1)

pos = net.spring_layout(graph2mode, k = 0.07, iterations = 25)

# To plot the typeA-nodes:
i = 0
for location in uniqueLoc_temp:
    typeAnodelist = []
    for node, data in graph2mode.nodes.data('location'):
        if data == location:
            typeAnodelist.append(node)
    net.draw_networkx_nodes(graph2mode, pos = pos, ax = ax, nodelist = typeAnodelist, node_color = cmapHexListToUse[i], node_size = 35, linewidths = 0.3, edgecolors = 'k', label = location)
    i += 1

# To plot the typeB-nodes:
typeBnodelist = [node for node in graph2mode.nodes() if not node in typeAnodesTagged_list]
net.draw_networkx_nodes(graph2mode, pos = pos, ax = ax, nodelist = typeBnodelist, node_color = '#ffffff', node_size = 30, linewidths = 0.3, edgecolors = 'k', node_shape = 's', label = '{}'.format(args.typeBnode[0]))

# To plot edges:
net.draw_networkx_edges(graph2mode, pos = pos, ax = ax, width = 0.1, edge_color = 'k')

# To plot legend:
ax.legend(loc = 'lower right', edgecolor = '#000000', scatterpoints = 1, \
            fontsize = 10, frameon = True)


# Save the graphs in .jpg and .svg formats
# (note that file names have to be absolute paths):
plt.axis('off')
plt.savefig(fname = '{}.png'.format(args.outputFileName[0]), dpi = 600, \
            format = 'png', transparent = False)
plt.savefig(fname = '{}.svg'.format(args.outputFileName[0]), dpi = 600, \
            format = 'svg', transparent = True)
