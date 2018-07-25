# This script removes sequences according to specified rules in local databades (in each instance of the pipeline). 
# It also produces the list of removed sequences so that they can be used for removing in the ready to go folder. 

# input: 
# - Report of sister taxa
# - rules
# - folder of ncbiFiles
# - empty folder for new ncbiFiles

# Running:
# - Put all the imput files and folders in the same folder and run scrip with ruby: "ruby seqs2remove.rb"

# ruby seqs2remove.rb path2Files sisterReport rules seqs2remove_out nonHomologs
# ruby seqs2remove.rb ./ sisterReport rules seqs2remove_out nonHomologs

path = ARGV[0]
total2remove = File.open(ARGV[1], 'r').readlines()
ncbiFiles = path + '/ncbiFiles/'
system "mkdir " + path + "/newncbi/"
newncbi = path + '/newncbi/'

puts "\nseqs2removeAD.rb: removing sequences from Databases:"
(Dir.open(ncbiFiles)).each do |ncbiFile|
	if ncbiFile.include? ".fasta"
		taxon = ncbiFile[0..9]
		to_remove = Array.new
		
		ncbisequences_raw = File.open(ncbiFiles + ncbiFile, "r").readlines()
		
		# ---- correcting .fasta format ----
		
		ncbisequences = Array.new
		seq = ''
		
		ncbisequences_raw.each do |line|
			if line =~ /^>/
				if seq != '' then ncbisequences << seq end	
				ncbisequences << line.gsub("\n", "")
				seq = ''
			end
			if line =~ /^([A-z]|\*)/ then seq = seq + line.gsub("\n", "") end
		end
		
		ncbisequences << seq
		
		#------------------------------------
		
		newncbiTags = Array.new
		newncbiFile = File.open(newncbi + ncbiFile, "w")

		puts ncbiFile
	
		total2remove.each do |seq2remove|
			seq2remove = seq2remove.gsub(/\n/, "")
			if seq2remove.include? taxon
				to_remove << seq2remove
			end
		end
		
		index = 0
		ncbisequences.each do |ncbisequence|
			if ncbisequence =~ /^>/
				tag = ncbisequence.gsub(/>|\n/, "")
				unless to_remove.include? tag
					newncbiFile.write(ncbisequence + "\n" + ncbisequences[index + 1] + "\n")
				else
					puts "\nremoved: " + ncbisequence
					puts "removed: " + ncbisequences[index + 1] + "\n"
				end
			end
			index += 1
		end
		newncbiFile.close
	end
end

system "rm -r " + ncbiFiles
system "mv " + newncbi + "\t" + ncbiFiles
