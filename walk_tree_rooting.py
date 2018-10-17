import dendropy
from p4 import *
import os, re
import csv
var.doRepairDupedTaxonNames = 1

path = '/home/mario/walk_tree/' 				# This is the folder that is the parent
												# of the the folder in which you have your trees
path2 = '/Users/marioceron/Documents/katzlab/duplications/reconciliation/051418_dupli/' 			# This is the actual folder where you have the trees
path3 = '/Users/marioceron/Documents/katzlab/duplications/reconciliation/051418_dupli_rooted/'

def get_clades(taxon):								# Get different forms of the taxa/clade identifier
	major = taxon.split('_')[0]   					# The identifier as major clade (e.g., Am, Ex)
	minor = taxon.split('_')[1]	  					# The identifier as minor clade (e.g., di, eu)
	sp = taxon.split('_')[2]						# The identifier as 'species' (eg., Acas, Bsal)
	clade_name = major + '_' + minor 				# The identifier as Major_minor (eg., Am_di, Ex_eu)
	taxon_name = major + '_' + minor + '_' + sp 	# The identifier as Major_minor_sp (eg., Am_di_Acas) 
	return (major, minor, sp, clade_name, taxon_name)

def correct_tree(t): 								# Some trees have '-', which causes problems in p4.
	tree2correct = open ('%s%s' % (path2, t), 'r')	# Open the file 't' and takes the information
	tree2correct = tree2correct.readline()			# Reads the info as tree for python 
	tree_corrected = open ('%stemporal_%s' % (path2, t), 'w')
													# The line above creates a new file that will contain ...
													# ... the corrected tree. This is a TEMPORAL file
	if '-' in tree2correct:							# If the tree has '-', delete it
		tree2correct = re.sub('-', '', tree2correct) 
	
	tree_corrected.write(tree2correct)				# Write the corrected tree in the temporal file 
	tree_corrected.close()							# Finish the writing. 

n = 0	# This counter should be initizalize in 0.
		# This is going to show you how many trees have been analyzed
		 
for t in os.listdir('%s' % path2):		# Take each file in the folder that have the trees
	t = t.strip('\n')					# Delete the 'new_line' character.
										# This is important, otherwise it will not match in next steps
	if 'OG5' in t:						# Consider only the files that contain the word 'OG5'.
										# This means that we are ignoring the hidden files
		n = n+1							# Each time that you take a file with a tree. This counter add 1...
		print "%s\t%s" % (n,t)  		# ... and shows you in the terminal.
										# In this way you can track how many trees have been analyzed
		
		var.trees = []								# Here we are initializing the variable (for p4)...
													# ... that contains the tree
		correct_tree(t)								# Correcting the format of the tree, using the function...
													# correct_tree. Read the coments of "def correct_tree(t):"
		tree_file = '%stemporal_%s' % (path2, t)	# Reading the CORRECTED file and taking the tree for python
		read(tree_file) 							# Reading the tree for p4 
		tree = var.trees[0] 						# The tree	itself in var 'tree' - going forward using p4
													# As the tree is now in 'tree', remove the temporal file
		os.remove('%stemporal_%s' % (path2, t))		# After putting , remove that file
		
#		error_tree = ''	

		OG5 = t.split('.')[1].replace('_postguidance', '')				# Take the OG code from the file that contains the tree

		sizes_cladesBaZa = {}			
		sizes_cladesOp = {}				
		sizes_cladesPl = {}				
		sizes_cladesAm = {}				
		sizes_cladesEx = {}				
		sizes_cladesSr = {}				
		
		for node in tree.iterNodes():					# For each node in the tree
			allTaxa_node = tree.getAllLeafNames(node)	# Get all taxa from leaves per node...
														# ... and make a list.
				
			MC_list =[]								
			for taxon in allTaxa_node:					# Take each taxon from the list above 
				MC_list.append(get_clades(taxon)[0])	# and get the major clade using 'get_clades'
														# it will end up with ...
														# list of MC of the taxa of each node
														# The list above will be in MC_list.
					
			# In the next bunch of lines, the script determines if MC_list contains only Ba/za,
			# Op, Pl, Am, Ex or Sr. This means that the script search the nodes that only
			# contains an specific MC. Finally, the script appends the nodes of the clades 
			# and their sizes in the hashes. Also, the script allows one contaminant. For instance,
			# A clade with 9 Op leaves and 1 Pl leaf will be recorder as node_XXXXX -> 10.
			# This step is very important for the rooting.
					
			if MC_list.count('Ba') + MC_list.count('Za') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesBaZa[tree.node(node)] = len(allTaxa_node)	
			if MC_list.count('Op') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesOp[tree.node(node)] = len(allTaxa_node)
			if MC_list.count('Pl') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesPl[tree.node(node)] = len(allTaxa_node)
			if MC_list.count('Am') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesAm[tree.node(node)] = len(allTaxa_node)
			if MC_list.count('Ex') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesEx[tree.node(node)] = len(allTaxa_node)
			if MC_list.count('Sr') == (len(MC_list) or len(MC_list)-1):
				sizes_cladesSr[tree.node(node)] = len(allTaxa_node)
				
			# In the next bunch of lines the tree is re-rooted by the biggest Ba/Za clade, or
			# the biggest Op clade, or the biggest Pl clade, or the biggest Am clade, or the
			# biggest Am clade, or the biggest Ex clade, or the biggest Ex clade.
			# In theory, only the first three options should occur. If the rooting fails,
			# print error tree in the terminal.
				
		if sizes_cladesBaZa: 		# If size_cladesBaZa is not 0
									# Take the node with the biggest number of taxa (leaves)
									# Re-root by this node
									
			biggestBaZa = max(sizes_cladesBaZa, key=sizes_cladesBaZa.get) 
			tree.reRoot(biggestBaZa)
		else:
			if sizes_cladesOp:
				biggestOp = max(sizes_cladesOp, key=sizes_cladesOp.get)
				tree.reRoot(biggestOp)
			else:
				if sizes_cladesPl:
					biggestPl = max(sizes_cladesPl, key=sizes_cladesPl.get)
					tree.reRoot(biggestPl)
				else:
					if sizes_cladesAm:
						biggestAm = max(sizes_cladesAm, key=sizes_cladesAm.get)
						tree.reRoot(biggestAm)
					else:
						if sizes_cladesEx:
							biggestEx = max(sizes_cladesEx, key=sizes_cladesEx.get)
							tree.reRoot(biggestEx)
						else:
							if sizes_cladesSr:
								biggestSr = max(sizes_cladesSr, key=sizes_cladesSr.get)
								tree.reRoot(biggestSr)
							else:
								error_tree = 'error tree'
		
		# The next loop iterates by the nodes of the tree
		# considering leaves as well as nodes
					
#	tree.write('%s%s' % (path3, t))
		
#		here = '%s%s' % (path3, t)
#		print t
#		out = tree.write()

		tree.writePhylip('%s%s' % (path3, t))
		