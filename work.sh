perl fasta2apg.pl -i /rhome/cjinfeng/BigData/01.Rice_genomes/HEG4/00.Genome/Chromosome/HEG4_ALLPATHLG_v1.chr.fasta -o HEG4v1.0 -size 200 -name HEG4v1.0
grep "^chr" HEG4v1.0.agp > HEG4v1.0.chr.agp
grep "^super" HEG4v1.0.agp > HEG4v1.0.unmapped.agp
python revision_HEG4.py
grep "^chr" HEG4v1.0.masked.agp > HEG4v1.0.masked.chr.agp
grep "^super" HEG4v1.0.masked.agp > HEG4v1.0.masked.unmapped.agp
cut -f1 HEG4v1.0.masked.unmapped.agp | uniq | sort | uniq | awk '{print $1",unknownchromosome"}' > HEG4v1.0.masked.unmapped.assignment
cut -f1 HEG4v1.0.masked.chr.agp | uniq | sort | uniq | awk '{print $1",chromosome1"}' > HEG4v1.0.masked.chr.assignment

perl fasta2apg.pl -i /rhome/cjinfeng/BigData/01.Rice_genomes/A123/00.Genome/Chromosome/A123_ALLPATHLG_v1.chr.fasta -o A123v1.0 -size 200 -name A123v1.0
grep "^chr" A123v1.0.agp > A123v1.0.chr.agp
grep "^super" A123v1.0.agp > A123v1.0.unmapped.agp
python revision_A123.py
grep "^chr" A123v1.0.masked.agp > A123v1.0.masked.chr.agp
grep "^super" A123v1.0.masked.agp > A123v1.0.masked.unmapped.agp
cut -f1 A123v1.0.masked.unmapped.agp | uniq | sort | uniq | awk '{print $1",unknownchromosome"}' > A123v1.0.masked.unmapped.assignment
cut -f1 A123v1.0.masked.chr.agp | uniq | sort | uniq | awk '{print $1",chromosome1"}' > A123v1.0.masked.chr.assignment
