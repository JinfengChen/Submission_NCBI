#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def usage():
    test="name"
    message='''
python revision.py
Remove ID and modify length in agp file manually after run this script.
Mask regions in contigs and update agp file.

    '''
    print message

def fasta_seq(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[str(record.id)] = str(record.seq)
    return fastaid

#HEG4v1.0_188	90484	23596..23653	adaptor:NGB00360.1
def readid(infile):
    data = defaultdict(lambda : list())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                pos  = re.split(r'\.\.', unit[2])
                if not data.has_key(unit[0]):
                    data[unit[0]] = [unit[1], pos[0], pos[1]]
                    #print unit[0], unit[1], pos[0], pos[1]
    return data

def readtable(infile):
    data = defaultdict(lambda : int())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[0]] = 1
    return data

def maskregion(prefix,id_mask, agp, contig, id_remove):
    ofasta= '%s.masked.contig.fa' %(prefix)
    oagp  = '%s.masked.agp' %(prefix)
    ofile = open(ofasta, 'w')
    for seqid in sorted(contig.keys()):
        #print '>%s' %(seqid)
        if id_mask.has_key(seqid):
            print seqid, id_mask[seqid][0], id_mask[seqid][1], id_mask[seqid][2]
            length = int(id_mask[seqid][2]) - int(id_mask[seqid][1])
            mask   = 'N'*length
            if int(id_mask[seqid][2]) == int(id_mask[seqid][0]):
                newseq = contig[seqid][:int(id_mask[seqid][1])]
                print 'Length changed***'
            elif int(id_mask[seqid][1]) == 0:
                print 'Length changed***'
                newseq = contig[seqid][int(id_mask[seqid][1]):]
            else:
                newseq = contig[seqid][:int(id_mask[seqid][1])] + mask + contig[seqid][int(id_mask[seqid][2]):]
            newrecord = SeqRecord(Seq(newseq), id = seqid, description='')
            SeqIO.write(newrecord, ofile, 'fasta')
            #print '>%s\n%s' %(seqid, newseq)
            print 'orignial length: %s, newlength length: %s' %(len(contig[seqid]),len(newseq))
        elif id_remove.has_key(seqid):
            continue
        else:
            newrecord = SeqRecord(Seq(contig[seqid]), id = seqid, description='')
            SeqIO.write(newrecord, ofile, 'fasta')

## Generated from SOAPdenovo assembly file /rhome/cjinfeng/BigData/01.Rice_genomes/HEG4/00.Genome/Chromosome/HEG4_ALLPATHLG_v1.chr.fasta using script fasta2apg.p
#chr01   1       33508   1       W       HEG4v1.0_1      1       33508   +
#chr01   33509   33608   2       N       100     scaffold        yes     paired-ends;align_genus
#chr01   33609   147049  3       W       HEG4v1.0_2      1       113441  +
#chr01   147050  147244  4       N       195     scaffold        yes     paired-ends;align_genus
def update_agp(prefix, infile, id_remove):
    oagp = '%s.masked.agp' %(prefix)
    ofile = open(oagp, 'w')
    lastchr = ''
    lastrank = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if line.startswith(r'#'):
                print >> ofile, line
            elif(len(line) > 2): 
                unit = re.split(r'\t',line)
                if unit[0] == lastchr and int(unit[3]) != lastrank + 1:
                    unit[3] = str(lastrank + 1)
                lastchr = unit[0]
                lastrank = int(unit[3])
                if id_remove.has_key(unit[5]):
                    continue
                elif unit[6] == 'scaffold':
                    if int(unit[5]) == 100:
                        unit[4] = 'U'
                        newline = '\t'.join(unit)
                        print >> ofile, newline
                    else:
                        unit[8] = 'paired-ends'
                        newline = '\t'.join(unit)
                        print >> ofile, newline
                else:
                    newline = '\t'.join(unit)
                    print >> ofile, newline
    ofile.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

    id_mask   = readid('Mask_ID.HEG4')
    id_remove = readtable('Remove_ID.HEG4')
    agp = 'HEG4v1.0_revision/HEG4v1.0.agp'
    contig = fasta_seq('HEG4v1.0/HEG4v1.0.contigs.fa')
    prefix = 'HEG4v1.0_revision/HEG4v1.0'
    maskregion(prefix, id_mask, agp, contig, id_remove)
    update_agp(prefix, agp, id_remove)


if __name__ == '__main__':
    main()

