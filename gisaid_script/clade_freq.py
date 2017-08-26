
import os
import gisaid_to_ncbi_list

	
def put_seqs_by_month(seqs, beginM, endM):

	seqs_byMonth = [ [] for i in range(beginM, endM+1) ]
	
	for sample in seqs:
		head = sample.split("\n")[0]
		ymd = head.split("|")[2].split("/")
		month = int(ymd[1])
		seqs_byMonth[month-1].append(sample)
		
	return seqs_byMonth
	
def calc_frequency_with_subs(subs, seqs_byMonth, regions):
	freq_byMonth = []
	countM = 0
	for month in seqs_byMonth:
		num_by_region = [ 0 for i in range(len(regions)) ]
		countM += 1
		mfreq = 0
		num_na = 0
		for seq in month:
			region = seq.split("\n")[0].split("|")[3]
			if region == "North America":
				num_na += 1
			
			inClade = 1
			for sub in subs:
				site = int(sub.split("_")[0])
				aa = sub.split("_")[1]
				if seq.split("\n")[1][site-1] != aa:
					inClade = 0
					break
			
			if inClade == 1:
				mfreq += 1
				
				region = seq.split("\n")[0].split("|")[3]
				num_by_region[regions.index(region)] += 1
				
		mfreq = 1.0*mfreq/len(month)
		mfreq = str(round(mfreq, 3))
		
		num = sum(num_by_region)
		
		num_by_region = map(str, num_by_region)
		num_by_region = ",".join(num_by_region)
		
		
		freq_byMonth.append(str(countM)+","+mfreq+","+num_by_region+","+str(num)+","+str(num_na)+","+str(len(month)))
	
	return freq_byMonth
	
#parameters
infName = os.path.normpath("../gisaid/gisaid_seqs_170101-170825_aligned_AA.fas")
metafName = os.path.normpath("../gisaid_meta_files/gisaid_meta_170101-170825_cut.csv")
outfName = os.path.normpath("../freq/clade_freq.csv")

gisaid_sep = "_|_"
loc_sep = " / "
date_sep = "-"
use_seg_id = False

beginM = 1
endM = 8

#3c3a
#3c2a
#3c2a+N171K
#3c2a+N171K+N121K
#3c2a+T131K+R142K
#3c2a+S144K+N121K
#N121K T135K N171K

#sub_3c3a = []
#sub_3c2a = []
sub_171k = ["171_K"]
#sub_171k_121k = ["171+K", "121+K", "135-K"]
#sub_171k_121k_135k = ["171+K", "121+K", "135+K"]
sub_131k_142k = ["131_K", "142_K"]
sub_144k_121k = ["144_K", "121_K"]

#get ncbi-like sequences
region_dict = gisaid_to_ncbi_list.get_region_from_metafile(metafName, loc_sep)
seqs = gisaid_to_ncbi_list.gisaid_to_ncbi(infName, gisaid_sep, date_sep, region_dict)
#ncbi format : >id|name|date|region_sep_underbar|4_(HA)

seqs_byMonth = put_seqs_by_month(seqs, beginM, endM)

regions = list(set(region_dict.values()))

freq_171k = calc_frequency_with_subs(sub_171k, seqs_byMonth, regions)
freq_131k_142k = calc_frequency_with_subs(sub_131k_142k, seqs_byMonth, regions)
freq_144k_121k = calc_frequency_with_subs(sub_144k_121k, seqs_byMonth, regions)

outf = open(outfName, "w")
outf.write("clade,month,freq," +",".join(regions)+ ",numCladeSeq,numNA,numTotalSeq\n")
for monthly_freq in freq_131k_142k:
	outf.write("131k142k"+","+monthly_freq+"\n")
	
for monthly_freq in freq_144k_121k:
	outf.write("144k121k"+","+monthly_freq+"\n")
	
for monthly_freq in freq_171k:
	outf.write("171k"+","+monthly_freq+"\n")

outf.close()