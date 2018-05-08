import os
from p4 import *
var.doRepairDupedTaxonNames = 2 # This line fixes duplicates problems for p4

#path = '/Users/marioceron/Documents/katzlab/Pipelinev2_2_archive/'
path = '/Users/katzlab32/Documents/PhyloTOL/050718_dupli/'
#path = '/Users/marioceron/Documents/katzlab/NonRandom.MicroIn/02-RAxML_trees/'

OGs = []
count = 0

def get_clades(taxon):
    taxon_id = taxon.split('_')
    taxon_name = taxon_id[0] + '_' + taxon_id[1] + '_' + taxon_id[2]
    taxon_name_short = taxon_id[0] + '_' + taxon_id[1]
    taxon_name_shortest = taxon_id[0]
    return taxon_name, taxon_name_short, taxon_name_shortest

for tree_file in os.listdir(path):    
    
    if 'OG5_' in tree_file:
    	OG = 'OG5_' + (tree_file.split('OG5_')[1])[0:6]
        count += 1
#        print "Count = %s\t%s" % (count, tree_file)
		
#        OG = tree_file.split('_')[0] + '_' + tree_file.split('_')[1]
#        OG = tree_file.split('.')[1]
        tree_file = tree_file.strip('\n')
        tree_line = open('%s%s' % (path, tree_file))
        tree_line = tree_line.readline()

        var.trees = []
        
        if '-' in tree_line:
            tree_lineNEW = tree_line.replace('-', '')    
        else:
            tree_lineNEW = tree_line
        if '>' in tree_lineNEW:
            tree_lineNEW = tree_lineNEW.replace('>', '')
        if '/' in tree_lineNEW:
            tree_lineNEW = tree_lineNEW.replace('/', '')

        TN = open ('%stemp_%s' % (path, tree_file), 'w')
        TN.write (tree_lineNEW)
        TN.close()
        tree_fileNEW = '%stemp_%s' % (path, tree_file)
        read(tree_fileNEW)
        tree = var.trees[0]
        
        Taxa = tree.getAllLeafNames(tree.root)
        
        for taxon in Taxa:
            taxonNames = get_clades(taxon)
            NamesTaxon = "%s\t%s\t%s\t%s" % (OG, taxonNames[0], taxonNames[1], taxonNames[2])
            print NamesTaxon
                       
        os.remove('%stemp_%s' % (path, tree_file))