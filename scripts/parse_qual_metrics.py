# Authors: Tessa Pierce, Nolan Hartwick
# script containing file parsers for results of assessment tools

#NOTE: relies on "run_busco_DBName" naming system for busco directories

import os, glob, fnmatch, re, argparse
# use fadapa to parse FastQC metrics
from fadapa import Fadapa

def cegma_parser(cegmaDir, filename):
    '''	CEGMA PARSER
	Extracts the percent complete and the percent partial from an opened file rf.
    '''
    cegmaF = glob.glob(os.path.join(cegmaDir, filename))
    cegmaInfo = {}
    if len(cegmaF) <1:
        cegmaInfo['cegma'] = 'no cegma information'
    else:
    	with open(cegmaF[0], 'r') as f: 
	    read_report = f.read()
	    cegmaInfo['cegma_%_complete'] = re.search('Complete\s+[0-9]+\s+.*?\s',read_report).group(0).split()[-1]
	    cegmaInfo['cegma_%_partial'] = re.search('Partial\s+[0-9]+\s+.*?\s',read_report).group(0).split()[-1]
    return cegmaInfo


def busco_parser(buscoDir, filename):
    ''' BUSCO PARSER
        Extracts info from BUSCO's "short_summary_busco_DBNAME" file
        C:94%[D:40%],F:1.8%,M:3.5%,n:843o
    '''
    buscoDB = "busco_" + buscoDir.rsplit('_', 1)[1] # grab DBNAME
    buscoF = glob.glob(os.path.join(buscoDir, filename))
    buscoInfo = {}
    if len(buscoF) <1:
        buscoInfo[buscoDB] = 'no busco information from ' + buscoDB
    else:
	with open(buscoF[0], 'r') as f:
            read_report = f.read()
            info = re.search('C:(\d+\.?\d*)%\[D:(\d+\.?\d*)%\],F:(\d+\.?\d*)%,M:(\d+\.?\d*)%,n:(\d*)',read_report).groups()
            buscoInfo[buscoDB + '_%_complete'] = info[0]
            buscoInfo[buscoDB + '_%_duplicated'] = info[1]
            buscoInfo[buscoDB + '_%_fragmented'] = info[2]
            buscoInfo[buscoDB + '_%_missing'] = info[3]
            buscoInfo[buscoDB + '_number_searched'] = info[4]
    return buscoInfo

def detonate_parser(detonateDir, filename):
    '''	DETONATE PARSER
	Extracts the score from the DETONATE .score file
    '''
    detonateD = {}
    detonateF = glob.glob(os.path.join(detonateDir, filename))
    if len(detonateF) <1:
        detonateD['detonate'] = 'no detonate information'
    else:
	with open(detonateF[0], 'r') as f:
            read_score = f.read()
	    detonateD['detonate'] = re.search('Score\t[-+]?\d*\.\d+|\d+',read_score).group(0).split()[-1]
    return detonateD

def transrate_parser(transrateDir, filename):
    '''TRANSRATE PARSER
	Extracts relevant info from the transrate assemblies.csv file
	#this csv will be two lines long: first, headers, then values
    '''
    transrateInfo = {} 
    transrateF = glob.glob(os.path.join(transrateDir, filename))
    if len(transrateF) <1:
        transrateInfo['transrate'] = 'no transrate information'
    else:
	with open(transrateF[0], 'r') as f: 
	    headers = f.readline().rstrip().split(',')
	    values = f.readline().rstrip().split(',')
	    transrateInfo = dict(zip(headers, values))
    return transrateInfo


def transrate_readcount_parser(transrateRCDir, filename):
    '''TRANSRATE PARSER 
    Extracts relevant info from the transrate assemblies.csv file
    '''
    readCount = {}
    transrateRCF = glob.glob(os.path.join(transrateRCDir, filename))
    if len(transrateRCF) <1:
        readCount['Transrate_readCount'] = 'no transrate readCount information'
    else:
        with open(transrateRCF[0], 'r') as f: 
            readCount['Transrate_readCount'] = f.readline().rstrip()
    return readCount


def fastqc_parser(fastqcDir, filename):
    '''FASTQC PARSER
    Extracts info from fastqc output files --> currently uses FADAPA parser
    '''
    fastqcD = {}
    fastqcF = sorted(glob.glob(os.path.join(fastqcDir, "*_fastqc", filename)))
    #use fnmatch to handle paired vs unpaired:
    fastqc1 = fnmatch.filter(fastqcF, '*_1_*') 
    fastqc2 = fnmatch.filter(fastqcF, '*_2_*')
    fastqcU = [x for x in fastqcF if x not in set(fastqc1 + fastqc2)]
    if len(fastqcF) <1: #no files (just in case)
	fastqcD['fastqc'] = 'no fastqc information'
    else:
        for fq1 in fastqc1: #paired files 
	    fq2 = f.replace('_1_', '_2_') # don't use fastqc2 list to prevent any order f-ups
	    with Fadapa(fq1) as f_1:
		basicStats1 = f_1.clean_data('Basic Statistics')
	        fName = basicStats1[1][1].rsplit('_1')[0]
		numSeqsD1 = basicStats1[4][1]
                seqLenD1 = f_1.clean_data('Sequence Length Distribution')  
                #fastqcD['%GC'] = basicStats[7][1]
		with Fadapa(fq2) as f_2:
		    basicStats2 = f_2.clean_data('Basic Statistics')
                    seqLenD2 = f_2.clean_data('Sequence Length Distribution')  
		    numSeqsD2 = basicStats2[4][1]
		    fastqcD[fName] = [numSeqsD1, seqLenD1, numSeqsD2, SeqLenD2] 
	for unp in fastqcU: #unpaired files 
	    with Fadapa(unp) as f:
	        basicStats = f.clean_data('Basic Statistics')
	        fName = basicStats[1][1].rsplit('.fa')[0] 
		numSeqs= basicStats[4][1]
		#seqLenRange= basicStats[6]#[1]
		#percGC= basicStats[7]#[1]
		seqLenD = f.clean_data('Sequence Length Distribution')  
		fastqcD[fName] = [numSeqs, seqLenD] 
    return fastqcD






