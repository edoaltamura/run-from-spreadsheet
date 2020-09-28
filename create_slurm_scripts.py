"""
SLURM submission script generation from spreadsheet.
"""

import argparse as ap
import pandas as pd
import os
import subprocess
import shutil

parser = ap.ArgumentParser(
    description=(
        "Generates SLURM submission scripts based on a template and the spreadsheet of "
        "runs."
    ),
    epilog=(
        "Example usage: python3 create_slurm_scripts.py -s tests.csv "
        "-p eagle_25.yml -t submission.slurm -x /path/to/swift"
    ),
)

parser.add_argument(
    "-p", "--parameter-file", help="Parameter file path", required=True, type=str
)

parser.add_argument(
    "-t", "--template", help="SLURM submission template path", required="True", type=str
)

parser.add_argument(
    "-s",
    "--spreadsheet",
    help="Spreadsheet containing your parameters and run IDs.",
    required=True,
    type=str,
)

parser.add_argument(
    "-o",
    "--output",
    help="Output filename for slurm submission script.",
    required=False,
    default="submit.slurm",
    type=str,
)

parser.add_argument(
    "-x",
    "--swift-path",
    help="Path to SWIFT executable to be used.",
    required=True,
    type=str,
)

parser.add_argument(
    "--submit",
    help="Submit all runs associated?",
    required=False,
    default=False,
    action="store_true",
)


def load_text(filename: str) -> str:
    """
    Load tex file to string.
    """
    with open(filename, "r") as handle:
        return handle.read()


def create_new_submission_string(
    submission_string: str, run_id: str, swift_path: str, parameter_file_name: str
) -> str:
    """
    Uses the submission string read from file to create a copy which will contain
    the input SWIFT usage parameters.
    """

    new_submission_string = (
        submission_string.replace("$RUN_ID", run_id)
        .replace("$SWIFT_PATH", swift_path)
        .replace("$PARAMETER_FILE", f"config/{os.path.basename(parameter_file_name)}")
    )

    return new_submission_string


def write_new_submission_string(
    submission_string: str, run_id: str, output_filename: str
) -> None:
    """
    Write new submission string to a slurm submit file.
    """

    with open(f"{run_id}/{output_filename}", "w") as handle:
        handle.write(submission_string)

    return


if __name__ == "__main__":
    args = parser.parse_args()

    print(f"Spreadsheet selected as: {args.spreadsheet}")
    print(f"Base parameter file selected as: {args.parameter_file}")
    print(f"SWIFT executable at: {args.swift_path}")
    print(f"Submission template at: {args.template}")

    spreadsheet = pd.read_csv(args.spreadsheet)
    submission_string = load_text(args.template)

    for index, row in spreadsheet.iterrows():
        write_new_submission_string(
            create_new_submission_string(
                submission_string=submission_string,
                run_id=row["Run ID"],
                swift_path=args.swift_path,
                parameter_file_name=args.parameter_file,
            ),
            run_id=row["Run ID"],
            output_filename=args.output,
        )

        # Set-up common files in /config subdirectory
        shutil.copyfile(
            os.path.join(os.path.dirname(args.spreadsheet), 'output_list.txt'),
            os.path.join(row["Run ID"], 'config', 'output_list.txt')
        )
        shutil.copyfile(
            os.path.join(os.path.dirname(args.spreadsheet), 'select_output.yml'),
            os.path.join(row["Run ID"], 'config', 'select_output.yml')
        )
        shutil.copyfile(
            os.path.join(os.path.dirname(args.spreadsheet), 'vr_config_hydro.cfg'),
            os.path.join(row["Run ID"], 'config', 'vr_config_hydro.cfg')
        )

    if args.submit:
        validate = input(
            "Do you really wish to submit of the scripts generated with "
            "this script? Type YES: "
        )

        if validate == "YES":
            for index, row in spreadsheet.iterrows():
                print(f"Submitting {row['Run ID']}")
                os.chdir(row["Run ID"])
                subprocess.call(["sbatch", args.output])
                os.chdir("../")
        else:
            print("Validation failed, exiting.")
