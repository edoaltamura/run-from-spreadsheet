"""
SLURM submission script generation for VELOCIraptor from spreadsheet.

Uses the following variables:

$RUN_NAME
$VELOCIRAPTOR_INVOCATIONS
"""

import argparse as ap
import pandas as pd
import numpy as np
import os
import subprocess

from typing import List

parser = ap.ArgumentParser(
    description=(
        "Generates SLURM submission scripts for VELOCIraptor to run on your "
        "outputs. Does not overwrite previously written catalogues unless asked "
        "to."
    ),
    epilog=(
        "Example usage: python3 create_vr_slurm_scripts.py "
        "-t velociraptor_template.slurm -s runs.csv -x /path/to/vr "
        "-C /path/to/config -l ~/Desktop/output_list.txt"
    ),
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
    default="velociraptor_submit.slurm",
    type=str,
)

parser.add_argument(
    "-x",
    "--velociraptor-path",
    help="Path to VELOCIraptor executable to be used.",
    required=True,
    type=str,
)

parser.add_argument(
    "-C",
    "--config",
    help="Path to VELOCIraptor configuration file to be used.",
    required=True,
    type=str,
)

parser.add_argument(
    "-c",
    "--catalogue",
    help="Catalogue basename for VELOCIraptor output.",
    required=False,
    type=str,
    default="halo",
)

parser.add_argument(
    "-l",
    "--output-list",
    help="Output list associated with your simulation.",
    required=True,
    type=str,
)

parser.add_argument(
    "-r",
    "--run-on",
    help="Select Output variations to run velociraptor on.",
    required=False,
    default=["Snapshot"],
    nargs="+",
)

parser.add_argument(
    "-b",
    "--basename",
    help="Snapshot basename to use.",
    required=False,
    default="eagle",
)

parser.add_argument(
    "--submit",
    help="Submit all runs associated?",
    required=False,
    default=False,
    action="store_true",
)

parser.add_argument(
    "--overwrite",
    help="Overwrite existing catalogues?",
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


def get_snapshot_numbers(output_list: str, run_on: List[str]) -> List[int]:
    """
    Get the snapshot numbers to run velociraptor on, from the output list.
    """

    data = pd.read_csv(output_list)

    # Need extra spaces because pandas doesn't seem to recognise the space after
    # a comma as a valid delimimter by default.
    numbers_to_run_on = np.arange(len(data))[
        np.logical_or.reduce(
            [data[" Select Output"] == f" {select_output}" for select_output in run_on]
        )
    ]

    return list(numbers_to_run_on)


def get_snapshot_names(
    snapshot_numbers: List[int],
    snapshot_basename: str,
    catalogue_basename: str,
    run_id: str,
    overwrite: bool,
):
    """
    Gets the snapshot names that we must run VELOCIraptor on. These are snapshots
    that both exist, and have not already had VR run on them.
    """

    names = []

    for snapshot_number in snapshot_numbers:
        catalogue_name = f"{catalogue_basename}_{snapshot_number:04d}.properties"
        if (
            os.path.exists(f"{run_id}/{catalogue_name}")
            or os.path.exists(f"{run_id}/{catalogue_name}.0")
        ) and not overwrite:
            continue

        snapshot_name = f"{snapshot_basename}_{snapshot_number:04d}"

        if not os.path.exists(f"{run_id}/{snapshot_name}.hdf5"):
            continue

        names.append(snapshot_name)

    return names


def create_velociraptor_invocation(
    snapshot_names: List[str],
    velociraptor_path: str,
    config_path: str,
    catalogue_basename: str,
) -> str:
    """
    Create velociraptor invocation string based on snapshot names.
    """

    return "\n".join(
        [
            (
                f"{velociraptor_path} -i {snapshot_name} -I 2 -o {catalogue_basename} "
                f"-C {config_path}"
            )
            for snapshot_name in snapshot_names
        ]
    )


def create_new_submission_string(
    submission_string: str, run_id: str, velociraptor_invocation: str
) -> str:
    """
    Uses the submission string read from file to create a copy which will contain
    the input VELOCIraptor usage parameters.
    """

    new_submission_string = submission_string.replace("$RUN_ID", run_id).replace(
        "$VELOCIRAPTOR_INVOCATION", f"{velociraptor_invocation}"
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
    print(f"Submission template at: {args.template}")
    print(f"VELOCIraptor path at: {args.velociraptor_path}")
    print(f"VELOCIraptor config file: {args.config}")
    print(f"Catalogue output basename: {args.catalogue}")
    print(f"Simulation output list: {args.output_list}")
    print(f"Running VR on snapshots of type: {args.run_on}")
    print(f"Assuming snapshot basename of: {args.basename}")

    spreadsheet = pd.read_csv(args.spreadsheet)
    submission_string = load_text(args.template)

    if args.overwrite:
        validate = input(
            "Do you really wish to overwrite the already existing catalogues? "
            "Type YES: "
        )

        if validate != "YES":
            print("Run this script again without --overwrite present.")
            exit(0)

    snapshot_numbers = get_snapshot_numbers(
        output_list=args.output_list, run_on=args.run_on
    )

    for index, row in spreadsheet.iterrows():
        snapshot_names = get_snapshot_names(
            snapshot_numbers=snapshot_numbers,
            snapshot_basename=args.basename,
            catalogue_basename=args.catalogue,
            run_id=row["Run ID"],
            overwrite=args.overwrite,
        )

        write_new_submission_string(
            create_new_submission_string(
                submission_string=submission_string,
                run_id=row["Run ID"],
                velociraptor_invocation=create_velociraptor_invocation(
                    snapshot_names=snapshot_names,
                    velociraptor_path=args.velociraptor_path,
                    config_path=args.config,
                    catalogue_basename=args.catalogue,
                ),
            ),
            run_id=row["Run ID"],
            output_filename=args.output,
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
