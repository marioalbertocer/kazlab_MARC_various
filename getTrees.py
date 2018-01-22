'''
This little script search a taxon trees and copy the trees that contain the taxon.

- Create a folder
- place this scrit in the folder
- run script and follow the steps 
'''

import os

# Asking the path to trees and taxa to search
treeFolder = raw_input("Drag folder with trees: ").rstrip()
searchTerm = raw_input('Seach this taxa in trees: ').rstrip()

# Process every tree in the folder
for tree in os.listdir(treeFolder):
	treeLine = open(treeFolder + '/' + tree).readline() # This line contain the tree in newick format

	find = 'no'  # declare decision tree does not have the taxon (until it find it)
	if treeLine: # if you actually have a tree
		taxa = treeLine.split(",") # break newick tree by leaves
		for taxon in taxa: # loop trough the taxa
			if taxon : taxon = (taxon.split(":")[0]).replace("(", "") # next two lines clean the leaf to contain only taxon name
			if "_" in taxon : taxon = taxon.split("_")[0] + "_" + taxon.split("_")[1] + "_" + taxon.split("_")[2]
			if searchTerm in taxon : find = 'yes' # if you find the taxon in the tree, then decision is 'yes'

		print tree + " has taxon? : " + find
		if find == 'yes': # if you find the taxon in the tree
			os.system("cp " + treeFolder + "/" + tree + " ./") # copy the tree from the folder to your current folder.
	