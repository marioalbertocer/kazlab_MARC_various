path_ali = '/Users/marioceron/Downloads/OGs_results2keep/'

(Dir.open(path_ali)).each do |ali|
	if ali =~ /forGuidance.fas_renamed.fas$/
		alignment = File.open(path_ali + ali, 'r')
		alignment = alignment.readlines()
		og = ali[0..9]
		
		taxa = Array.new
#		minors = Array.new

		alignment.each do |line|
			if line =~ />/			
				line = line.gsub(/^>/, '')
				line = line.split('_')
				taxon = line[0] + '_' + line[1] + '_' + line[2]
#				minor = line[0] + '_' + line[1]
				taxa.push(taxon)
#				minors.push(line)
			end
		end
		
		taxa_uniq = taxa.uniq
		taxa_counts = Hash.new
		countEuks = 0
		countProk = 0
		
		taxa_uniq.each do |taxon_uniq|
			
			if taxon_uniq =~ /(Ba_)|(Za_)/
				countProk += 1 					
			else 
				countEuks += 1
			end
			
			count = 0
			taxa.each do |taxon|
				
				if taxon == taxon_uniq
					count += 1
				end

			end
			taxa_counts[taxon_uniq] = count
		end

		euksratio = (countEuks.to_f / (countProk.to_f + countEuks.to_f)).round(3)
		paralogs_counts = taxa_counts.values
		paralogness = (paralogs_counts.reduce(:+) / (paralogs_counts.length).to_f).round(3)
		z = 1.960 # z for 95% confidence
		
		residDiference = (paralogs_counts.map! {|taxon_count| (taxon_count - paralogness)**2}) 
		s = Math.sqrt(residDiference.reduce(:+)/(paralogs_counts.length - 1)).round(3)
		ci = (z.to_f * (s/Math.sqrt(paralogs_counts.length).to_f)).round(3)
		
		puts og + "\t" + countEuks.to_s + "\t" + euksratio.to_s + "\t" + paralogness.to_s + "\t" + s.to_s + "\t" + ci.to_s 
	end
end


