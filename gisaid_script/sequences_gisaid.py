#ToDo
#check region
#check set season
import random
import sys

EA = ["Japan", "China", "Hong_Kong", "Thailand", "Philippines", "Singapore", 
	"Malaysia", "Viet_Nam", "Taiwan", "South_Korea", "Cambodia", "Macao",
	"Mongolia", "Korea", "Indonesia", "Vietnam", "Palau", "Lao", "Hong_Kong_(SAR)", "Myanmar"]
AS = ["Sri_Lanka", "Nepal", "Kuwait", "Qatar", "Iraq", "Jordan", "Kyrgyzstan",
	"Saudi_Arabia", "Iran", "Georgia", "Bahrain", "Oman", "Pakistan", "India", "Turkey", "Afghanistan",
	"Bangladesh", "Armenia", "Ukraine", "Palestinian_Territory", "Israel", "Kazakhstan"]
EU = ["Netherlands", "United_Kingdom", "Russia", "France", "Norway", "Sweden",
	"Germany", "Italy", "Switzerland", "Spain", "Austria", "Serbia", "Denmark",
	"Czech_Republic", "Slovenia", "Finland", "Albania", "Bulgaria", "Romania", "Portugal",
	"Latvia", "Hungary", "Luxembourg", "Ireland", "Belarus", "Belgium", "Poland", "Moldova",
	"Estonia", "Russian_Federation", "Cyprus", "Bosnia_and_Herzegovina", "Macedonia", "Greece"]
AF = ["South_Africa", "Ghana", "Senegal", "Djibouti", "Egypt", "Kenya", "Ethiopia", "Cameroon", "Tanzania",
	"Togo", "Mali", "Central_African_Republic", "Mozambique", "Uganda", "Niger", "Nigeria",
	"Algeria", "Morocco", "Cote_d'Ivoire", "Lebanon", "Rwanda", "Madagascar", "Zambia", "Tunisia", 
	"Congo", "Burkina_Faso"]
NA = ["USA", "Guam", "Canada", "United_States"]
SA = ["Mexico", "Nicaragua", "Uruguay", "Brazil", "El_Salvador", "Dominican_Republic",
	"Colombia", "Argentina", "Bolivia", "Saint_Lucia", "Guatemala", "Dominica", 
	"Peru", "Panama", "Ecuador", "Chile", "Barbados", "Suriname", "Venezuela", "Trinidad_and_Tobago",
	"Honduras", "Paraguay", "Costa_Rica"]
OC = ["Australia", "New_Zealand", "Solomon_Islands", "Fiji"]
regions = [EA, AS, EU, AF, NA, SA, OC]

def check_seq(seq): #this criteria can be changed
	isBad = 0
	nbad = 0
	for s in range(len(seq)):
		if (seq[s]!='A') and (seq[s]!='C') and (seq[s]!='G') and (seq[s]!='T'):
			isBad = 1
			break

	return isBad
				

def season_list(infName, beginS, endS):
	bySeason = [[] for i in range(beginS*2, (endS+1)*2-1)]
	inf = open(infName, "r")
	numbad = 0
	for line in inf:
		if line.find(">") >= 0 :
			seq = line	
			ctime = line.split("|")[2].split("/")
			y = int(ctime[0])
			try:
				m = int(ctime[1])
			except ValueError:
				m = 0 #I cannot assign season for sequences without month info
				continue
			if y< beginS-1 or (y== beginS-1 and m < 10) or (y==endS and m > 3) or y>endS:
				m = 0 
				continue			
			
			if m >= 10: 
				t1 = (y+1)-beginS
			else: 
				t1 = y - beginS

			if m >= 10 or m <= 3: 
				t2 = 0
			else: 
				t2 = 1

			idx = t1*2 + t2
		else:
			if m==0:
				continue
			seq += line.upper()
			badseq = check_seq(line.upper().split("\n")[0])
			if badseq :
				numbad += 1
				continue
			bySeason[idx].append(seq)
	print ("numbad", numbad)
	return bySeason
			
