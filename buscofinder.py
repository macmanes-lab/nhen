#!/usr/bin/env python3
import argparse
import os
#retreive user arguments 
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--score", help = "type of busco score", default = "M")
parser.add_argument("-m", "--max_score", help = "max acceptible score", default = 10, type = float)
args = parser.parse_args()
#make empty string that will hold final names and scores
fin_string = ""
#iterate through each file in directory
for file in os.scandir("/mnt/lustre/macmaneslab/nah1004/transcriptomes/reports"):
	if file.name.startswith("qual"):
		if file.name.endswith("v2"):
#iterate through file to find desired scores
			try:
				with open( file, "r") as in_handle:
					line = in_handle.readline()
					line = line.strip()
					bad_list = line.split()
					wanted_item = bad_list[-1].replace("[", ",")
					wanted_item = wanted_item.replace("]","")
					scores_list = wanted_item.split(",")
					scores_dict = {}
#obtain only items from list that will be necessary for pertaining score and its name
					for scores in scores_list:
						element = scores.split(":")
						ID = element[0]
						score = float(element[1].strip("%"))
						scores_dict[ID]=score
					arguments = scores_dict[args.score]
					new_name = file.name.replace("qualreport.", "").replace("_v2", "")
#only look for scores that are either above or below a particular threshold, given by user
					print("T1: {}".format(scores_dict[args.score]))
					if args.score in "CDS":
						if scores_dict[args.score] > args.max_score:
							fin_string += "{}\t{}\n".format(new_name, arguments)
					else:
						if scores_dict[args.score] < args.max_score:
							fin_string += "{}\t{}\n".format(new_name, arguments)		
			except IOError as err:
				print(err)
print(fin_string)
#write parsed through information to new file
try:
	with open ("names_scores.txt", "w") as in_handle:
		in_handle.write(fin_string)
except IOError as err:
	print ( err )

