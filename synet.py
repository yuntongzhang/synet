#!/usr/bin/env python
"""
SyNET main runner
"""

import argparse
import time

from synet.synthesis3 import Synthesizer
from synet.utils import read_all_boxes

__author__ = "Ahmed El-Hassany"
__email__ = "eahmed@ethz.ch"


def main():
    parser = argparse.ArgumentParser(description='Synthesize network config.')
    parser.add_argument("-i", required=True, dest="initial_inputs", help="Initial inputs file")
    parser.add_argument("-r", required=True, dest="fixed_outputs", help="Requirements file")
    parser.add_argument("-m", required=False, dest="mode", default='bgp', help="OSPF/BGP/Static mode")
    parser.add_argument("-u", dest="unrolling_limit", default=5, type=int,
                        help="Unrolling limit")
    args = parser.parse_args()
    with open(args.initial_inputs) as f:
        initial_inputs = f.read()
    with open(args.fixed_outputs) as f:
        fixed_outputs = f.read()
    if args.mode == 'bgp':
        BOXES_ORDER = ['ibgp01', 'ibgp02', 'ibgp03', 'ibgp04', 'ibgp05', 'ibgp06', 'ibgp07', 'ibgp08', 'ibgp09',
                       'ospf01', 'ospf02-0', 'ospf02-1', 'fwd01-0', 'fwd01-1']
    elif args.mode == 'ospf':
        BOXES_ORDER = ['ospf01', 'ospf02-0', 'ospf02-1', 'fwd01-0', 'fwd01-1']
    elif args.mode == 'static':
        BOXES_ORDER = ['fwd01-0-static', 'fwd01-1-static']
        BOXES_ORDER = ['fwd01-1-static']
    else:
        raise NameError('Unknown synthesis mode')

    start = time.time()
    boxes = {}
    all_boxes = read_all_boxes()
    for box_name in BOXES_ORDER:
        boxes[box_name] = all_boxes[box_name]
    syn = Synthesizer(boxes, BOXES_ORDER, initial_inputs, fixed_outputs,
                      unrolling_limit=args.unrolling_limit)

    syn.synthesize()
    end = time.time()
    print ("XXXXX Synthesis time for %s is %s" % (args.initial_inputs.split('/')[-1].split('.')[0], end - start))
    outdir = "configs/%s" % (args.initial_inputs.split('/')[-1].split('.')[0] + '-configs')
    print ("Generating configs to ", outdir)
    syn.gen_configs(outdir)


if __name__ == '__main__':
    main()
