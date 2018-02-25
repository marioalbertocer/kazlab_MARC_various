path = './'
report_summary = File.open(path + "report_walk_contamination_single_022318.txt", 'r').readlines()
rules = File.open(path + "rules", 'r').readlines()
sequences_contamination = File.open(path + "rules_2remove", 'w')
ncbiFiles = ''
seqs2remove = Array.new

count = 0
report_summary.each do |line|
	count += 1
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
					seqs2remove.push(sequence)
					sequences_contamination.write(sequence + "\n")
				end
			end 		
		end
	end
end

(Dir.open(ncbiFiles)).each do |ncbiFile|
	seqs2remove.each do |seq2remove|
		taxon = (seq2remove.split("_"))[0..9]
		actualseq2rem = (seq2remove.split("_"))[10..-1]
		if ncbiFile.include? taxon
			ncbisequences = File.open(ncbiFiles + ncbiFile, "r").readlines()
			index = 0
			to_remove = 0
			ncbisequences.each do |ncbisequence|
				if actualseq2rem == ncbisequence.sub(">|\n")
					to_remove = index
				end
				index += 1
			end
			removed_seq = ncbisequences.delete_at(to_remove + 1)
			removed_tag = ncbisequences.delete_at(to_remove)
			puts "removed:\t" + removed_tag
			puts "removed:\t" + removed_seq
		end
	end
end
		
	

	
