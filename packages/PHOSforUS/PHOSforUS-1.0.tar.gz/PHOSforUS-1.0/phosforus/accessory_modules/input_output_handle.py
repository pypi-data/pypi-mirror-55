#!/usr/bin/env python

#### Generic module import

import datetime
import numpy
import os
import pickle
import sys

#### Module functions

def input_fileset(if_input, if_file, if_direc, if_manual):
    if_seqs = []
    if if_file == True:
        if_fname = if_input
        with open(if_fname) as seq_file:
			for line in seq_file:
				sst = line.rstrip('\n')
				if sst[0] == ">":
					if_seqs.append([sst, ""])
				else:
					if_seqs[-1][1] += sst
        if len(if_seqs) == 0:
			print "#### ERROR: No valid input was found in input directory"
			print "Please check input files"
			sys.exit()
			return -1
        else:
            print "#### Sequence input completed"
            return if_seqs

    elif if_direc == True:
        if_fnames = os.listdir(if_input)
        if_fnames.remove('.DS_Store')
        if len(if_fnames) == 0:
            print "#### ERROR: No sequence file was found in given directory"
            sys.exit()
            return -1
        else:
            for if_1 in range(len(if_fnames)):
                with open(if_input+"/"+if_fnames[if_1]) as seq_file:
                    for line in seq_file:
                        sst = line.rstrip('\n')
                        if sst[0] == ">":
                            if_seqs.append([sst, ""])
                        else:
                            if_seqs[-1][1] += sst
            if len(if_seqs) == 0:
                print "#### ERROR: No valid input was found in input directory"
                print "Please check input files"
                sys.exit()
                return -1
            else:
                print "#### Sequence input completed"
                return if_seqs

    elif if_manual == True:
        if_sub = [">Manual_seq_input", if_input.upper()]
        if_seqs.append(if_sub)
        print "#### Manual sequence input completed"
        return if_seqs

    else:
        print "#### ERROR: Sequence input failed"
        print "#### Please provide valid input option"
        sys.exit()
        return -1

def input_indices(ii_path):
    ind_label = []
    ind_list = []
    with open(ii_path+"/preset_indices/index_reselect.txt") as ind_file:
        for line in ind_file:
            ssl = line.rstrip('\n').split()
            ind_label.append(ssl[0])
            ind_list.append([float(i) for i in ssl[1:]])
    return ind_label, ind_list

def input_escape(ie_path):
    escape_label = ['dGN', 'ddGN', 'dHapN', 'ddHapN', 'dHpN', 'ddHpN', 'TdSN', 'dTdSN', 'dGD', 'ddGD', 'dHapD', 'ddHapD', 'dHpD', 'ddHpD', 'TdSD', 'dTdSD']
    escape_raw = []
    with open(ie_path+"/preset_indices/eScape_sorted_filled.csv") as ind_file:
    	for line in ind_file:
    		ssl = line.rstrip('\n').split()
    		escape_raw.append([float(i) for i in ssl[1:17]])
    return escape_label, numpy.transpose(escape_raw)

def preset_clf_import(pci_path):
    pci_param_order = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17"]
    pcx_list = []
    for pcx_1 in range(5):
        pcx_sub = []
        for pcx_2 in range(19):
            #print pcx_1, pcx_2
            if pcx_2 == 0:
                pci_clf = pickle.load(open(pci_path+"/preset_params/class_"+str(pcx_1)+"/metaparam_"+str(pcx_1)+".txt"))
                pcx_sub.append(pci_clf)
                #print str("preset_params/class_"+str(pcx_1)+"/metaparam_"+str(pcx_1)+".txt")
            else:
                pci_clf = pickle.load(open(pci_path+"/preset_params/class_"+str(pcx_1)+"/param_"+str(pcx_1)+"_"+ pci_param_order[pcx_2-1]+".txt"))
                pcx_sub.append(pci_clf)
                #print str("preset_params/class_"+str(pcx_1)+"/param_"+str(pcx_1)+"_"+ pci_param_order[pcx_2-1]+".txt")
        pcx_list.append(pcx_sub)
    return pcx_list
                

def output_formatter(of_file, of_res, of_number, of_st, of_ed):
    try:
        os.stat("result_output")
    except:
        os.mkdir("result_output")
    
	of_outfname = "result_output/phosforus_output_"+"00000"[0:(6-len(str(of_number)))]+str(of_number)+".txt"
	of_outfile = open(of_outfname, 'w')

	of_outfile.write("[PHOSforUS analysis results]")
	of_outfile.write('\n')
	of_outfile.write('\n')
	of_outfile.write("## Sequence_label: "+of_file[0])
	of_outfile.write('\n')
	of_outfile.write('\n')
	of_outfile.write("## RAW_sequence")
	of_outfile.write('\n')
	of_outfile.write('\n')

	of_slen = len(of_file[1])
	of_lno = int(numpy.ceil(float(of_slen)/60.0))
	
	for of_1 in range(of_lno):
		of_outfile.write(of_file[1][(of_1*60):min(((of_1+1)*60), of_slen)])
		of_outfile.write('\n')

	of_outfile.write('\n')
	of_outfile.write("## Mapped_phosphorylation_sites")
	of_outfile.write('\n')
	of_outfile.write('\n')

	for of_2 in range(of_lno):
		of_part = min(60, of_slen-(of_2*60))
		for of_3 in range(of_part):
			det_of = 0
			for of_4 in range(len(of_res)):
				if (of_2*60+of_3+1) == of_res[of_4][0]:
					if of_res[of_4][2] == "PHOSPHO":
						det_of += 1
			if det_of > 0:
				of_outfile.write('#')
			else:
				of_outfile.write('_')
		of_outfile.write('\n')

	of_outfile.write('\n')
	of_outfile.write("## Site_wise_details")
	of_outfile.write('\n')
	of_outfile.write('\n')
	of_outfile.write("Sites")
	of_outfile.write('\t')
	of_outfile.write("P-type")
	of_outfile.write('\t')
	of_outfile.write("Predict")
	of_outfile.write('\t')
	of_outfile.write("Log_score")
	of_outfile.write('\t')
	of_outfile.write("Phos_prob")
	of_outfile.write('\n')

	for of_5 in range(len(of_res)):
		of_outfile.write(str(of_res[of_5][0]))
		of_outfile.write('\t')
		of_outfile.write(str(of_res[of_5][1]))
		of_outfile.write('\t')
		of_outfile.write(str(of_res[of_5][2]))
		of_outfile.write('\t')
		of_outfile.write(str(of_res[of_5][3]))
		of_outfile.write('\t')
		of_outfile.write(str(of_res[of_5][4]))
		of_outfile.write('\n')

	of_outfile.write('\n')
	of_outfile.write("## Start_time: "+str(of_st)[8:])
	of_outfile.write('\n')
	of_outfile.write("## End_time: "+str(of_ed)[8:])
	of_outfile.write('\n')
	of_outfile.write("## Time_rapsed: "+str(of_ed-of_st))
	of_outfile.write('\n')

	of_outfile.close()

####
