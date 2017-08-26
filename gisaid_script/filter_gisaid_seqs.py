from Bio.Seq import Seq
from Bio import SeqIO
import os
import csv
import gisaid_to_ncbi_list

	
def put_seqs_by_month(seqs, beginM, endM):

	seqs_byMonth = [ [] for i in range(beginM, endM)) ]
	
	for sample in seqs:
		head = sample.split("\n")[0]
		ymd = head.split("|")[2].split("/")
		month = int(ymd[1])
		seqs_by_month[month-1].append(sample)
		
	
		
#parameters
infName = os.path.normpath("../gisaid/gisaid_seqs_170101-170825_aligned_AA.fas")
metafName = os.path.normpath("../gisaid_meta_files/gisaid_meta_170101-170825_cut.csv")

gisaid_sep = "_|_"
loc_sep = " / "
date_sep = "-"
use_seg_id = False

#clean up sequences
region_dict = gisaid_to_ncbi_list.get_region_from_metafile(metafName, loc_sep)
seqs = gisaid_to_ncbi_list.gisaid_to_ncbi(infName, gisaid_sep, region_dict)

seqs_byMonth = put_seqs_by_month(seqs)




