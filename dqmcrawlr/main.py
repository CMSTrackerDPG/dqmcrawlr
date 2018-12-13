from __future__ import print_function

import argparse
import json
import os
import re
import sys

from cernrequests import certs

from dqmcrawlr.decorators import time_measured
from dqmcrawlr.jsonfairy import get_json
from dqmcrawlr.utils import open_runs, save_to_disk


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

    return parser.parse_args()


@time_measured
def retrieve_resource(run_number, reconstruction, resource, destination_folder):
    json_output = get_json(run_number, reconstruction, resource)
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


def main():
    args = parse_arguments()

    check_certificates()

    runs = open_runs(args.input)
    resource = args.resource
    destination_folder = re.sub("\/.*\/", "", resource)

    print("Crawling {} runs of the resource {}".format(len(runs), resource))
    for run in runs:
        run_number = run["run_number"]
        reconstruction = run["reconstruction"]

        print("Crawling {} {:10s} ".format(run_number, "{}...".format(reconstruction)), end="")
        sys.stdout.flush()

        try:
            retrieve_resource(run_number, reconstruction, resource, destination_folder)
        except Exception as e:
            print("ERROR")
            print(e)

    print("Done.")
    print()
    print("All files have been saved in the folder '{}'".format(destination_folder))


if __name__ == "__main__":
    main()
