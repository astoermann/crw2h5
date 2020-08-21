---
# Binned, single subject example 
*See [mkpy docs](https://kutaslab.github.io/mkpy/Quick%20Start.html) for explanations of all the commands and files. Click on the command to find it in the glossary and learn more. The glossary links are incuded for each command below* <br>
## Conda environment
*always activate a conda environment before starting. This notebook uses [mkconda](https://anaconda.org/kutaslab/mkconda) 0.0.11*

conda activate mkconda-0.0.11

## Python Libraries

from pathlib import Path
from mkpy import mkh5
import pandas as pd

## Data Paths
Set paths and variable names for files later

MKDIG_DIR = Path("../../mkdig")
MKPY_DIR = Path("../../mkpy")

## File names
Set file names so they can be easily changed and don't have to retype every time

# h5 continuous file 
h5_f = str(MKPY_DIR / ("stm02.h5"))

# h5 epoch file 
epochtable = str(MKPY_DIR / ("stm02.epochs.h5"))

# subject ID
sub = 'stm02'

# kutas lab data files (from DIG + yhdr that you created)
eeg = MKDIG_DIR / (sub + ".crw")
log = MKDIG_DIR / (sub +".x.log")
yhdr = MKPY_DIR / (sub + ".yhdr")

## Build the continuous h5 file

1) [mkh5.mkh5](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5): Import the h5 file into a dataframe and reset it (generally you will want to reset the file to start fresh).

myh5 = mkh5.mkh5(h5_f)
myh5.reset_all()

2) [create_mkdata](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.create_mkdata): load in subject and cals to the h5 data structure<br><br>
*The first argument is the data branch you want to add the data to. This can be subject name, or for more complicated files could be a path.*<br><br>
&emsp;2a) [append_mkdata](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.append_mkdata): if your file is split into two for some reason (i.e., separate cals, DIG crash) this is where you would add this command as well

myh5.create_mkdata(sub, eeg, log, yhdr)

3) [calibrate_mkdata](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.calibrate_mkdata): calibrate data; the first line sets the values similar to normerp<br><br>
*If you don't know what values to use, you can use [plotcals](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.plotcals) to select them before running the calibrate command.* 

pts, pulse, lo, hi, ccode = 5, 10, -40, 40, 0
myh5.calibrate_mkdata(sub, # specific data group
                    n_points = pts,   # pts to average
                    cal_size = pulse, # uV
                    lo_cursor = lo,   # lo_cursor ms
                    hi_cursor = hi,   # hi_cursor ms
                    cal_ccode= ccode) # condition code

## Find event codes in the data
[get_event_table](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.get_event_table): Label the events in the data, but don't pull out epochs yet. Capture this info in a data frame.
* For this simple example we will use the .ytbl format for the code map (see {doc}`codemaps` ytbl example)

event_table = myh5.get_event_table(MKPY_DIR / ("stmath.ytbl"))
## Look at the event table you just made
event_table.head(312)

## Set epochs
[set_epochs](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.set_epochs): Pull out epochs in the data. Does not save them yet.
* First argument is the name of the epochs table
* Second argument is the event table you made (not the code map)
* Third and fourth argument is the window you want the epoct to have around 0

myh5.set_epochs('stmath', event_table, -100, 900) 

## Export epochs
[export_epochs](https://kutaslab.github.io/mkpy/source/mkpy.mkh5.html#mkpy.mkh5.mkh5.export_epochs): save the epoched data to use later. Can be in h5, pdh5 (pandas), or feather format.
* First argument is the epochs table
* Second argument is the file name to save to (set above in the file names section)
* Third argument is what you want to save as

myh5.export_epochs('stmath', epochtable, file_format='h5')