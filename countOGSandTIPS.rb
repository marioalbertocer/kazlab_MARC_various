path = "/Users/katzlab32/Documents/PhyloTOL/051418_dupli/"
taxa = ["Am_ar_Enut", "Am_ar_Mbal", "Am_di_Acas", "Am_di_Mspa", "Am_di_Naes", "Am_is_Fnol", "Am_my_Dpur", "Am_my_Ppol", "Ba_ac_Cdip", "Ba_aq_aaeo", "Ba_ba_Bfra", "Ba_bc_Ctha", "Ba_cd_Cmur", "Ba_ch_Caur", "Ba_cv_Amuc", "Ba_cy_Acyl", "Ba_cy_Onig", "Ba_cy_Pspb", "Ba_de_Trad", "Ba_di_Dtur", "Ba_fb_Gkau", "Ba_fc_Oval", "Ba_fu_Fnuc", "Ba_ni_Tyel", "Ba_pa_Abra", "Ba_pa_rpro", "Ba_pb_bpse", "Ba_pb_Vpar", "Ba_pd_Daes", "Ba_pg_Abau", "Ba_pg_ecol", "Ba_pl_Plim", "Ba_sp_Sple", "Ba_te_Alai", "Ba_th_tmar", "EE_ap_Ttra", "EE_br_Bant", "EE_ce_Chsp", "EE_ce_Rhet", "EE_cr_Gcry", "EE_ha_Ehux", "EE_ha_Igal", "EE_is_Tglo", "EE_is_Tmar", "EE_ka_Rtru", "Ex_eu_Bsal", "Ex_eu_Egym", "Ex_eu_linf", "Ex_eu_tcon", "Ex_he_Ngru", "Ex_is_Tpyr", "Ex_ja_Rame", "Ex_ma_Mjak", "Ex_ox_Mono", "Ex_pa_Tfoe", "Ex_pa_tvag", "Op_ch_mbre", "Op_ch_Sros", "Op_fu_Aalg", "Op_fu_Amac", "Op_fu_Bden", "Op_fu_Ccor", "Op_fu_Dspa", "Op_fu_Lcor", "Op_fu_Rall", "Op_fu_scer", "Op_ic_Cowc", "Op_ic_Sarc", "Op_me_cele", "Op_me_Cpul", "Op_me_Ctel", "Op_me_Dpul", "Op_me_hsap", "Op_me_Hvul", "Op_me_Ppil", "Op_me_Skow", "Op_me_sman", "Op_me_tadh", "Pl_gl_Cpad", "Pl_gl_Gnos", "Pl_gr_atha", "Pl_gr_Atri", "Pl_gr_crei", "Pl_gr_Cvar", "Pl_gr_Mpol", "Pl_gr_Pcol", "Pl_gr_Pspg", "Pl_gr_Tchu", "Pl_rh_Ccho", "Pl_rh_Ccoe", "Pl_rh_Gsul", "Pl_rh_Rmar", "Sr_ap_Cpar", "Sr_ap_pfal", "Sr_ch_Vbra", "Sr_ci_Ptet", "Sr_ci_Scer", "Sr_ci_Slem", "Sr_di_Aspi", "Sr_di_Gcat", "Sr_di_Hsps", "Sr_di_Omar", "Sr_di_Smic", "Sr_pe_Perk", "Sr_rh_Bmot", "Sr_rh_Bnat", "Sr_rh_Cten", "Sr_rh_Erot", "Sr_rh_Lvor", "Sr_rh_Sspa", "Sr_st_Aana", "Sr_st_Aman", "Sr_st_Bhom", "Sr_st_Bpac", "Sr_st_Cfra", "Sr_st_Croe", "Sr_st_Csub", "Sr_st_Dspe", "Sr_st_Esil", "Sr_st_Espi", "Sr_st_Goce", "Sr_st_Ngad", "Sr_st_Ospa", "Sr_st_Pinf", "Sr_st_Ppar", "Sr_st_Ptri", "Sr_st_Spus", "Sr_st_tpse", "Za_as_Heia", "Za_as_Loki", "Za_as_Odin", "Za_as_Thob", "Za_cr_Sisl", "Za_cr_Tneu", "Za_eb_Mspa", "Za_ec_Minf", "Za_eh_Haci", "Za_eh_Ngre", "Za_em_Mhol", "Za_ep_tvol", "Za_et_Tkod", "Za_ey_Mkan", "Za_ko_ckor", "Za_na_nequ", "Za_pa_Maci", "Za_th_Csym", "EE_ap_Asig", "EE_ap_Ftro", "EE_ap_Mpla", "EE_ap_Nlon", "EE_ap_Rram", "EE_is_Drot"]

taxa.each do |taxon|
	ogs = 0
	tips = 0

	(Dir.open(path)).each do |file|
		if file =~ /\.tre/
			og = file[15..24]
			tree = (File.open(path + file, "r").readline()).gsub("\n", "")
			if tree.include? taxon then ogs += 1 end
			tree = tree.split(",")
		
			taxaINtree = Array.new
		
			tree.each do|taxonINtree|
				taxonINtree = taxonINtree.gsub("(", "")	
				taxonINtree = taxonINtree.gsub(/(.{10})(.*)/, '\1')
				taxaINtree.push(taxonINtree)
			end
			
			if taxaINtree != []
				taxaINtree.each do |taxonINtree|
					if taxonINtree == taxon 
						tips += 1
					end
				end
			end
		end	
	end
	
	puts taxon + "\t" + ogs.to_s + "\t" + tips.to_s
	
end