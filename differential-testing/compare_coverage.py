#!/usr/bin/env python3

import argparse
import json
import os
from matplotlib import pyplot as plt
from matplotlib_venn import venn3

parser = argparse.ArgumentParser(description="Compare code coverage files.")


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


parser.add_argument("coverage_files", type=file_path, action="store", nargs="+")
parser.add_argument("--output-file", default="coverage.png", action="store")

def covert_to_file_to_coverage_map(coverage_list):
    mapping = {}
    for file in coverage_list:
        file_name = file["file"]
        file.pop("file")
        mapping[file_name] = file
    return mapping


def coverage_to_set(coverage_list):
    file_to_coverage_mapping = covert_to_file_to_coverage_map(coverage_list)
    line_coverage_set = set()
    for file_name in file_to_coverage_mapping:
        coverage_info = file_to_coverage_mapping[file_name]
        lines = coverage_info["lines"]
        for line in lines["details"]:
            if line["hit"] > 0:
                line_coverage_set.add(f"{line['line']}-{file_name}")
    return line_coverage_set


if __name__ == "__main__":
    args = parser.parse_args()

    coverage_files = args.coverage_files
    labels = []
    sets = []
    for coverage_file in coverage_files:
        with open(coverage_file, "r") as f:
            coverage = json.load(f)

        coverage_set = coverage_to_set(coverage)

        labels.append(os.path.basename(coverage_file).split(".json")[0])
        sets.append(coverage_set)

    venn = venn3(sets, set_labels=tuple(labels))
    plt.show()

