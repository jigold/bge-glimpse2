import argparse
import json
from argparse import Namespace


def populate_inputs(path: str, args: dict):
    inputs = json.dumps(args, indent=4)
    with open(path, 'w') as f:
        f.write(inputs + '\n')


def split_reference_inputs(args: Namespace) -> dict:
    renamed_args = {}
    for arg, val in args.items():
        renamed_arg = f'Glimpse2SplitReference.{arg}'
        renamed_args[renamed_arg] = val
    return renamed_args


def main(split_reference_path: str,
         split_reference_args: Namespace):
    split_reference_args = split_reference_inputs(split_reference_args)
    populate_inputs(split_reference_path, split_reference_args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    split_reference = subparsers.add_parser("split-reference")
    split_reference.add_argument('--output', type=str, required=True)

    split_reference.add_argument("--regions-file", type=str, required=True)
    split_reference.add_argument("--region", type=str, required=False)

    split_reference.add_argument('--seed', type=int, default=3242342)
    split_reference.add_argument("--min-window-cm", type=int, required=False)
    split_reference.add_argument("--uniform-number-of-variants", action="store_true", default=False)
    split_reference.add_argument("--drop-monomorphic-ref-sites", action="store_true", default=False)

    split_reference.add_argument("--preemptible", type=int, default=1)
    split_reference.add_argument("--docker", type=str, required=True)
    split_reference.add_argument("--monitoring-script", type=str)

    split_reference_args, _ = split_reference.parse_known_args()
    split_reference_args = vars(split_reference_args)

    regions_file = split_reference_args.pop('regions_file')
    contig_regions = []
    reference_panel_filenames = []
    genetic_map_filenames = []

    with open(regions_file, 'r') as f:
        f.readline()
        for line in f:
            line = line.rstrip()
            region, reference_filename, genetic_map_filename = line.split('\t')
            contig_regions.append(region)
            reference_panel_filenames.append(reference_filename)
            genetic_map_filenames.append(genetic_map_filename)

    region = split_reference_args['region']
    if region is not None:
        idx = contig_regions.index(region)
        if idx != -1:
            contig_regions = [region]
            reference_panel_filenames = [reference_panel_filenames[idx]]
            genetic_map_filenames = [genetic_map_filenames[idx]]

    split_reference_args['contig_regions'] = contig_regions
    split_reference_args['reference_panel_filenames'] = reference_panel_filenames
    split_reference_args['genetic_map_filenames'] = genetic_map_filenames

    empty_args = []
    for name, arg in split_reference_args.items():
        if arg is None:
            empty_args.append(name)
    for name in empty_args:
        split_reference_args.pop(name)

    split_reference_path = split_reference_args.pop('output')
    main(split_reference_path, split_reference_args)

