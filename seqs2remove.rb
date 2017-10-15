report_summary = File.open("../report_walk_contam_ProteinStructures.txt", 'r').readlines()
rules = File.open("../proteinStructures_rules.txt", 'r').readlines()
sequences_contamination = File.open("../proteinStructures_2remove.txt", 'w')

count = 0
report_summary.each do |line|
	count += 1
	puts count
	line = line.chomp
	line = line.split("\t")
	taxon = line[1]
	sequence = line[2]
	sister = line[3]

	rules.each do |rule|
		rule = rule.chomp
		rule = rule.split("\t")
		taxon_rule = rule[0]
		
		if taxon == taxon_rule
			contamination = rule[1..-1]	
			contamination.each do |taxon_contamination|

				if sister.include? taxon_contamination
					puts sequence
					sequences_contamination.write(sequence + "\n")
				end
				
			end 		
		end
	end
end


