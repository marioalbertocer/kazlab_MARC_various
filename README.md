# kazlab_MARC_various
scripts for my research in katzlab

* seqs2remove.rb: It generates a list of sequences of contamination to be removed from sequence files such as genomes or transcriptomes. 
Input
  * Input:
    * report of sister taxa <-- This is the output of walk_tree_contamination.py. A file that list all sister taxa for each taxon in phylogenetic trees
    * rules for contamination removal <-- A list of rules for contamination removal that is based on the report of sister taxa and watching the phylogenetic trees.
  * Output:
    * list of sequences to be removed from sequence files of the pipleline database. 
  
