import dendropy
from p4 import *
import os, re
import csv
var.doRepairDupedTaxonNames = 1

path = '/home/mario/walk_tree/' 				# This is the folder that is the parent
												# of the the folder in which you have your trees
path2 = '/home/mario/walk_tree/treesYY/' 			# This is the actual folder where you have the trees
report = open (path + 'report_walk_contamination.txt', 'w')	# Here is the output

# In the next line you should list the weird taxa
#weirdtaxalist = ["Sr_ci_Ahae", "Sr_ci_Ansp", "Sr_ci_Bame", "Sr_ci_Bjap", "Sr_ci_Brsp", "Sr_ci_Btru", "Sr_ci_Camp", "Sr_ci_Cirr", "Sr_ci_Clim", "Sr_ci_Cmag", "Sr_ci_Cpsp", "Sr_ci_Cunc", "Sr_ci_Cxsp", "Sr_ci_Dmuc", "Sr_ci_Dnas", "Sr_ci_Drum", "Sr_ci_Ecau", "Sr_ci_Ecra", "Sr_ci_Eeca", "Sr_ci_Efoc", "Sr_ci_Ehar", "Sr_ci_Emag", "Sr_ci_Fehr", "Sr_ci_Fron", "Sr_ci_Ftar", "Sr_ci_Glsp", "Sr_ci_Imul", "Sr_ci_Ipro", "Sr_ci_Knsp", "Sr_ci_Lemb", "Sr_ci_Lito", "Sr_ci_Lxsp", "Sr_ci_Mavi", "Sr_ci_Meto", "Sr_ci_Mpul", "Sr_ci_Nosp", "Sr_ci_Nova", "Sr_ci_Otri", "Sr_ci_Padh", "Sr_ci_Pmul", "Sr_ci_Posp", "Sr_ci_Pper", "Sr_ci_Pros", "Sr_ci_Pspe", "Sr_ci_Pssp", "Sr_ci_Ptet", "Sr_ci_Rmsp", "Sr_ci_Samb", "Sr_ci_Sasu", "Sr_ci_Scer", "Sr_ci_Sinc", "Sr_ci_Slem", "Sr_ci_Smin", "Sr_ci_Sond", "Sr_ci_Spat", "Sr_ci_Sras", "Sr_ci_Sroe", "Sr_ci_Sspp", "Sr_ci_Tcsp", "Sr_ci_tthe", "Sr_ci_Vort", "Sr_ci_Zssp"]
#weirdtaxalist = ["Sr_rh_Aelo", "Sr_rh_Amsp", "Sr_rh_Asco", "Sr_rh_Aspa", "Sr_rh_Assp", "Sr_rh_Astr", "Sr_rh_Blon", "Sr_rh_Bmar", "Sr_rh_Bmot", "Sr_rh_Bnat", "Sr_rh_Briz", "Sr_rh_Cdel", "Sr_rh_Cerc", "Sr_rh_Cgra", "Sr_rh_Crep", "Sr_rh_Cssp", "Sr_rh_Cten", "Sr_rh_Cysp", "Sr_rh_Emar", "Sr_rh_Erot", "Sr_rh_Eusp", "Sr_rh_Gcom", "Sr_rh_Gspa", "Sr_rh_Lamo", "Sr_rh_Loce", "Sr_rh_Lvor", "Sr_rh_Mchi", "Sr_rh_Misp", "Sr_rh_Mmac", "Sr_rh_Nsph", "Sr_rh_Nsps", "Sr_rh_Pbra", "Sr_rh_Pglo", "Sr_rh_Phyl", "Sr_rh_Pmar", "Sr_rh_Pmic", "Sr_rh_Pssp", "Sr_rh_Quin", "Sr_rh_Rfil", "Sr_rh_Spsu", "Sr_rh_Sspa", "Sr_rh_Trsp"]
#weirdtaxalist = ["Sr_rh_Cdel", "Sr_rh_Cssp", "Sr_rh_Cgra", "Sr_rh_Assp", "Sr_rh_Amsp", "Sr_rh_Cysp", "Sr_rh_Eusp", "Sr_rh_Misp", "Sr_rh_Pssp", "Sr_rh_Trsp"]
weirdtaxalist = ["Sr_st_psub", "Pl_gr_Pokl", "Pl_rh_cmer", "Op_me_mmul", "Sr_rh_mmac", "EE_ha_Pcrd", "Pl_gr_Pcol", "Sr_rh_Eusp", "Sr_ci_Sspp", "Pl_gr_Ptab", "Sr_rh_Pssp", "Op_me_isca", "Ex_eu_scul", "Sr_di_Nsci", "Pl_gr_Ntab", "Pl_gr_Cjap", "Op_me_Hech", "Sr_rh_Asco", "Pl_gr_Ptae", "Sr_st_Sbin", "Pl_rh_Hpul", "Sr_rh_Aelo", "Ex_eu_Dpap", "Sr_st_Trot", "Pl_rh_Furc", "Sr_rh_Cerc", "Sr_di_Lpol", "Pl_gr_Csti", "Am_ar_Mbal", "Sr_st_Mspa", "Sr_st_Croe", "Pl_gl_Gwit", "Sr_ch_Vbra", "Ex_is_Tpyr", "Pl_gr_Omed", "Sr_ci_Bjap", "Sr_ci_Sras", "Op_me_Avir", "Pl_gr_Tstr", "Pl_gr_Pokl", "Sr_ci_Bjap", "Sr_ci_Brsp", "Sr_ci_Clim", "Sr_ci_Cunc", "Sr_ci_Ecra", "Sr_ci_Efoc", "Sr_ci_Fehr", "Sr_ci_Ftar", "Sr_ci_Glsp", "Sr_ci_Knsp", "Sr_ci_Lemb", "Sr_ci_Lito", "Sr_ci_Lxsp", "Sr_ci_Meto", "Sr_ci_Mpul", "Sr_ci_Nosp", "Sr_ci_Padh", "Sr_ci_Posp", "Sr_ci_Pspe", "Sr_ci_Pssp", "Sr_ci_Rmsp", "Sr_ci_Sasu", "Sr_ci_Sinc", "Sr_ci_Smin", "Sr_ci_Spat", "Sr_ci_Sras", "Sr_ci_Sroe", "Sr_ci_Sspp", "Sr_ci_Vort", "Sr_ci_Zssp", "Sr_rh_Amsp", "Sr_rh_Eusp", "Sr_rh_Lvor", "Sr_rh_Misp", "Sr_rh_Sspa", "Sr_rh_Trsp"]

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
		# This is going to show you how many trees have been analized
		 
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
		
		taxon_names = tree.getAllLeafNames(0) 		# node 0 is the root, so this should list all taxon names
													# But, they will be like Sr_ap_pfal_PF110062_OG5_126572
													# You need a list of modified names like Sr_ap_pfal.
		taxon_names_mod = []						# This var accumulates the modified taxa names PER TREE
													# Then, you should initialize this var here.
				
		for taxon in taxon_names:							# Take each taxon name
			taxon_names_mod.append(get_clades(taxon)[4])	# Modify the name using function 'get_clades'
															# Read at the top what 'get_clades' does 
															# append the modified name in taxon_names_mod
		
		error_tree = ''	
		for taxa in weirdtaxalist:				# For each weird taxon ...
			OG5 = t.split('.')[1].replace('_postguidance', '')				# Take the OG code from the file that contains the tree
			if taxa in taxon_names_mod:			# If the weird taxon is in taxon_names_mod...
												# As taxon_names_mod contains all taxa in the tree...
												# This conditional means that the weird taxon is in the tree
												# Create hashes for Ba/Za, Op, Pl, Am, Ex and Sr.
												# sister taxa and their size are appended in the hashes
												# This info changes per node. Hashes should be initialized 
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
					
				for node in tree.iterNodes(): 				# but I really want to start with leaves!
					if node.getNChildren() == 0: 			# If node is a leaf...
						taxon_full = node.name					# Take the taxon that is in the leave 
						clade_name = get_clades(taxon_full)[4]	# Put taxon in the format MC_mc_sp
															# Ex: Sr_ap_pfal
															# save taxon in var clade_name
						taxa_interest = taxa				
						if taxa_interest in clade_name:		# If the leaf is the weird taxon...
															 	
							sisterTaxa = tree.getAllLeafNames(node.parent)	# Take all taxa that are in 
																			# the parental node of the leaf
																			# This list contains the weird
																			# taxon, and the sister taxa.
							for taxon in sisterTaxa:						
								if get_clades(taxon)[4] in taxa_interest:
									sisterTaxa.remove(taxon)				# Remove the weird taxon and
																			# end up only with the sister taxa.
							
