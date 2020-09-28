General functionalities
-----
Generates runs based on a spreadsheet provided, with
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

Calibration of zoom simulations
-----
This repository, forked from Josh's pipeline for calibrating EAGLE-XL 
periodic cosmological boxes, is adapted to be used for setting up
zoom simulations. The listing functionality of the spreadsheet allows
to run a whole sample of group or clusters with different sets of 
subgrid parameters. Although runs at different resolutions could be 
gathered in the same `.csv` file, we do recommend the use of separate 
files, since the set-up pipeline would need to handle significantly 
different sets of parameters (e.g. particle softenings, particle
splitting threshold and other resolution-dependent quantities).

The spreadsheet includes explicit specification of the initial 
conditions file of the individual run, in order to allow for different
objects in the sample to appear in the same spreadsheet.

Once the spreadsheet is selected, make sure to look at the `launch_setup.sh` script
and edit the directory where you wish to set-up the runs. After that, just run the
script as 
```bash
source launch_setup.sh
```

Reference model
-----
The runs are compared to a reference subgrid model, commonly identified as
`Ref`. This calibration set of simulations is created such as the sample is
firstly run with the `Ref` model, in order to then explore departures from it.