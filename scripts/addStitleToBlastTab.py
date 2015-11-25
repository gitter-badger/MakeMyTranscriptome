import sys, argparse

parser = argparse.ArgumentParser()

parser.add_argument('--db2Name', help='tab-separated database lookup: full name file for reference (eg nr or swissprot)')
parser.add_argument('-b','--blast', help='blast input file')

args = parser.parse_args()

blastOrder = []
blastD = {}
with open(args.blast, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
        blastOrder.append(line[1])
        blastD[line[1]] = line


#potentially huge file --> don't want this in memory
with open(args.db2Name, 'r') as f:
    for line in f:
        line = line.rstrip().split('\t')
    hitInfo = blastD.get(line[0], None)
    if hitInfo is not None:
        hitInfo.extend(line[1:])
    f.close()

for hit in blastOrder:
    print('\t'.join(map(str,blastD[hit])) + '\n')




