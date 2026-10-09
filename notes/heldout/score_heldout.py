"""score_phase.py of notes/benchmark_strata (issue #1) restricted to the GNN
held-out chromosomes chr17, chr21 and chr22.
    python3 score_heldout.py TRUTH.vcf QUERY.vcf OUT_PREFIX"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'benchmark_strata'))
sys.path.insert(0, '/ssd/longphase_process/benchmark_strata')
import score_phase as sp
sp.CHROMS = ['chr17', 'chr21', 'chr22']
sp.init_beds()
sp.run(sp.load_vcf(sys.argv[1]), sys.argv[2], sys.argv[3])
