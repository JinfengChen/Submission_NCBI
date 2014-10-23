echo "create project in sra website and organize the reads by experiment and sample"

echo "ssh to m05 node"
ssh m05
cd /scratch/Rice

echo "copy fastq to Rice, compress and md5sum"
rsync --progress -a -L /rhome/cjinfeng/Rice/RIL/Illumina/HEG4_P_0/HEG4_P_ATCACG_FC193L6_p2.fq ./
/opt/pigz/2.2.5/bin/pigz HEG4_P_ATCACG_FC193L6_p2.fq
md5sum HEG4_P_ATCACG_FC193L6_p2.fq.gz >> md5sum.list

echo "login to ftp and upload file"
lftp sra@ftp-private.ncbi.nih.gov
mput HEG4_P_ATCACG_FC193L6_p*.fq

