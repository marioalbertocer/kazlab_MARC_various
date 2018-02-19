# Takes phylogenetic trees and list the sister clade of every taxon. 
# - When the sister clade if monophyletic, it reports the sister's taxa minor clade or 'same clade' if the sister taxa are the same than the compared taxon. 
# - If the sister clade is polyphyletic, it reports all minor clades of the sister taxa.
#
# Some chaneges were made to work with single cells:
# - In LKH data when sister has same first 8 digits in the name, it takes the whole clade and reports its sister. 
# - For all other taxa when the 10 digits codes is the same for the sister, it takes the whole clade and reports its sister.
# - Now it reports branch lengths


import dendropy
from p4 import *
import os, re
import csv
var.doRepairDupedTaxonNames = 1

path = '/Users/katzlab32/Desktop/sisterReporter/' 				# This is the folder that is the parent
												# of the the folder in which you have your trees
#path2 = '/Users/katzlab32/Desktop/contamination/contamination_alltaxa/' 			# This is the actual folder where you have the trees

path2 = 'Contamination_Foram_amoebae/'
report = open (path + 'report_walk_contamination_single_amoeba.txt', 'w')	# Here is the output

# In the next line you should list the weird taxa
weirdtaxalist = ["Am_ar_edis", "Am_ar_ehis", "Am_ar_einv", "Am_ar_Enut", "Am_ar_Mbal", "Am_di_Acas", "Am_di_Ahea", "Am_di_Cmit", "Am_di_Endo", "Am_di_Luap", "Am_di_Mspa", "Am_di_Naes", "Am_di_Odes", "Am_di_Patl", "Am_di_Pcat", "Am_di_Pess", "Am_di_Tric", "Am_di_Vexi", "Am_di_Vnsp", "Am_di_Vrob", "Am_di_Vsim", "Am_hi_Gfon", "Am_is_Fflu", "Am_is_Fnol", "Am_is_Fsin", "Am_is_Pmon", "Am_is_Sram", "Am_is_Sste", "Am_is_Vant", "Am_my_Asub", "Am_my_Ddac", "Am_my_ddis", "Am_my_Dpur", "Am_my_Ppal", "Am_my_Ppol", "Am_th_Tqua", "Am_tu_Hver", "Am_tu_Nabe", "Am_va_Clsp", "Am_va_Usch", "EE_ap_Ttra", "EE_br_Bant", "EE_br_Stet", "EE_ce_Acsp", "EE_ce_Chsp", "EE_ce_Reri", "EE_ce_Rhet", "EE_cr_Ccur", "EE_cr_Gcry", "EE_cr_Gpac", "EE_cr_Gspa", "EE_cr_Gspb", "EE_cr_Gthe", "EE_cr_Hand", "EE_cr_Hphi", "EE_cr_Htep", "EE_cr_Psul", "EE_cr_Rlen", "EE_cr_Rsal", "EE_cr_Undd", "EE_ha_Cbre", "EE_ha_Clep", "EE_ha_Cpol", "EE_ha_Crho", "EE_ha_Ehux", "EE_ha_Goce", "EE_ha_Igal", "EE_ha_Ispa", "EE_ha_Pant", "EE_ha_Pcar", "EE_ha_Pcrd", "EE_ha_Plut", "EE_ha_Ppar", "EE_ha_Pspa", "EE_ha_Saps", "EE_ha_Unid", "EE_is_Ctri", "EE_is_Pbil", "EE_is_Tglo", "EE_is_Tmar", "EE_is_Tsub", "EE_ka_Rtru", "Ex_eu_Bsal", "Ex_eu_Dpap", "Ex_eu_Egra", "Ex_eu_Egym", "Ex_eu_Elon", "Ex_eu_lbra", "Ex_eu_linf", "Ex_eu_lmaj", "Ex_eu_lmex", "Ex_eu_Lpyr", "Ex_eu_Ndes", "Ex_eu_Pemi", "Ex_eu_Pser", "Ex_eu_Scul", "Ex_eu_tbrg", "Ex_eu_tbru", "Ex_eu_tcon", "Ex_eu_tcru", "Ex_eu_tviv", "Ex_fo_glab", "Ex_fo_glae", "Ex_fo_glam", "Ex_fo_Sbar", "Ex_fo_Ssal", "Ex_fo_Svor", "Ex_he_Ngru", "Ex_he_Pcos", "Ex_he_Slip", "Ex_he_Smar", "Ex_is_Tpyr", "Ex_ja_Haro", "Ex_ja_Jbah", "Ex_ja_Jlib", "Ex_ja_Rame", "Ex_ja_Secu", "Ex_ma_Mcal", "Ex_ma_Mjak", "Ex_ox_Mono", "Ex_pa_Hmel", "Ex_pa_Phom", "Ex_pa_Tfoe", "Ex_pa_tvag", "Op_ch_mbre", "Op_ch_Mova", "Op_ch_Sros", "Op_fu_Aalg", "Op_fu_afum", "Op_fu_Aloc", "Op_fu_Amac", "Op_fu_anid", "Op_fu_aory", "Op_fu_Bden", "Op_fu_calb", "Op_fu_Ccor", "Op_fu_cgla", "Op_fu_cimm", "Op_fu_cneg", "Op_fu_cneo", "Op_fu_cpos", "Op_fu_dhan", "Op_fu_Dspa", "Op_fu_ebie", "Op_fu_ecun", "Op_fu_egos", "Op_fu_eint", "Op_fu_Gpro", "Op_fu_gzea", "Op_fu_klac", "Op_fu_lbic", "Op_fu_Lcor", "Op_fu_Mdap", "Op_fu_Mglo", "Op_fu_mgri", "Op_fu_Mmel", "Op_fu_Napi", "Op_fu_Ncer", "Op_fu_ncra", "Op_fu_Npar", "Op_fu_Npat", "Op_fu_pchr", "Op_fu_Pgra", "Op_fu_Pneu", "Op_fu_Pspa", "Op_fu_psti", "Op_fu_Rall", "Op_fu_Rdel", "Op_fu_Rirr", "Op_fu_scer", "Op_fu_Scom", "Op_fu_spom", "Op_fu_Spun", "Op_fu_Trub", "Op_fu_Umey", "Op_fu_Wseb", "Op_fu_ylip", "Op_ic_Apar", "Op_ic_Cowc", "Op_ic_Sarc", "Op_is_Mvib", "Op_me_aaeg", "Op_me_Aaur", "Op_me_Acal", "Op_me_agam", "Op_me_amel", "Op_me_apis", "Op_me_Aque", "Op_me_Avag", "Op_me_Avir", "Op_me_Bflo", "Op_me_bmaa", "Op_me_bmor", "Op_me_Bplu", "Op_me_cbri", "Op_me_cele", "Op_me_Cfol", "Op_me_Cgig", "Op_me_cint", "Op_me_clup", "Op_me_Cmey", "Op_me_cpip", "Op_me_Cpul", "Op_me_Ctel", "Op_me_dmel", "Op_me_Dpul", "Op_me_drer", "Op_me_ecab", "Op_me_Emue", "Op_me_ggal", "Op_me_Hcal", "Op_me_Hech", "Op_me_Hrob", "Op_me_hsap", "Op_me_Hvul", "Op_me_isca", "Op_me_Lbai", "Op_me_Lcha", "Op_me_mdom", "Op_me_Mlei", "Op_me_mmul", "Op_me_mmus", "Op_me_nvec", "Op_me_oana", "Op_me_Ocar", "Op_me_Odio", "Op_me_Olob", "Op_me_Omin", "Op_me_Pcar", "Op_me_Pglo", "Op_me_phum", "Op_me_Ppil", "Op_me_ptro", "Op_me_rnor", "Op_me_Sdom", "Op_me_Skow", "Op_me_sman", "Op_me_Srap", "Op_me_tadh", "Op_me_Tbry", "Op_me_Tkit", "Op_me_tnig", "Op_me_trub", "Op_me_Tspi", "Op_me_Xboc", "Pl_gl_Cglo", "Pl_gl_Cpad", "Pl_gl_Gnos", "Pl_gl_Gwit", "Pl_gr_Aace", "Pl_gr_Aalb", "Pl_gr_atha", "Pl_gr_Atri", "Pl_gr_Bpra", "Pl_gr_Cinc", "Pl_gr_Cjap", "Pl_gr_Cmoe", "Pl_gr_Corb", "Pl_gr_crei", "Pl_gr_Cscu", "Pl_gr_Csti", "Pl_gr_Cvar", "Pl_gr_Dsal", "Pl_gr_Dten", "Pl_gr_Egui", "Pl_gr_Gbil", "Pl_gr_Hann", "Pl_gr_Heli", "Pl_gr_Mant", "Pl_gr_micr", "Pl_gr_Mpol", "Pl_gr_Mpus", "Pl_gr_Mspa", "Pl_gr_Mver", "Pl_gr_Npyr", "Pl_gr_Ntab", "Pl_gr_Oluc", "Pl_gr_Omed", "Pl_gr_osat", "Pl_gr_otau", "Pl_gr_Pcap", "Pl_gr_Pcol", "Pl_gr_Pgel", "Pl_gr_Pgin", "Pl_gr_Pobo", "Pl_gr_Pokl", "Pl_gr_Ppaa", "Pl_gr_ppat", "Pl_gr_Prap", "Pl_gr_Psal", "Pl_gr_Psin", "Pl_gr_Pspa", "Pl_gr_Pspd", "Pl_gr_Pspf", "Pl_gr_Pspg", "Pl_gr_Ptae", "Pl_gr_Pwic", "Pl_gr_rcom", "Pl_gr_Sobl", "Pl_gr_Tchu", "Pl_gr_Tstr", "Pl_gr_vcar", "Pl_rh_Batr", "Pl_rh_Ccho", "Pl_rh_Ccoe", "Pl_rh_cmer", "Pl_rh_Eaus", "Pl_rh_Eden", "Pl_rh_Emad", "Pl_rh_Furc", "Pl_rh_Goki", "Pl_rh_Gsul", "Pl_rh_Gten", "Pl_rh_Hpul", "Pl_rh_Kalv", "Pl_rh_Lden", "Pl_rh_Paer", "Pl_rh_Phai", "Pl_rh_Pyez", "Pl_rh_Rhod", "Pl_rh_Rmac", "Pl_rh_Rmar", "Pl_rh_Toli", "Sr_ap_bbov", "Sr_ap_chom", "Sr_ap_cmur", "Sr_ap_Cpar", "Sr_ap_Eace", "Sr_ap_Emax", "Sr_ap_Eten", "Sr_ap_Gnip", "Sr_ap_Hham", "Sr_ap_Labb", "Sr_ap_ncan", "Sr_ap_pber", "Sr_ap_pcha", "Sr_ap_pfal", "Sr_ap_pkno", "Sr_ap_pviv", "Sr_ap_pyoe", "Sr_ap_tann", "Sr_ap_tgon", "Sr_ap_tpar", "Sr_ch_Cvel", "Sr_ch_Vbra", "Sr_ci_Ahae", "Sr_ci_Ansp", "Sr_ci_Bame", "Sr_ci_Bjap", "Sr_ci_Brsp", "Sr_ci_Btru", "Sr_ci_Camp", "Sr_ci_Cirr", "Sr_ci_Clim", "Sr_ci_Cmag", "Sr_ci_Cpsp", "Sr_ci_Cunc", "Sr_ci_Cxsp", "Sr_ci_Dmuc", "Sr_ci_Dnas", "Sr_ci_Drum", "Sr_ci_Ecau", "Sr_ci_Ecra", "Sr_ci_Eeca", "Sr_ci_Efoc", "Sr_ci_Ehar", "Sr_ci_Emag", "Sr_ci_Fehr", "Sr_ci_Fron", "Sr_ci_Ftar", "Sr_ci_Glsp", "Sr_ci_Imul", "Sr_ci_Ipro", "Sr_ci_Knsp", "Sr_ci_Lemb", "Sr_ci_Lito", "Sr_ci_Lxsp", "Sr_ci_Mavi", "Sr_ci_Meto", "Sr_ci_Mpul", "Sr_ci_Nosp", "Sr_ci_Nova", "Sr_ci_Otri", "Sr_ci_Padh", "Sr_ci_Pmul", "Sr_ci_Posp", "Sr_ci_Pper", "Sr_ci_Pros", "Sr_ci_Pspe", "Sr_ci_Pssp", "Sr_ci_Ptet", "Sr_ci_Rmsp", "Sr_ci_Samb", "Sr_ci_Sasu", "Sr_ci_Scer", "Sr_ci_Sinc", "Sr_ci_Slem", "Sr_ci_Smin", "Sr_ci_Sond", "Sr_ci_Spat", "Sr_ci_Sras", "Sr_ci_Sroe", "Sr_ci_Sspp", "Sr_ci_Tcsp", "Sr_ci_tthe", "Sr_ci_Vort", "Sr_ci_Zssp", "Sr_di_Acar", "Sr_di_Amas", "Sr_di_Aost", "Sr_di_Aspi", "Sr_di_Aspp", "Sr_di_Atam", "Sr_di_Bnut", "Sr_di_Ccoh", "Sr_di_Cfus", "Sr_di_Dacu", "Sr_di_Dbal", "Sr_di_Espp", "Sr_di_Gaus", "Sr_di_Gcat", "Sr_di_Gspi", "Sr_di_Harc", "Sr_di_Hsps", "Sr_di_Htri", "Sr_di_Kbre", "Sr_di_Kfol", "Sr_di_Kmic", "Sr_di_Kmik", "Sr_di_Kven", "Sr_di_Lelo", "Sr_di_Lfis", "Sr_di_Lpol", "Sr_di_Nsci", "Sr_di_Omar", "Sr_di_Paci", "Sr_di_Pbah", "Sr_di_Pbei", "Sr_di_Pgla", "Sr_di_Plim", "Sr_di_Plun", "Sr_di_Pmin", "Sr_di_Ppis", "Sr_di_Pret", "Sr_di_Pspp", "Sr_di_Shan", "Sr_di_Skaw", "Sr_di_Smic", "Sr_di_Stro", "Sr_di_Syma", "Sr_di_Tjol", "Sr_pe_Olen", "Sr_pe_Pche", "Sr_pe_Perk", "Sr_rh_Aelo", "Sr_rh_Amsp", "Sr_rh_Asco", "Sr_rh_Aspa", "Sr_rh_Astr", "Sr_rh_Blon", "Sr_rh_Bmar", "Sr_rh_Bmot", "Sr_rh_Bnat", "Sr_rh_Briz", "Sr_rh_Cdel", "Sr_rh_Cerc", "Sr_rh_Crep", "Sr_rh_Cssp", "Sr_rh_Cten", "Sr_rh_Cysp", "Sr_rh_Emar", "Sr_rh_Erot", "Sr_rh_Eusp", "Sr_rh_Gcom", "Sr_rh_Gspa", "Sr_rh_Lamo", "Sr_rh_Loce", "Sr_rh_Lset", "Sr_rh_Lvor", "Sr_rh_Misp", "Sr_rh_Mmac", "Sr_rh_Nsph", "Sr_rh_Nsps", "Sr_rh_Pbra", "Sr_rh_Pglo", "Sr_rh_Phya", "Sr_rh_Phyb", "Sr_rh_Pmar", "Sr_rh_Pmic", "Sr_rh_Pssp", "Sr_rh_Quin", "Sr_rh_Rfil", "Sr_rh_Spsu", "Sr_rh_Sspa", "Sr_rh_Szan", "Sr_rh_Trsp", "Sr_st_Aana", "Sr_st_Aast", "Sr_st_Acan", "Sr_st_Acof", "Sr_st_Ainv", "Sr_st_Alag", "Sr_st_Alai", "Sr_st_Alim", "Sr_st_Aman", "Sr_st_Amsp", "Sr_st_Apal", "Sr_st_Arad", "Sr_st_Aspb", "Sr_st_Asub", "Sr_st_Atth", "Sr_st_Bhom", "Sr_st_Bpac", "Sr_st_Bspa", "Sr_st_Bspp", "Sr_st_Cfra", "Sr_st_Chys", "Sr_st_Cneb", "Sr_st_Cneo", "Sr_st_Croe", "Sr_st_Cspa", "Sr_st_Cspb", "Sr_st_Cspc", "Sr_st_Csub", "Sr_st_Cten", "Sr_st_Cwai", "Sr_st_Dbri", "Sr_st_Dfra", "Sr_st_Dspa", "Sr_st_Dspe", "Sr_st_Esil", "Sr_st_Espa", "Sr_st_Espi", "Sr_st_Fcyl", "Sr_st_Fjap", "Sr_st_Fpar", "Sr_st_Fser", "Sr_st_Fspa", "Sr_st_Fves", "Sr_st_Goce", "Sr_st_Hseo", "Sr_st_Htam", "Sr_st_Ldig", "Sr_st_Ljap", "Sr_st_Lpar", "Sr_st_Lqpa", "Sr_st_Lqpb", "Sr_st_Mpol", "Sr_st_Mspa", "Sr_st_Ngad", "Sr_st_Nocu", "Sr_st_Npun", "Sr_st_Nspa", "Sr_st_Odan", "Sr_st_Ospa", "Sr_st_Paus", "Sr_st_Pcal", "Sr_st_Pela", "Sr_st_Penc", "Sr_st_Pfar", "Sr_st_Pimp", "Sr_st_Pinf", "Sr_st_Pins", "Sr_st_Pmul", "Sr_st_Poli", "Sr_st_Ppar", "Sr_st_Ppyr", "Sr_st_pram", "Sr_st_Pspl", "Sr_st_Psub", "Sr_st_Pter", "Sr_st_Ptri", "Sr_st_Pult", "Sr_st_Pves", "Sr_st_Pvit", "Sr_st_Rmar", "Sr_st_Sagg", "Sr_st_Sbin", "Sr_st_Scon", "Sr_st_Sdic", "Sr_st_Selo", "Sr_st_Slat", "Sr_st_Spar", "Sr_st_Spus", "Sr_st_Sspa", "Sr_st_Stur", "Sr_st_Suni", "Sr_st_Tfra", "Sr_st_tpse", "Sr_st_Trot", "Sr_st_Tspa"]

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
	t = t.strip('\n')					
										
	if 'OG5' in t:						# Consider only the files that contain the word 'OG5'.
		OG5 = t.split('.')[1].replace('_postguidance', '')	# Take the OG code from the file that contains the tree
										
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
		taxon_names_mod2 = []						# Then, you should initialize this var here.
				
		for taxon in taxon_names:							# Take each taxon name
			taxon_names_mod.append(get_clades(taxon)[4])	# Modify the name using function 'get_clades'
			taxon_names_mod2.append(get_clades(taxon)[3])	# Read at the top what 'get_clades' does 
															# append the modified name in taxon_names_mod
		
		taxon_names_mod2 = list(set(taxon_names_mod2))
		doBL = 'y'
		branches = {}
		numberNodes = 0
		numberLeaves = 0
		error_tree = ''	
		
		if taxon_names_mod2 > 4:
			for taxa in weirdtaxalist:				# For each weird taxon ...
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
				
				
					for node in tree.iterNodesNoRoot():				# For each node in the tree
						allTaxa_node = tree.getAllLeafNames(node)	# Get all taxa from leaves per node...
																	# ... and make a list.
					
						if doBL == 'y':
							numberNodes += 1
							branch = node.br.len											
							branches[str(node)] = float(branch)

				
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
				
					if doBL == 'y':
						total_av = 0
					
						for i in branches: total_av = total_av + branches[i]
						averageBL = (total_av / numberNodes)				

					
					for node in tree.iterNodesNoRoot(): 				# but I really want to start with leaves!
						branchFinal = node.br.len
					
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
							
								sisterTaxa_real = []
								sisterTaxa_match = []
								taxon8times = 0      							# used later for checking monophyletic clades with DIFFERENT cells
								allowedStrains = ["1","2","3","4","5","6","7","8","9","0"]
							
								for taxon in sisterTaxa:						# used later for checking monophyletic clades SAME cells
									if taxa_interest in taxon: sisterTaxa_match.append(taxon)
							
								# In the next loop we will evaluate if it is monophyletic clades with DIFFERENT cells
							
								for taxon in sisterTaxa:								
									taxonfull = (get_clades(taxon)[4])
									if taxonfull[:-2] in taxa_interest:
										if taxonfull[-1] in allowedStrains:
											if taxonfull[8] in allowedStrains:
												taxon8times += 1									
											elif taxonfull[8] == taxa_interest[8]:
												taxon8times += 1
										
								# if monophyletic (with different cells) then we need to move to a deeper node
							
								if taxon8times == len(sisterTaxa):
									branch2report = (node.parent).br.len
									sisterNode = (node.parent).sibling
									if not sisterNode : sisterNode = (node.parent).leftSibling()
									sisterTaxa_real = tree.getAllLeafNames(sisterNode)
									if not sisterTaxa_real :   # Here we had to crete this conditional becase the step above didn't work when branches are 0																					
										sisterTaxa_real = tree.getAllLeafNames(sisterNode.parent)	
										for i in sisterTaxa : sisterTaxa_real.remove(i)
									
								else:
																
									if len(sisterTaxa_match) == len(sisterTaxa):	# So, if we also have a monophyletic clade (not from different cells), 
																					# then it should be processed as above.
									
										if not (node.parent).br : continue
										branch2report = (node.parent).br.len
										sisterNode = (node.parent).sibling
										if not sisterNode : sisterNode = (node.parent).leftSibling()
										sisterTaxa_real = tree.getAllLeafNames(sisterNode)
										if not sisterTaxa_real : 
											sisterTaxa_real = tree.getAllLeafNames(sisterNode.parent)	
											for i in sisterTaxa : sisterTaxa_real.remove(i)								
									
									else:										# when no mpnophyletic
										branch2report = branchFinal
										sisterTaxa_real = sisterTaxa
										sisterTaxa_real.remove(taxon_full)		# Remove leaf to take sister taxa
															
	#							sisterClades = []
								sisterMinors = []
								sisterSequences = ''								
								for taxon in sisterTaxa_real:		
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
										report.write (OG5 + '\t' + taxa + '\t' + taxon_full + '\t' +  result + '\tNA' + '\t' + str(branch2report) + '\t' + str(averageBL) + '\n')	
								
									else:											# If weird taxon hasn't this MC 	
										result = minorClade							# return the MC
																					# report result in output
																				
										if len(sisterTaxa_real) > 10 : sisterSequences = 'too-long'	
										report.write (OG5 + '\t' + taxa + '\t'+ taxon_full + '\t' +  result + '\t' + sisterSequences + '\t' + str(branch2report) + '\t' + str(averageBL) + '\n')	

								if len(sisterMinors) > 1:							# If sister clades has more than 1
									result = "non-monophyletic"						# retrieve 'non-monophyletic'
																					# report result in output
								
									if len(sisterMinors) > 20 : minors = 'too-long'
									report.write (OG5 + '\t' + taxa + '\t' + taxon_full + '\t' +  result + '\t'  + minors + '\t' + str(branch2report) + '\t' + str(averageBL) + '\n') 

				else:
					result = 'no_taxaOFinterest' # If the tree does not have the weird taxon, return 'no_taxaOFinterest'
	#				report.write (OG5 + ',' + taxa + ',' +  result + '\n') # report result in output

				doBL = 'n'

			if 'error tree' in error_tree: # if the tree couldn't be re-rooted, retrieve 'OG cannot be annalized' 
				print OG5 + ' cannot be annalized'
				error_tree = ''
		
		else:
			print OG5 + ":\t" + "This tree is ignored because it contains less than 4 minor clades"
#	print (branches.values()).sort()

#	total = 0
#	for i in branches: total = total + branches[i]
#	averageBL = (total / 100) * 10

report.close() 
