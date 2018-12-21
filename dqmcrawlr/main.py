from __future__ import print_function

import sys

import argparse
import json
import os
import re
from cernrequests import certs

from dqmcrawlr.crawler import DQMCrawler
from dqmcrawlr.decorators import time_measured
from dqmcrawlr.utils import (
    open_runs,
    save_to_disk,
    open_dataset_cache,
    save_dataset_cache_to_disk,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=" CMS Data Quality Monitor crawler.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=36),
    )

    parser.add_argument(
        "-i",
        "--input",
        help="input file containing one run number and reconstruction type per line",
    )

    parser.add_argument("-r", "--resource", help="name of the resource/ histogram")

    parser.add_argument(
        "-c",
        "--cached",
        help="Use existing dataset cache to save time.",
        action="store_true",
    )

    parser.add_argument(
        "--online", help="Use online DQM rather than offline.", action="store_true"
    )

    return parser.parse_args()


@time_measured
def retrieve_resource(
    crawler, run_number, reconstruction, resource, destination_folder
):
    json_output = crawler.get_json(run_number, reconstruction, resource)
    path = "{}/{}_{}.json".format(destination_folder, run_number, reconstruction)
    save_to_disk(json.dumps(json_output, indent=2), path)
    print("OK", end="")


def check_certificates():
    cert, key = certs.default_user_certificate_paths()
    if not os.path.isfile(cert):
        print("Error: {} does not exist".format(cert))
        sys.exit()
    if not os.path.isfile(key):
        print("Error: {} does not exist".format(key))
        sys.exit()


def _remove_duplicates(runs):
    run_numbers = sorted(set([run["run_number"] for run in runs]))
    return [{"run_number": run_number} for run_number in run_numbers]


def main():
    args = parse_arguments()

    online_service_only = args.online
    use_dataset_cache = args.cached
    input_file_name = args.input
    resource = args.resource

    destination_folder = re.sub(r"\/.*\/", "", resource)

    check_certificates()

    dataset_cache = open_dataset_cache() if use_dataset_cache else None

    crawler = DQMCrawler(dataset_cache=dataset_cache)

    runs = open_runs(input_file_name)

    if online_service_only:
        runs = _remove_duplicates(runs)

    print("Crawling {} runs of the resource {}\n".format(len(runs), resource))
    for run in runs:
        run_number = run["run_number"]
        reconstruction = run["reconstruction"] if not online_service_only else "online"

        print("{} {:10s} ".format(run_number, "{}...".format(reconstruction)), end="")
        sys.stdout.flush()

        try:
            retrieve_resource(
                crawler, run_number, reconstruction, resource, destination_folder
            )
        except Exception as e:
            print("ERROR")
            print(e)

    print("Done.")
    print()
    print("All files have been saved in the folder '{}'".format(destination_folder))

    if args.cached:
        print()
        print("Saving dataset cache...")
        save_dataset_cache_to_disk(crawler.dqm_session.cache.datasets)
        print("Done.")


if __name__ == "__main__":
    main()
