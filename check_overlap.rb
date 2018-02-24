# Counts the number of sequences:
# - pre-overlapfilter
# - in the tsv file (tested only with the similarity filter turned off)
# - in the pre-guidance file
# This helps to determine if the overlap filter is removing too many 'good' sequences. 
# For running it, just modify te paths accordingly. Beware that the script requires the folder my-data 
# from a run of the pipeline

mydata = '/Users/katzlab32/Desktop/my-data/'
run = '021618_contaminationOGs2'
path = mydata + "/" + run.to_s + "_results/Output/"
fasta2keepDir = path + "fasta2keep/"
results2keep = path + run + "_results2keep/"
ublastDir = path + "UBlastFiles/"
null = '/Users/katzlab32/Desktop/null/'


outs = Hash.new

(Dir.open(path)).each do |outFile|
	if outFile.include? '_out'
		og = (outFile.split("_")[0..1]).join("_")
		taxon = (outFile.split("_")[2..-2]).join("_")			
		key = og + "," + taxon
		out = File.open(path + outFile).readlines()
		outCount = 0
		out.each do |line|
			if line =~ />/
				outCount += 1 
			end
		end
		outs[key] = outCount.to_s
	end
end			

totalf2k = Array.new
(Dir.open(fasta2keepDir)).each do |f2kFile|
	if f2kFile.include? 'fastatokeep.fas'
		og = (f2kFile.split("_")[0..1]).join("_")
		taxon = ((f2kFile.split("_")[2..-1]).join("_")).gsub("fastatokeep.fas", "")	
		key = og + "," + taxon
		f2k = File.open(fasta2keepDir + f2kFile).readlines()
		f2kCount = 0
		f2k.each do |line|
			if line =~ />/
				f2kCount += 1 
			end
		end
		outs[key] = outs[key] + "," + f2kCount.to_s
		totalf2k.push(key)
	end
end			

(outs.keys).each do |key|
	unless totalf2k.include? key
		outs[key] = outs[key] + "," + "0"
	end
end

(Dir.open(ublastDir)).each do |blaFile|
	if blaFile.include? '_resultsFiltered.tsv' 
		og = (blaFile.split("_")[0..1]).join("_")
		taxon = (blaFile.split("_")[2..-2]).join("_")			
		key = og + "," + taxon
		bla = File.open(ublastDir + blaFile).readlines()
		blaCount = 0
		overlapP = Array.new

		if bla != []
			if bla[0] =~ /No sequences.* /
				overlapP.push(bla[0].gsub(/(No sequences.* )|\n/, "")) 
			else
				overlapP.push((bla[0].split("\t"))[1])
				bla.each do |line|
					values = line.split("\t")
					if values[12] == 'OF+'
						overlapP.push(values[0])
					end
				end
			end
		end
		
		blaCount = ((overlapP.uniq).length) if overlapP != []
		outs[key] = outs[key] + "," + blaCount.to_s
		allFile = File.open(path + og + "_" + taxon + "_out.txt", "r").readlines()
		nullFile = File.open(null + og + "_" + taxon + "_null.txt", "a")
		
		seqIndex = 1
		allFile.each do |sequence|
			if sequence =~ /^>/			
				unless overlapP.include? sequence.gsub(/>|\n/, "")
					nullFile.write(sequence + allFile[seqIndex])
				end
			end
			seqIndex += 1
		end
		
	end
end			

allr2k = Hash.new
(Dir.open(results2keep)).each do |r2kFile|
	if r2kFile.include? 'preguidance.fas_renamed.fas'
		og = (r2kFile.split("_")[0..1]).join("_")
		r2k = File.open(results2keep + r2kFile).readlines()
		r2kCount = 0
		
		(outs.keys).each do |og_taxon|
			if og_taxon.include? og
				r2kCount = 0		
				r2k.each do |line|
					if line =~ />/
						taxon = ((line.split("_")[0..2]).join("_")).gsub(">", "")
						key = og + "," + taxon
						if key == og_taxon
							r2kCount += 1
						end 
					end
				end
				allr2k[og_taxon] = r2kCount.to_s
			end
		end
	end
end	

(outs.keys).each do |key|
	puts key + "," + outs[key] + "," + allr2k[key]
end