#							sisterClades = []
							sisterMinors = []
							sisterSequences = ''								
							for taxon in sisterTaxa:						
#								sisterClades.append(get_clades(taxon)[0])	# Modify the sister taxa
																			# from MC_mc_sp to MC
																			# Ex: Sr_ap_pfal to Sr
								sisterMinors.append(get_clades(taxon)[3])
								sisterSequences = sisterSequences + ',' + taxon
							
							# The next two lines take the list of MC of the sister taxa and remove duplicates
							# Ex: if the list were: [Sr, Sr, Sr, Am], it will produce [Sr, Am].
							# The example above is a non-monophyletic sister clade that produces 2 elements.
							# A monophyletic sister clade produces only one element in the list.
							# Ex: [Sr, Sr, Sr], produces [Sr]
							# The new list w/o duplicates is saved in var sisterClades
							
#							sisterClades = set(sisterClades)	# 'set' makes an iterable but not-indexable object
#							sisterClades = list(sisterClades)	# 'list' makes it indixeble
							sisterMinors = set(sisterMinors)
							sisterMinors = list(sisterMinors)
							
							minors = ''
							for minor in sisterMinors:
								minors = minors + ',' + minor
								
							
							if len(sisterMinors) == 1:							# If sisterMinors is 1 element
								minorClade = sisterMinors[0]					# get its minor clade

								if minorClade in taxa_interest:					# If weird taxon also has this MC
									result = 'same_minor'							# return 'same_MC'
									report.write (OG5 + '\t' + taxa + '\t' + taxon_full + '\t' +  result + '\tNA' + '\n')	
								
								else:											# If weird taxon hasn't this MC 	
									result = minorClade							# return the MC
																				# report result in output
										
									report.write (OG5 + '\t' + taxa + '\t'+ taxon_full + '\t' +  result + '\t' + sisterSequences + '\n')	

							if len(sisterMinors) > 1:							# If sister clades has more than 1
								result = "non-monophyletic"						# retrieve 'non-monophyletic'
																				# report result in output
								
								report.write (OG5 + '\t' + taxa + '\t' + taxon_full + '\t' +  result + '\t'  + minors + '\n') 

#								for c in sisterClades:
#									result = "non-monophyletic_%s" % c
#									report1.write ('%s,%s\n' % (get_OG5(t), taxa))
#									report2.write ("%s,%s\n" % (taxa, result))

			else:
				result = 'no_taxaOFinterest' # If the tree does not have the weird taxon, return 'no_taxaOFinterest'
#				report.write (OG5 + ',' + taxa + ',' +  result + '\n') # report result in output

		if 'error tree' in error_tree: # if the tree couldn't be re-rooted, retrieve 'OG cannot be annalized' 
			print OG5 + ' cannot be annalized'
			error_tree = ''
		

report.close() 
