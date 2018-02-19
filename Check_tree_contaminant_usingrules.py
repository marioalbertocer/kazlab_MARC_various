#!/usr/bin/python

# This script is intended to collect all trees according to a rule of contamination. For instance
# If there is a rule like "Sr_ci_Cunc Am", It will collect all trees that have Sr_ci_Cunc sister to a clade of Am

# Running as:
# python Check_trees_contaminant_usingrules.py speadsheet rules treesFolder

# speadsheet = Spreadsheet reporting sisterclades
# rules = set of rules for which you want to collect the trees
# treesFolder = Folder in which you have all trees.
 

import sys
import os
from sys import argv

def copy_tree_rule(line, rules, treefolder):
	
	values = line.split("\t")
	for rule in rules:
		cont = (rule.replace("\n", "")).split('\t')[1:] 
		if values[1] == rule.split('\t')[0]:
			for contamination in cont:
				if contamination in values[3]:
					os.system('mkdir Treetolookat/' + values[1] + "-" + contamination)
					os.system('cp ' + treefolder + "/" + "*" + values[0] + "* Treetolookat/"+ values[1] + "-" + contamination + "/")			
def main():

	script, spreadsheet, rulefile, treefolder = argv
	os.system('mkdir Treetolookat')
	
	rules = open(rulefile, 'r').readlines()
	spreadsheet = open(spreadsheet, 'r').readlines()
	
	for line in spreadsheet : copy_tree_rule(line.replace('\n', ''), rules, treefolder)

main()




