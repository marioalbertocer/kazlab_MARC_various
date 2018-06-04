path2trees = '/Users/katzlab32/Documents/PhyloTOL/051418_dupli/'
#out = File.open(path + folder + 'criteriaANDcounts_out.txt', 'w')

mncCut = 3
mjcCut = 3
ignoreMJC = ['EE', 'Ba' + 'Za']

treesDir = Dir.open(path2trees)
treesDir.each do |i|

	if i =~ /OG5_/
		og = "OG5_" + (i.split("OG5_")[1])[0..5]
		
		minCs = Array.new()
		majCs = Array.new()

		op = am = pl = ex = sr = ee = ba = za = 0
		criterion1 = 'no'
		
		# for each OG read the folder of the trees and read the tree for the OG		
		tree = File.open(path2trees + i, 'r').readline()
		
		# As the trees are in neweck format, we can make a list of leaves by 
		# splitting the tree by the comas.
		tree = tree.split(',')

		# if there are more than 10 leaves in the tree, it meets the criterion 1
		if tree.length > 10
			criterion1 = 'yes'

			# Here we are going to clean the leaves, so that we can extract
			# the major clade and minor clade (e.g., Sr_di).
			# We collect all cleaned leaves in a list.
			tree.each do |leaf|
				leaf = leaf.gsub(/\(/, "")
				leaf = leaf.gsub(/\)/, "")
				leaf = leaf.split("_")
				minCs << leaf[0] + "_" + leaf[1]
				majCs << leaf[0]		
			end
		end	
		
		# Now that we have all the leaves (as Sr_di) in a list, we need to 
		# remove duplicates:
		minCs.uniq!
		majCs.uniq!
		
		# if there are at least 2 minor clades for at least 3 major clades, it meets criterion 2
		num_mjc = 0
		criterion2 = 'no'
		if majCs.length >= mjcCut
			majCs.each do |majC|
				counter = 0
				if ignoreMJC !~ majC
					minCs.each do |minC|
						if majC == minC.split('_')[0]
							counter += 1
						end
					end
					if counter >= 2 then num_mjc += 1 end
				end
			end
		end
		if num_mjc >= 3 then criterion2 = 'yes' end

		# Finally, we count the number of minor clades per major clade there are 
		# in the tree. 
		minCs.each do |minC|
			pl = pl + 1	if (minC =~ /Pl_/)
			ee = ee + 1 if (minC =~ /EE_/)
			sr = sr + 1	if (minC =~ /Sr_/)
			ex = ex + 1	if (minC =~ /Ex_/)
			am = am + 1 if (minC =~ /Am_/)															
			op = op + 1 if (minC =~ /Op_/)
			za = za + 1 if (minC =~ /Za_/)
			ba = ba + 1 if (minC =~ /Ba_/)					
		end
			
 		# The report is corrected with criterion and counts and printed in the terminal
		puts "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % [og, criterion1, criterion2, op, am, ex, ee, pl, sr, za, ba]
#		out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % [line, og, criterion, op, am, ex, ee, pl, sr, za, ba]) 		
	end
end
