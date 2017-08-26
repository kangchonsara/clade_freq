import sys
rawDir = sys.argv[1]

metaf = open(rawDir+"rawFile_for_further_analysis.csv", "r")
outf = open(rawDir+"gisaid_aligned_1217.fas", "w")

country = dict()
for line in metaf:
	each = line.split("\r")[0].split(",")
	try:
 		id = each[0].split(" | ")[0]
 		id = id.replace("EPI", "")
		#name = each[0].split(" | ")[1]
	except IndexError:
		continue
	try:
		loc = each[2].split(" / ")[1]
	except IndexError:
		if each[3].find(" / ") >= 0:
			loc = each[3].split(" / ")[1]
		else:
			continue
	#date = each[3]
	country[id] = loc
	
#id name date region
for year in range(2012, 2018):
	gisaidf = open(rawDir+str(year)+"_align_cut.fas", "r")
	for line in gisaidf:
		if line.find(">") >= 0:
			key = 1
			each = line.split("\r")[0].split("_|_")
			id =  each[3]
			name = each[1]
			ymd = each[2].split("-")
			date = "/".join(ymd)
			try:
				region = country[id].replace(" ", "_")
			except KeyError:
				key = 0
				continue
			seq = ">"+id+"|"+name+"|"+date+"|"+region+"|4_(HA)\n"
		else:
			if key == 1:
				seq += line.split("\r")[0] + "\n"
				outf.write(seq)
	gisaidf.close()
outf.close()
