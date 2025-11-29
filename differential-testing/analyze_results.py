import argparse
import json
import random
from pathlib import Path


parser = argparse.ArgumentParser(
    description="Count the amount of discrepancies for a particular model."
)


parser.add_argument("target_dir", type=lambda x: Path(x).absolute())

parser.add_argument("--logs-dir", type=lambda x: Path(x).absolute(), required=False)
parser.add_argument(
    "--match-data", type=lambda x: Path(x).absolute(), required=False, default=None
)
parser.add_argument("--ignore-map", type=lambda x: Path(x).absolute(), required=False, default=None)
parser.add_argument("--include-map", type=lambda x: Path(x).absolute(), required=False, default=None)
parser.add_argument("--unique", action="store_true")
parser.add_argument("--library-successes", type=int, required=False, default=None)
parser.add_argument("--filter-non-discrepancies", action="store_true")
parser.add_argument("--limit", type=int, required=False, default=None)
parser.add_argument("--shuffle", action="store_true")


extra_options = parser.add_mutually_exclusive_group(required=False)
extra_options.add_argument("--print-count", action="store_true")
extra_options.add_argument("--print-paths", action="store_true")
extra_options.add_argument("--print-outcomes", action="store_true")
extra_options.add_argument("--print-successful-library-map", action="store_true")
extra_options.add_argument("--print-certs", action="store_true")


def count_successful_libraries(data):
    return list(data.values()).count(0)


def shuffled(list):
    copied = list.copy()
    random.shuffle(copied)
    return copied


def remap_outputs(path_to_data):
    return {key: 0 if value == 0 else -1 for key, value in path_to_data.items()}


def calculate_successful_libraries_to_count_map(outcomes):
    successful_libraries_to_count = {}
    for path, data in outcomes.items():
        count = count_successful_libraries(data)
        successful_libraries_to_count[count] = (
            successful_libraries_to_count.get(count, 0) + 1
        )
    return successful_libraries_to_count


def has_discrepancy(data):
    return any([exit_code == 0 for exit_code in data.values()]) and any(
        [exit_code != 0 for exit_code in data.values()]
    )


def find_unique_outcomes(files, only_discrepancies):
    seen = set()
    outcomes = []
    for path in files:
        with path.open() as f:
            remapped_outputs = remap_outputs(json.load(f))
            data = frozenset(remapped_outputs.items())

        if data not in seen and (
            not only_discrepancies
            or only_discrepancies
            and has_discrepancy(remapped_outputs)
        ):
            seen.add(data)
            outcomes.append((path, dict(data)))

    return {key: dict(sorted(value.items())) for key, value in outcomes}


def find_all_outcomes(files, only_discrepancies):
    outcomes = {}
    for path in files:
        with path.open() as f:
            data = remap_outputs(json.load(f))
        if not only_discrepancies or only_discrepancies and has_discrepancy(data):
            outcomes[path] = dict(sorted(data.items()))
    return outcomes


def find_all_matching_outcomes(files, expected_data):
    outcomes = {}
    for path in files:
        with path.open() as f:
            data = remap_outputs(json.load(f))
            if data == expected_data:
                outcomes[path] = dict(sorted(data.items()))
    return outcomes


def order_and_trim_data(outcomes, logs_dir, limit, shuffle_data, ignore_map, include_map):
    filtered = ignore_outcomes_containing(outcomes, logs_dir, ignore_map)
    filtered = include_outcomes_containing(filtered, logs_dir, include_map)

    as_list = list(filtered.items())

    as_list = shuffled(as_list) if shuffle_data else sorted(as_list)

    if limit:
        outcomes = dict(as_list[0:limit])
    else:
        outcomes = dict(as_list)


    return outcomes

def ignore_outcomes_containing(outcomes, logs_dir, ignore_map):
    if ignore_map is not None and logs_dir is not None:

        with ignore_map.open() as f:
            library_to_ignore_in_logs = {key.lower(): value for key, value in json.load(f).items()}

        new_outcomes = {}

        for path, data in outcomes.items():
            log_files = {}
            for library, ignore_strings in library_to_ignore_in_logs.items():
                pem_file = path.stem
                log_files[logs_dir / (pem_file + "-" + library + ".log")] = ignore_strings

            include = True
            for log_file, ignore_strings in log_files.items():
                with log_file.open("rb") as f:
                    text = f.read()

                if any([ignore_string.encode() in text for ignore_string in ignore_strings]):
                    include = False
                    break

            if include:
                new_outcomes[path] = data

        return new_outcomes

    else:
        return outcomes


def include_outcomes_containing(outcomes, logs_dir, include_map):
    if include_map is not None and logs_dir is not None:

        with include_map.open() as f:
            library_to_include_in_logs = {key.lower(): value for key, value in json.load(f).items()}

        new_outcomes = {}

        for path, data in outcomes.items():
            log_files = {}
            for library, include_strings in library_to_include_in_logs.items():
                pem_file = path.stem
                log_files[logs_dir / (pem_file + "-" + library + ".log")] = include_strings

            include = False
            for log_file, ignore_strings in log_files.items():
                with log_file.open("rb") as f:
                    text = f.read()

                if all([ignore_string.encode() in text for ignore_string in ignore_strings]):
                    include = True
                    break

            if include:
                new_outcomes[path] = data

        return new_outcomes

    else:
        return outcomes


def calculate_outcomes(
    files,
    logs_dir=None,
    shuffle_data=False,
    unique=False,
    filter_non_discrepancies=False,
    library_successes=None,
    limit=None,
    match_data=None,
    ignore_map=None,
    include_map=None
):
    if match_data:

        with match_data.open() as f:
            expected_data = remap_outputs(json.load(f))

        outcomes = find_all_matching_outcomes(files, expected_data)
    else:
        outcomes = (
            find_unique_outcomes(files, filter_non_discrepancies)
            if unique
            else find_all_outcomes(files, filter_non_discrepancies)
        )

        if library_successes:
            outcomes = {
                path: data
                for path, data in outcomes.items()
                if count_successful_libraries(data) == library_successes
            }

    return order_and_trim_data(outcomes, logs_dir, limit, shuffle_data, ignore_map, include_map)


if __name__ == "__main__":
    args = parser.parse_args()
    files = args.target_dir.glob("*.json")
    if ((args.logs_dir is None) ^ (args.ignore_map is None)) and ((args.logs_dir is None) ^ (args.include_map is None)):
        parser.error("mappings and logs dir must be included together.")

    outcomes = calculate_outcomes(
        files,
        args.logs_dir,
        args.shuffle,
        args.unique,
        args.filter_non_discrepancies,
        args.library_successes,
        args.limit,
        args.match_data,
        args.ignore_map,
        args.include_map
    )

    if args.print_count:
        print(len(outcomes))

    if args.print_paths:
        for path, data in outcomes.items():
            print(path.resolve())

    if args.print_certs:
        for path, data in outcomes.items():
            print(path.stem)

    if args.print_outcomes:
        for path, data in outcomes.items():
            print(json.dumps(data))

    if args.print_successful_library_map:
        map = calculate_successful_libraries_to_count_map(outcomes)
        print(json.dumps(map))
