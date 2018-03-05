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
* seqs2remove.rb:removes sequences according to specified rules in local databades (in each instance of the pipeline). It also produces the list of removed sequences so that they can be used for removing in the ready to go folder 
  * Input:
    * report of sister taxa <-- This is the output of walk_tree_contamination.py. A file that list all sister taxa for each taxon in phylogenetic trees
    * rules for contamination removal <-- A list of rules for contamination removal that is based on the report of sister taxa and watching the phylogenetic trees.
    * folder of ncbiFiles
    * empty folder for new ncbiFiles
  * Output:
    * list of sequences to be removed from sequence files of the pipleline database.
    * new ncbiFiles with sequences of contamination already removed
* paralogness.rb: It calculates the paralogness (average number of paralogs per tree), the standar deviation and a confidence interval.
	* Input: Preguidance files.
	* run:
		* paralogness.rb
* getTrees.py: Searches a taxon in trees and copy the trees that contain the taxon.
	* Create a folder
	* place this scrit in the folder
	* run script (python getTrees.py) and follow the steps 
* walk_tree_contamination_single.py: Same than walk_tree_contamination.py but with some modifications to work with single cells and report brach lengths. Read inside script to have more detailed information
	* Create a folder
	* place this scrit and the folder with trees in the folder.
	* Change these two lines
		* path = '/Users/katzlab32/Desktop/sisterReporter/'   <-- Here you need to put the path of the folder that you just created
		* path2 = 'Contamination_Foram_amoebae/'  <-- name of the folder with trees (use backslash at the end)
		* weirdtaxalist = ["Am_ar_edis", "Am_ar_ehis", "Am_ar_einv" ...] <-- replace list of taxa with your taxa of interest or leave empty "[]" if you want to run with all taxa included in your trees
	* run
		* python walk_tree_contamination_single.py
	* IMPORTANT <-- this script requires p4
* Check_tree_contaminant_usingrules: Collects all trees according to a rule of contamination. For instance, if there is a rule like "Sr_ci_Cunc Am", It will collect all trees that have Sr_ci_Cunc sister to a clade of Am
	* Input: 
		* speadsheet: report of walk_tree_contamination_single.py
		* rules = set of rules for which you want to collect the trees
		* treesFolder = Folder in which you have all trees.
	* running: 
		* python Check_trees_contaminant_usingrules.py speadsheet rules treesFolder
* summaryWTCSBL.py: Produces a summary (table) of the output of walk_tree_contamination_single.py. But, it only takes into account the cases in which the branches were short (shorter than the average branch length of the tree)
	* Input:
		* speadsheet: report of walk_tree_contamination_single.py
		* Open script and double check paths and file names
		* run
			* python summaryWTCSBL.py
* renameFiles.rb: Replace words from files in a folder. For instance if I want to replace the name of a taxon (Sr_ci_Cunc) in a set of trees by another name like Sr_ci_Cu01. 
	* Input:
		* Folder with the original files
		* a new empty folder <-- Here the script will place the renamed files
		* a table (.csv) with two columns containing the original word in the first column and the new word in the second column
	* Run: 
		* ruby renameFiles.rb
* check_overlap.rb: Helps to determine if overlap filter is removing too many 'good' sequences by counting sequences kept and removed after the filter
	* Input:
		* The whole folder my-data from PhyloTOL
	* Output: 
		* It retrieves all sequences that were removed for the overla filter. It put them in a folder created by the user
		* It prints in the terminal a table with counts of sequences in:
			* before overlap filter
			* during the filter (tsv files)
			* after the filter (pre-guidance files)