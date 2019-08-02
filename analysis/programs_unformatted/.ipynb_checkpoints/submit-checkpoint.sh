#!/bin/sh

#PBS -N feb_RWIS 
#PBS -l nodes=1:ppn=6,naccesspolicy=singleuser,walltime=01:30:00
#PBS -q wwtung 
#PBS -m abe

module load anaconda/5.3.1-py27
source activate jtrp

cd $PBS_O_WORKDIR

#./process |& tee feb_RWIS.log
python ./sgp2csv_v2.py |& tee feb_RWIS.log
