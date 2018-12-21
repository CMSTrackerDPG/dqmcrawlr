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
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30),
    )

    parser.add_argument(
        "input",
        help="input file containing one run number and reconstruction type per line",
    )

    resource_group = parser.add_mutually_exclusive_group(required=True)
    resource_group.add_argument("--resource", help="name of the resource/ histogram")
    resource_group.add_argument(
        "--trackingmap",
        help="Shortcut for the TrackEtaPhi_ImpactPoint_GenTk resource",
        action="store_true",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--force-online",
        help="Use only online DQM and ignore reconstruction type.",
        action="store_true",
    )
    group.add_argument(
        "--no-cache",
        help="Don't use dataset cache for offline DQM.",
        action="store_true",
    )

    return parser.parse_args()


@time_measured
def retrieve_resource(destination_folder, retrieval_function, *args, **kwargs):
    json_output = retrieval_function(*args, **kwargs)
    path = "{}/{}_{}.json".format(
        destination_folder, kwargs["run_number"], kwargs["reconstruction"]
    )
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

    check_certificates()

    force_online = args.force_online
    use_dataset_cache = False if args.no_cache or args.force_online else True
    input_file_name = args.input

    if args.trackingmap:
        resource = "TrackEtaPhi_ImpactPoint_GenTk"
    else:
        resource = args.resource

    destination_folder = re.search(r"\w+$", resource).group(0)

    dataset_cache = open_dataset_cache() if use_dataset_cache else None

    crawler = DQMCrawler(dataset_cache=dataset_cache)

    runs = open_runs(input_file_name)

    if force_online:
        runs = _remove_duplicates(runs)

    print("Crawling {} runs of the resource {}\n".format(len(runs), resource))
    for run in runs:
        run_number = run["run_number"]
        reconstruction = run["reconstruction"] if not force_online else "online"

        print("{} {:10s} ".format(run_number, "{}...".format(reconstruction)), end="")
        sys.stdout.flush()

        try:
            if args.trackingmap:
                retrieve_resource(
                    destination_folder,
                    crawler.get_tracking_map,
                    run_number=run_number,
                    reconstruction=reconstruction,
                )
            else:
                retrieve_resource(
                    destination_folder,
                    crawler.get_json,
                    run_number=run_number,
                    reconstruction=reconstruction,
                    resource=args.resource,
                )
        except Exception as e:
            print("ERROR")
            print(e)

    print("Done.")
    print()
    print("All files have been saved in the folder '{}'".format(destination_folder))

    if use_dataset_cache:
        print()
        print("Saving dataset cache...")
        save_dataset_cache_to_disk(crawler.dqm_session.cache.datasets)
        print("Done.")


if __name__ == "__main__":
    main()
