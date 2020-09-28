"""
Parameter file generation from spreadsheet.
"""

import argparse as ap
import pandas as pd
import yaml
import os
import shutil

parser = ap.ArgumentParser(
    description=(
        "Generates directories and parameter files based on the provided spreadsheet"
    ),
    epilog=(
        "Example usage: python3 create_parameter_files.py -s tests.csv -p eagle_25.yml"
    ),
)

parser.add_argument(
    "-p", "--parameter-file", help="Base parameter file path.", required=True, type=str
)

parser.add_argument(
    "-s",
    "--spreadsheet",
    help="Spreadsheet containing your parameters and run IDs.",
    required=True,
    type=str,
)

parser.add_argument(
    "--clean",
    help="Delete all of the runs generated with this script.",
    required=False,
    default=False,
    action="store_true",
)


def load_yaml(filename: str) -> dict:
    """
    Load yaml file to dictionary (possibly of dictionaries).
    """
    with open(filename, "r") as handle:
        return yaml.load(handle, Loader=yaml.Loader)


def create_new_parameter_file(parameter_file: dict, row: pd.core.series.Series) -> dict:
    """
    Create a new parameter file from the old one, changing the data
    to be the stuff from `row`, which is a pandas dataframe row.
    """

    new_parameter_file = parameter_file.copy()

    for parameter, value in row.iteritems():
        if parameter in ["Run ID", "Comment"]:
            continue

        section, param = parameter.split(":")
        new_parameter_file[section][param] = value

    new_parameter_file["MetaData"]["run_name"] = row["Run ID"]

    return new_parameter_file


def write_new_parameter_file(parameter_file: dict, run_id: str, filename: str) -> None:
    """
    Writes a new parameter file to run_id/config/filename.
    """

    with open(f"{run_id}/config/{filename}", "w") as handle:
        yaml.dump(parameter_file, handle, default_flow_style=False)

    return


if __name__ == "__main__":
    args = parser.parse_args()

    print(f"Spreadsheet selected as: {args.spreadsheet}")
    print(f"Base parameter file selected as: {args.parameter_file}")

    spreadsheet = pd.read_csv(args.spreadsheet)
    parameter_file = load_yaml(args.parameter_file)

    if args.clean:
        validate = input(
            "Do you really wish to delete all of the directories generated with "
            "this script? Type YES: "
        )

        if validate == "YES":
            for index, row in spreadsheet.iterrows():
                if os.path.exists(row["Run ID"]):
                    print(f"Deleting {row['Run ID']}")
                    shutil.rmtree(f"./{row['Run ID']}")
        else:
            print("Validation failed, exiting.")

    else:
        for index, row in spreadsheet.iterrows():

            if not os.path.exists(row["Run ID"]):
                os.mkdir(row["Run ID"])

            if not os.path.exists(f"{row['Run ID']}/config"):
                os.mkdir(f"{row['Run ID']}/config")

            shutil.copyfile(
                os.path.join(os.path.dirname(args.spreadsheet), os.path.basename(args.parameter_file)),
                os.path.join(row["Run ID"], 'config', os.path.basename(args.parameter_file))
            )

            write_new_parameter_file(
                create_new_parameter_file(parameter_file=parameter_file, row=row),
                run_id=row["Run ID"],
                filename=args.parameter_file,
            )
