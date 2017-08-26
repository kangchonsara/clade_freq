#from tab deliminated *_loc_date_age.txt files, make a better raw file for further analysis

import os
monthDict ={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7,
			"Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
directory = os.path.normpath("C:/Age/ageDist/ageDist_season_region/data/")

beginY = 2012
endY = 2017

def seasonIdx(date):
	#season for northern hemisphere: Oct ~ Sep
	
	ymd = date.split("-")
	if len(ymd) < 2: #No month information
		return -1
	try: # date looks like 2010-09-03
		y = int(ymd[0])
		m = int(ymd[1])
	except ValueError: #date looks like Sep-09
		y = int(ymd[1]) + 2000
		m = monthDict[ymd[0]]
		
	if y == beginY and m<=9:
		return -1			

	if m >= 10: 
		idx = y - beginY
	else: 
		idx = y - beginY - 1

	return idx
	
def bySeason(year):
	inf = open(directory + "\\" + str(year) + "_loc_date_age.txt", "r")
	rawData = []
	for line in inf:
		if line.find("Host_Age") >= 0: 
			each = line.split("\t")
			col_id = each.index("HA Segment_Id")
			col_date = each.index("Collection_Date")
			col_age = each.index("Host_Age")
			col_loc = each.index("Location")
		else:
			each = line.split("\t")		
			#get age
			if each[col_age] != '':
				age = int(each[col_age])
				if each[col_age+1] == "M":
					age = int(age/12)
			else:
				continue
				
			#get id, location
			id = each[col_id]
			loc = each[col_loc]
			
			#get date info
			date = each[col_date]
			ymd = date.split("-")

			if len(ymd) < 2: #No month information
				print (year, date)
				return -1
			try: # date looks like 2010-09-03
				y = int(ymd[0])
				m = int(ymd[1])
				date = date
			except ValueError: 
				#date looks like Sep-09 without day info
				#day info is filled as 15th
				y = int(ymd[1]) + 2000
				m = monthDict[ymd[0]]
				d = '15'
				date = str(y) + "-" + str(m) + "-" + d
	
			rawData.append((id, str(age), loc, date))
	inf.close()
	return rawData
	
outf = open(directory+"//"+"rawFile_for_further_analysis.csv", "w")
outf.write("id,age,location,collection_date\n")
for i in range(beginY, endY+1):
	rawData = bySeason(i)
	for d in rawData:
		outf.write(",".join(d) + "\n")
outf.close()
