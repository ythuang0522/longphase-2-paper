ROOT=/disk/software/dipcall.kit
N_THREADS=16
MAPPER=minimap2
MM2_IDX=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa
MM2_OPT=-xasm5 --cs -t$(N_THREADS)
REF_FA=/disk/research/GCA_000001405.15_GRCh38_no_alt_analysis_set.fa

all:HG008N_v6.3_GRCh38.dip.bed HG008N_v6.3_GRCh38.dip.vcf.gz

HG008N_v6.3_GRCh38.hap1.paf.gz:../asm/HG008N_v6.3_hap1.fasta.gz
	$(ROOT)/$(MAPPER) -c --paf-no-hit $(MM2_OPT) $(MM2_IDX) $< 2> $@.log | gzip > $@
HG008N_v6.3_GRCh38.hap2.paf.gz:../asm/HG008N_v6.3_hap2.fasta.gz
	$(ROOT)/$(MAPPER) -c --paf-no-hit $(MM2_OPT) $(MM2_IDX) $< 2> $@.log | gzip > $@

HG008N_v6.3_GRCh38.hap1.sam.gz:../asm/HG008N_v6.3_hap1.fasta.gz
	$(ROOT)/$(MAPPER) -a $(MM2_OPT) $(MM2_IDX) $< 2> $@.log | gzip > $@
HG008N_v6.3_GRCh38.hap2.sam.gz:../asm/HG008N_v6.3_hap2.fasta.gz
	$(ROOT)/$(MAPPER) -a $(MM2_OPT) $(MM2_IDX) $< 2> $@.log | gzip > $@

HG008N_v6.3_GRCh38.hap1.bam:HG008N_v6.3_GRCh38.hap1.sam.gz
	$(ROOT)/k8 $(ROOT)/dipcall-aux.js samflt $< | $(ROOT)/samtools sort -m4G --threads 4 -o $@ -
HG008N_v6.3_GRCh38.hap2.bam:HG008N_v6.3_GRCh38.hap2.sam.gz
	$(ROOT)/k8 $(ROOT)/dipcall-aux.js samflt $< | $(ROOT)/samtools sort -m4G --threads 4 -o $@ -

HG008N_v6.3_GRCh38.pair.vcf.gz:HG008N_v6.3_GRCh38.hap1.bam HG008N_v6.3_GRCh38.hap2.bam
	$(ROOT)/htsbox pileup -q5 -evcf $(REF_FA) $^ | $(ROOT)/htsbox bgzip > $@
HG008N_v6.3_GRCh38.dip.vcf.gz:HG008N_v6.3_GRCh38.pair.vcf.gz
	$(ROOT)/k8 $(ROOT)/dipcall-aux.js vcfpair  $< | $(ROOT)/htsbox bgzip > $@

HG008N_v6.3_GRCh38.hap1.var.gz:HG008N_v6.3_GRCh38.hap1.paf.gz
	gzip -dc $< | sort -k6,6 -k8,8n | $(ROOT)/k8 $(ROOT)/paftools.js call - 2> $@.vst | gzip > $@
HG008N_v6.3_GRCh38.hap2.var.gz:HG008N_v6.3_GRCh38.hap2.paf.gz
	gzip -dc $< | sort -k6,6 -k8,8n | $(ROOT)/k8 $(ROOT)/paftools.js call - 2> $@.vst | gzip > $@
HG008N_v6.3_GRCh38.hap1.bed:HG008N_v6.3_GRCh38.hap1.var.gz
	gzip -dc $< | grep ^R | cut -f2- > $@
HG008N_v6.3_GRCh38.hap2.bed:HG008N_v6.3_GRCh38.hap2.var.gz
	gzip -dc $< | grep ^R | cut -f2- > $@
HG008N_v6.3_GRCh38.dip.bed:HG008N_v6.3_GRCh38.hap1.bed HG008N_v6.3_GRCh38.hap2.bed
	$(ROOT)/bedtk isec -m $^ > $@
