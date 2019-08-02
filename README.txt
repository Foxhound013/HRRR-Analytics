This directory serves as a repository for the analysis carried out for the 2020 TRB Paper "Evaluation of the High-Resolution Rapid Refresh Model for Forecasting Roadway Surface Temperatures"

The data is located in ./analysis/hrrr_closest2rwis_processed/all_out/
	The files in this directory are csvs for December 2018 through March 2019 for 13 sites. Each directory is named according to its site.

All programs used in the analysis can be found in the ./analysis/programs_unformatted/ directory. These files have not been set up to be run
directly from this directory. They still maintain their original file paths from the authors PC as well as the authors directory on Brown.

The files used are listed below. They're listed in the order that they would need to be used to carry out this analysis.

Files that orginated on Brown
	-autoHRRR => bash script; gets the HRRR data from Utah archive, down samples variables, down samples spatially to Indiana.
	-process => bash script; Takes the raw grib files from autoHRRR and down samples to a single grid point (or set of grid points) for a particular month (files are still in month, day, hour files).
	-sgp2csv_v2.py => python script; Take the single grid pt csv and writes together all files for a given month.
	-submit.sh => bash scipt; Used for submitting jobs to the cluster

Note: Much of the work done on brown takes a significant amount of time.
Note 2: The autoHRRR and process files rely on the wgrib2 program available on the cluster. Without wgrib2, these scripts will not work.

Files that originated on the local PC	
	-catfiles.ipynb => python notebook; Takes the data from each month and combines each months files into a site by site 4 month file for each forecast hour. Consolidates the data for analysis.
	-Plots.ipynb => python notebook; This is where the analysis actually took place.


