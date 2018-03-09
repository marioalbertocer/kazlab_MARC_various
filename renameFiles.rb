list = File.open('/Users/katzlab32/Desktop/conta/list', 'r').readlines()

path = '/Users/katzlab32/Desktop/conta/BlastFiles'
pathreplaced = '/Users/katzlab32/Desktop/conta/renamed'

(Dir.open(path)).each do |filename|
	if filename !~ /^\./
			
		file  = File.open(path + "/" + filename, "r").readlines()
		filereplaced = File.open(pathreplaced + "/" + filename, "w")
		file.each do |line|

			line = line.chomp
			line2replace = 'no'
			list.each do |toreplace|
				toreplace = toreplace.chomp
				toreplace = toreplace.split(',')
				if line.include? toreplace[0]
					line2replace = line.gsub(toreplace[0], toreplace[1])
				end
			end
		
			if line2replace == 'no'
				filereplaced.write(line + "\n")
			else
				filereplaced.write(line2replace + "\n")
				puts "replaced line in %s: " % filename
				puts line2replace
			end
		end

	end
end	



