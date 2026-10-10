"""Issue 5: the VCF step of meth_phaser_post_processing (0.0.4 with the local patches), as in
its main(), without the BAM step. Same arguments as meth_phaser_post_processing."""
import sys
from importlib.machinery import SourceFileLoader
mp = SourceFileLoader('mpp', '/disk/software/methphaser/meth_phaser_post_processing').load_module()
args = mp.parse_arg(sys.argv[1:])
if args.high_success_rate_param:
    dfs = mp.get_block_relationships(args.meth_phasing_input_folder, min_required_read=0, min_diff_perc=0)
else:
    dfs = mp.get_block_relationships(args.meth_phasing_input_folder, min_required_read=args.minimum_coverage,
                                     min_diff_perc=args.voting_difference)
mp.get_altered_vcf(args.vcf_called, args.output_vcf, dfs)
