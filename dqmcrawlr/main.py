import argparse
import json
import re

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


def main():
    args = parse_arguments()
    runs = open_runs(args.input)
    resource = args.resource
    destination_folder = re.sub("\/.*\/", "", resource)

    print("Crawling {} runs of the resource {}".format(len(runs), resource))
    for run in runs:
        run_number = run["run_number"]
        reconstruction = run["reconstruction"]
        print(
            "Crawling {} {}...".format(run_number, reconstruction), end="", flush=True
        )
        try:
            json_output = get_json(run_number, reconstruction, resource)
            path = "{}/{}_{}.json".format(
                destination_folder, run_number, reconstruction
            )
            save_to_disk(json.dumps(json_output, indent=2), path)
            print(" OK")
        except:
            print(" ERROR")

    print("Done.")
    print()
    print("All files have been saved in the folder '{}'".format(destination_folder))


if __name__ == "__main__":
    main()
