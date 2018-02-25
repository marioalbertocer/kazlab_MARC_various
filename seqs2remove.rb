path = './'
report_summary = File.open(path + "report_walk_contamination_single_022318.txt", 'r').readlines()
rules = File.open(path + "rules", 'r').readlines()
sequences_contamination = File.open(path + "rules_2remove", 'w')
ncbiFiles = './ncbiFiles/'
newncbi = './newncbi/'
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
	if ncbiFile.include? ".fasta"
		taxon = ncbiFile[0..9]
		to_remove = Array.new
		ncbisequences = File.open(ncbiFiles + ncbiFile, "r").readlines()
		newncbiTags = Array.new
		newncbiFile = File.open(newncbi + ncbiFile, "w")



		puts ncbiFile
		
		
		seqs2remove.each do |seq2remove|
			if seq2remove.include? taxon
				puts "to_remove: " + seq2remove
				to_remove.push(seq2remove)
			end
		end
		
		
		
		
		index = 0
		ncbisequences.each do |ncbisequence|
			if ncbisequence =~ /^>/
				tag = ncbisequence.gsub(/>|\n/, "")
				puts tag
				unless to_remove.include? tag
					newncbiFile.write(ncbisequence + ncbisequences[index + 1])
				else
					puts "removed: " + ncbisequence
					puts "removed: " + ncbisequences[index + 1]
				end
			end
			index += 1
		end
	end
end
		
	

	
