# kazlab_MARC_various
scripts for my research in katzlab

* walk_tree_contamination.py: This is a script that takes phylogenetic trees and list the sister clade of every taxon. When the sister clade if monophyletic, it reports the sister's taxa minor clade or 'same clade' if the sister taxa are the same than the compared taxon. If the sister clade is polyphyletic, it reports all minor clades of the sister taxa.
 * IMPORTANT <-- this script requires p4
* seqs2remove.rb: It generates a list of sequences of contamination to be removed from sequence files such as genomes or transcriptomes. 
Input
  * Input:
    * report of sister taxa <-- This is the output of walk_tree_contamination.py. A file that list all sister taxa for each taxon in phylogenetic trees
    * rules for contamination removal <-- A list of rules for contamination removal that is based on the report of sister taxa and watching the phylogenetic trees.
  * Output:
    * list of sequences to be removed from sequence files of the pipleline database. 
* paralogness.rb: It calculates the paralogness (average number of paralogs per tree), the standar deviation and a confidence interval.
 * Input: Preguidance files. 
