#!/usr/bin/env python
# File created on 08 Nov 2009.
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Greg Caporaso", "Dan Knights"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from qiime.util import make_option
from qiime.pick_otus import map_otu_map_files
from qiime.format import write_otu_map
from qiime.util import parse_command_line_parameters

script_info={}
script_info['brief_description']="""Merge OTU mapping files"""
script_info['script_description']="""This script merges OTU mapping files generated by denoise_wrapper.py and/or pick_otus.py

For example, if otu_map1.txt contains:

=   ====    ====    ====
0   seq1    seq2    seq5
1   seq3    seq4    
2   seq6    seq7    seq8
=   ====    ====    ====

and otu_map2.txt contains:

=== =   =
110 0   2
221 1
=== =   =

The resulting OTU map will be:

=== ====    ====    ====    ====    ====    ====
110 seq1    seq2    seq5    seq6    seq7    seq8
221 seq3    seq4
=== ====    ====    ====    ====    ====    ====
"""
script_info['script_usage']=[]
script_info['script_usage'].append(("""Expand an OTU map:""","""If the seq_ids in otu_map2.txt are otu_ids in otu_map1.txt, expand the seq_ids in otu_map2.txt to be the full list of associated seq_ids from otu_map1.txt. Write the resulting otu map to otu_map.txt (-o).""","""merge_otu_maps.py -i otu_map1.txt,otu_map2.txt -o otu_map.txt"""))

script_info['script_usage'].append(("""Expand a failures file:""",""" Some OTU pickers (e.g. uclust_ref) will generate a list of failures for sequences which could not be assigned to OTUs. If this occurs in a chained OTU picking process, the failures file will need to be expanded to include the orignal sequence ids. To do this, pass the failures file via -f, and the otu maps up to, but not including, the step that generated the failures file. ""","""merge_otu_maps.py -i otu_map1.txt,otu_map2.txt -f fail.txt -o all_failures.txt"""))

script_info['output_description']="""The result of this script is an OTU mapping file."""
script_info['required_options']=[
    make_option('-i','--otu_map_fps',type='existing_filepaths',
                    help=('the otu map filepaths, comma-separated and '
                    'ordered as the OTU pickers were run [REQUIRED]')),
    make_option('-o','--output_fp', type='new_filepath',
                help='path to write output OTU map [REQUIRED]')
]

script_info['optional_options']=[
    make_option('-f','--failures_fp',type='existing_filepath',
                help='failures filepath, if applicable')
]

script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    otu_files = map(open,opts.otu_map_fps)
    failures_fp = opts.failures_fp
    output_fp = opts.output_fp
    if failures_fp:
        failures_f = open(failures_fp,'U')
    else:
        failures_f = None
    
    try:
        result = map_otu_map_files(otu_files,failures_file=failures_f)
    except KeyError,e:
        print ('Some keys do not map ('+ str(e) +') -- is the order of'
        ' your OTU maps equivalent to the order in which the OTU pickers'
        ' were run? If expanding a failures file, did you remember to leave'
        ' out the otu map from the run which generated the failures file?')
        exit(1)
    
    if failures_fp != None:
        of = open(output_fp,'w')
        of.write('\n'.join(result))
        of.close()
    else:
        write_otu_map(result.items(),output_fp)

    
if __name__ == "__main__":
    main()
