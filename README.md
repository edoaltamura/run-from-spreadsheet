Generates runs based on a spreadshseet provided, with
individual directories.

The spreadsheet should be organised as follows:

Run ID | EagleSection:Param | EagleSection:Param2 | ... | Comment
-------|--------------------|---------------------|-----|----------
Hello  |        0.1         |          0.2        | ... | Good run!
...    |        ...         |          ...        | ... |   ...

This will then generate directories for each of the Run IDs,
changing the selected parameters to the new values based on a
'base' parameter file.

You can also generate submission scripts, with a template
that uses the following special parameters

+ `$SWIFT_PATH` - the path to the SWIFT executable
+ `$RUN_ID` - ID for the run
+ `$PARAMETER_FILE` - the parameter file name

Don't forget to change the directory paths in your
parameter file to include a relative change to one directory
higher (e.g. `../output_list.txt`).

Finally, you can create a submission script to run VELOCIraptor on your
outputs in postprocessing by using the `create_vr_slurm_scripts.py` file.
Note that this assumes that you run it from the same directory as the others
(i.e. one above the `Run ID` directories that `create_parameter_files.py`
created).