def add_April(bySeason, infName, endS):
	inf = open(infName, "r")
	numbad = 0
	for line in inf:
		if line.find(">") >= 0 :
			add = 0
			seq = line	
			ctime = line.split("|")[2].split("/")
			y = int(ctime[0])
			try:
				m = int(ctime[1])
			except ValueError:
				m = 0 #I cannot assign season for sequences without month info
				continue
			if y == endS and m == 4:
				add = 1
		else:
			if add==0:
				continue
			seq += line.upper()
			badseq = check_seq(line.upper().split("\n")[0])
			if badseq :
				numbad += 1
				continue
			bySeason[-1].append(seq)
	return bySeason
		

def remove_duplicates(seasons):
	bySeason = []
	for s in range(len(seasons)):
		genotypes = []
		seqs = []
		for seq in seasons[s]:
			found = 0
			country = seq.split("|")[3]
			for r in range(len(regions)):
				if country in regions[r]:
					found = 1
					break
			if found == 0:
				continue
			genotype = str(r) + seq.split("\n")[1]
			if genotype in genotypes:
				continue
			else:
				genotypes.append(genotype)
				seqs.append(seq)
		bySeason.append(seqs)
	return bySeason
		
def genotype_list(seasons, endS):
	bySeason = []
	mi_list = []
	for s in range(len(seasons)):
		genotypes = []
		mi = []
		season = []
		for seq in seasons[s]:
			genotype = seq.split("\n")[1]
			if genotype in genotypes:
				mi[genotypes.index(genotype)] += 1
			else:
				genotypes.append(genotype)
				mi.append(1)
				season.append(seq)
		mi_list.append(mi)
		bySeason.append(season)
	
	return bySeason, mi_list[-1]
	
def make_fasta(seasons, endS, mi, dataDir, sidx_offset):
	fastafname = dataDir+str(endS)+"gisaid"
	mif = open(dataDir+"mi_"+str(endS)+".txt", "w")	
	seqs = []
	for sidx in range(len(seasons)):
		names = []
		nname = []
		for seqid in range(len(seasons[sidx])):
			seq = seasons[sidx][seqid]
			each = seq.split("|")
			name = each[1].replace("_", "")
			name = name.replace("-", "")
			name = name.replace("(", "")
			name = name.replace(")", "")
			num = ''
			if name in names:
				nname[names.index(name)] += 1
				for i in range(nname[names.index(name)]):
					num+=str('d')
			else:
				names.append(name)
				nname.append(1)
			head = name+num+ "|" + str(sidx+sidx_offset)
			sample = ">" + head + "\n"
			sample += seq.split("\n")[1].replace("\n", "") + "\n"
			seqs.append(sample)
			
			if sidx == len(seasons)-1:
				mif.write(head + " " + str(mi[seqid]) + "\n")
	mif.close()	
	for k in range(1, 11):
		outf = open(fastafname+"_"+str(k)+".fasta", "w")
		if k == 1:
			for seq in seqs:
				outf.write(seq)
			outf.close()
		else:
			random.shuffle(seqs)
			for seq in seqs:
				outf.write(seq)
			outf.close()
		
def main():

	#fixed parameters	
	beginS = 2013
	sidx_offset = 65
	
	
	endS = int(sys.argv[1])
	rawDir = sys.argv[2]
	dataDir = sys.argv[3]
	infName = rawDir+"gisaid_aligned_1217.fas"
	mifname = dataDir+"mi_"	
	
	bySeason = season_list(infName, beginS, endS)
	bySeason = add_April(bySeason, infName, endS)
	
	bySeason = remove_duplicates(bySeason)
	
	bySeason, mi = genotype_list(bySeason, endS)
	make_fasta(bySeason, endS, mi, dataDir, sidx_offset)

	
if __name__ == "__main__":
	main()

