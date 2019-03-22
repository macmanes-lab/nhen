#!/usr/bin/env python3
import argparse
from Bio import SeqIO
import random
#create user agruments
parser = argparse.ArgumentParser()
parser.add_argument("--percentage","-p", help= "quantity of reads are being altered", type= float)
parser.add_argument("--function", "-f", help= "function that will cause alteration", choices = ["chimeric", "redundancy", "fragmentation", "incompleteness", "local_misassembly"])
parser.add_argument("--seq_file", "-s", help= "this is sequence file that you are manipulating")
parser.add_argument("--new_file", "-n", help= "this will be the name of the file that holds your altered reads")
args = parser.parse_args()

#this function will place segments of random sequences to other sequences
def chimeric(collection,seq_file, num_seq):
	fin_list = []
	try:
	    	with open(seq_file, "rU") as in_handle:
        	        for seq_record in SeqIO.parse(in_handle, "fasta"):
                	        seq_list.append(str(seq_record.seq))
                	random_coll = random.sample(seq_list, num_seq)
	except IOError as err:
		print(err)
	print(collection)
	print(random_coll)
	for pos in range(len(collection)):
		fin_list.append(collection[pos] + random_coll[pos])
	return(fin_list)	
#this function will make a copy of a random set of collections
def redundancy(collection):
	seq_list = []
	for sequence in collection:
		new_seq = sequence *2
		seq_list.append(new_seq)
	return (seq_list)
#this function will randomly make new sequences out of given orginial sequences
def fragmentation(collection):
	new_list = []
	for sequence in collection:
		length = len(sequence)
		rand_start = random.randint(0,15)
		rand_stop = random.randint(16,length)
		new_seq = sequence[rand_start:rand_stop]
		new_list.append(new_seq)
		removed_seq= sequence.replace(new_seq, "")
		new_list.append(removed_seq)
	return (new_list)
#this function will cut out random sections
def incompleteness (collection):
	newly_cut = []
	for sequence in collection:
		print("current sequence is {}".format(sequence))
		length = len(sequence) -1
		end_slice_num = random.randint(1,length)
		print(end_slice_num)
		removed_seq = sequence[:end_slice_num]
		print(removed_seq)
		newly_cut.append(removed_seq)
	return (newly_cut)
#this function will mix up the midsections of sequences
def local_misassembly(collection):
	newly_shuffed = []
	for sequence in collection:
		print(sequence)
		length = len(sequence)
		new_seq = "".join(random.sample(sequence, length))
		print(new_seq)
		newly_shuffed.append(new_seq)
	return (newly_shuffed)



#read in chosen files, inact function
transcriptome_list = []
seq_list = []
try:
	with open(args.seq_file, "rU") as in_handle:
		for seq_record in SeqIO.parse(in_handle, "fasta"):
			seq_list.append(str(seq_record.seq))
		num_seq = int(len(seq_list) * args.percentage) 
		print(num_seq)
		random_coll = random.sample(seq_list, num_seq)	
		if args.function == "redundancy":
			line = redundancy(random_coll)
		if args.function == "chimeric":
			line = chimeric(random_coll,args.seq_file, num_seq)
		if args.function == "fragmentation":
			line = fragmentation(random_coll)
		if args.function == "incompleteness":
			line = incompleteness(random_coll)
		if args.function == "local_misassembly":
			line = local_misassembly(random_coll)
		transcriptome_list.append(line)
		for item in transcriptome_list:
			print(item)
except IOError as err:
	print(err)
#place outcome in new file
#try:
#	with open(args.new_file, "w") as out_handle:
#		SeqIO.write(transcriptome, out_handle, "fasta")
#except IOError as err:
#	print(err)
