
from Bio import SeqIO
import csv

def get_region_from_metafile(metafName, loc_sep):
	region_dict = dict()
	
	metaf = open(metafName, "rU")
	meta_csv = csv.DictReader(metaf)
	for data in meta_csv:
		id = data['Isolate_Id']
		region = data['Location'].split(loc_sep)[0]
		region_dict[id] = region
		
	return region_dict

def gisaid_to_ncbi(infName, gisaid_sep, date_sep, region_dict):
	#ncbi format : >id|name|date|region_sep_underbar|4_(HA)
	
	inf = open(infName, "rU")	
	fasta_obj = list(SeqIO.parse(inf, "fasta"))
	
	ncbi_seqs = []
	
	for sample in fasta_obj:
		each = sample.id.split(gisaid_sep)
		id = str(each[0])
		name = str(each[1])
		ymd = each[2].split(date_sep)
		date = str("/".join(ymd))
		try:
			region = region_dict[id]
		except KeyError:
			print (id)
			continue
			
		head = ">"+id+"|"+name+"|"+date+"|"+region+"|4_(HA)\n"
		seq = str(sample.seq) + "\n"
		
		ncbi_seqs.append(head+seq)

	return ncbi_seqs