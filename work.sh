perl fasta2apg.pl -i /rhome/cjinfeng/BigData/01.Rice_genomes/HEG4/00.Genome/Chromosome/HEG4_ALLPATHLG_v1.chr.fasta -o HEG4v1.0 -size 200 -name HEG4v1.0
grep "^chr" HEG4v1.0.agp > HEG4v1.0.chr.agp
grep "^super" HEG4v1.0.agp > HEG4v1.0.unmapped.agp

perl fasta2apg.pl -i /rhome/cjinfeng/BigData/01.Rice_genomes/A123/00.Genome/Chromosome/A123_ALLPATHLG_v1.chr.fasta -o A123v1.0 -size 200 -name A123v1.0
grep "^chr" A123v1.0.agp > A123v1.0.chr.agp
grep "^super" A123v1.0.agp > A123v1.0.unmapped.agp
