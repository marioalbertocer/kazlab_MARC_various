# kazlab_MARC_various
scripts for my research in katzlab

* walk_tree_contamination.py: Takes phylogenetic trees and list the sister clade of every taxon. When the sister clade if monophyletic, it reports the sister's taxa minor clade or 'same clade' if the sister taxa are the same than the compared taxon. If the sister clade is polyphyletic, it reports all minor clades of the sister taxa.
	* Create a folder
	* place this scrit and the folder with trees in the folder.
	* Change these two lines
		* path = '/home/mario/walk_tree/'   <-- Here you need to put the path of the folder that you just created
		* path2 = 'treesYY/'   <-- name of the folder with trees (use backslash at the end)
		* weirdtaxalist = ["Sr_st_psub", "Pl_gr_Pokl", "Pl_rh_cmer" ...] <-- replace list of taxa with your taxa of interest
	* run script
	* IMPORTANT <-- this script requires p4
* seqs2remove.rb: It generates a list of sequences of contamination to be removed from sequence files such as genomes or transcriptomes. 
  * Input:
    * report of sister taxa <-- This is the output of walk_tree_contamination.py. A file that list all sister taxa for each taxon in phylogenetic trees
    * rules for contamination removal <-- A list of rules for contamination removal that is based on the report of sister taxa and watching the phylogenetic trees.
  * Output:
    * list of sequences to be removed from sequence files of the pipleline database. 
* paralogness.rb: It calculates the paralogness (average number of paralogs per tree), the standar deviation and a confidence interval.
	* Input: Preguidance files.
* getTrees.py: Searches a taxon in trees and copy the trees that contain the taxon.
	* Create a folder
	* place this scrit in the folder
	* run script and follow the steps 
* walk_tree_contamination_single.py: Same than walk_tree_contamination.py but with some modifications to work with single cells and report brach lengths. Read inside script to have more detailed information
	* Create a folder
	* place this scrit and the folder with trees in the folder.
	* Change these two lines
		* path = '/Users/katzlab32/Desktop/sisterReporter/'   <-- Here you need to put the path of the folder that you just created
		* path2 = 'Contamination_Foram_amoebae/'  <-- name of the folder with trees (use backslash at the end)
		* weirdtaxalist = ["Am_ar_edis", "Am_ar_ehis", "Am_ar_einv" ...] <-- replace list of taxa with your taxa of interest
	* run script
	* IMPORTANT <-- this script requires p4
* Check_tree_contaminant_usingrules: Collects all trees according to a rule of contamination. For instance, if there is a rule like "Sr_ci_Cunc Am", It will collect all trees that have Sr_ci_Cunc sister to a clade of Am
	* Input: 
		* speadsheet: report of walk_tree_contamination_single.py
		* rules = set of rules for which you want to collect the trees
		* treesFolder = Folder in which you have all trees.
	* running: 
		* python Check_trees_contaminant_usingrules.py speadsheet rules treesFolder
* summaryWTCSBL.py <-- Produces a summary (table) of the output of walk_tree_contamination_single.py. But, it only takes into account the cases in which the branches were short (shorter than the average branch length of the tree)
	* Input:
		* speadsheet: report of walk_tree_contamination_single.py
		* Open script and double check paths and file names
		* run


