import os, re

report = open('./report_walk_contamination_single-all.txt', 'r').readlines() # This is the output of the walking script
output = open('./summary_contamination_all_singBLave.csv', 'w')
output.write("Taxon,same,Sr_,Pl_,EE_,Ex_,Am_,Op_,Ba_,Za_,non-monophyletic,Total\n")

trees = []
taxa = []

for i in report :    				# Extract the OGs and the taxa from the report of the walking script
	trees.append(i.split("\t")[0])	
	taxa.append(i.split("\t")[1])

trees = sorted(list(set(trees)))	# Sort list of trees and taxa (removing duplicates)
taxa = sorted(list(set(taxa)))

for taxon in taxa:
	
	sm = sr = pl = ee = ex = am = op = ba = za = nm = to = 0  # These are all the columns for the summary

	for line in report:   #  Filling the table ...
		values = line.split('\t')
		
		if values[1] == taxon:
			to += 1
			if values[3] != 'same_minor': # If the sister is not the same minor clade, then report all with samll branch lengths
				if float(values[5]) < float(values[6]) : # If branch length is smaller than average
#				if float(values[5]) < 0.1 : # If branch length is smaller than 0.1
				
					if values[3] == 'non-monophyletic' : nm += 1
					if 'Sr_' in values[3] : sr += 1
					if 'Pl_' in values[3] : pl += 1
					if 'EE_' in values[3] : ee += 1
					if 'Ex_' in values[3] : ex += 1
					if 'Am_' in values[3] : am += 1
					if 'Op_' in values[3] : op += 1
					if 'Ba_' in values[3] : ba += 1
					if 'Za_' in values[3] : za += 1
					
			else : sm += 1		
			
	newLine = taxon
	for i in [sm,sr,pl,ee,ex,am,op,ba,za,nm,to] : 
		newLine = newLine + ',' + str(i)

	print newLine     #  Printing ...
	output.write(newLine + "\n")
	
	
