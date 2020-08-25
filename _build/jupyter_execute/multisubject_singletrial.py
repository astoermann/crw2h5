---
# Multiple subject, single trial example

## Conda environment
*always activate a conda environment before starting. This notebook uses [mkconda](https://anaconda.org/kutaslab/mkconda) 0.0.11*

conda activate mkconda-0.0.11

## Python Libraries

from pathlib import Path
from mkpy import mkh5
import pandas as pd

## Build the file
There is now a loop to incorporate multiple subjects into one file. This makes the following changes:
* A variable is added at the beginning with a list of the subjects you want to include in the loop/file (sids)
* Creating the file names is under the loop for the data files (not the h5 files since there is one file) 
* mk5 commands to create the continuous file go under the loop
* An 'if' statement is used for the append_mkdata command for an extra cal file
* Commands after the continuous file is built (get_event_table, set_epochs, export_epochs) are done on the entire file and aren't in the loop <br>
* If you need a refresher on any of the commands, see {doc}`singlesubject_binned`

A time function has been added at the top of the cell to demonstrate that the file now takes a while to build

Code Map:
* For this example we will use the .xls format for the code map (see {doc}`codemaps` xlsx example)

%%time
# set data directories
MKDIG_DIR = Path("../../mkdig")
MKPY_DIR = Path("../../mkpy")

# set the subject number(s) to loop across
sids = ['02', '03', '04', '05', '06', '07', '08', '09', '10', 
    '12', '13', '14', '15', '16', '17', '19', '20', '21',
    '22', '23', '24', '25', '26', '27', '28', '30', '31',
    '33', '34', '35']

# name files  
h5_f = MKPY_DIR / ("stmath.h5")
epochtable = MKPY_DIR / ("stmath.epochs.h5")

# reset the .h5 file
myh5 = mkh5.mkh5(h5_f)
myh5.reset_all()

# loop over subjects to add to one h5 file
for sid in sids:
    
    # subject number
    sub = 'stm'+sid
    
    # subject file names
    yhdr = MKPY_DIR / (sub + ".yhdr")
    eeg = MKDIG_DIR / (sub + ".crw")
    log = MKDIG_DIR / (sub +".x.log")

    # load in subject files
    myh5.create_mkdata(sub, eeg, log, yhdr)
    
    ##stm03 has separate cal files, so append the data   
    if sub == 'stm03':
        myh5.append_mkdata('stm03', 
                           MKDIG_DIR / ("stm03cal.crw"), 
                           MKDIG_DIR / ("stm03cal.x.log"), 
                           MKPY_DIR / ("stm03.yhdr"))    

        
    # calibrate data
    pts, pulse, lo, hi, ccode = 5, 10, -40, 40, 0
    myh5.calibrate_mkdata(sub, # specific data group
                        n_points = pts,   # pts to average
                        cal_size = pulse, # uV
                        lo_cursor = lo,   # lo_cursor ms
                        hi_cursor = hi,   # hi_cursor ms
                        cal_ccode= ccode) # condition code

# Find event codes in the data                        
event_table_raw = myh5.get_event_table(MKPY_DIR / ("stmath_code_map_new.xlsx"))

```{note}
The warnings above:

`LogRawEventCodeMismatch` is to check the data and make sure it is okay that the raw and log file event codes mismatch. This happens sometimes when you pause DIG and should be fine as long as the mismatch is trailing events (as in this case).

`dropping out of bounds` happens when the pause mark happened outside of the window you set for cals to be measured (i.e., -40ms to 40ms)

```

### Data tranformations to the event table
You do not have to do this step, but it is useful to know that you can 'break in' to the pandas data frame to add more data or drop rows to make the epochs file not as large when you export it. 
#### Add extra variables across all columns
These are new variables that you want columns for that are not imported with the header or code map (useful if you are combining multiple experiments but want one code map)

# show the column names before adding variables
display(event_table_raw.columns)

# code for experiment
event_table_raw['expt'] = "expt_1"
# show the a few variables from the data frame with the new column added
event_table_raw[['data_group','crw_ticks','regexp','match_code','Stimulus','expt', 'anchor_tick_delta']].head(6)

#### Get reaction times
*Note: this example has an event in between the one we want to time lock too and the one we want to get a reaction time for. If you do not have this problem, then you just need to drop the extra capture group lines.*
* *Use code similar to the first line below (.query)*
* *Query for anchor_tick_delta > or < 0 depending on where you put the anchor (#)*

# pull out the rows of the dataframe with positive response ticks(i.e, after the anchor) and copy to new dataframe
rt_df = event_table_raw.query('anchor_tick_delta > 0').copy()

# rename anchor tick delta to response ticks, so variables don't get overwritten on merging
rt_df["response_ticks"] = rt_df["anchor_tick_delta"]

# select on the variables needed for merging
rt_df = rt_df.loc[:, ['data_group','response_ticks','anchor_code']]

# set the index for merging later
rt_df.set_index(['data_group','anchor_code'],inplace=True)

# check the dataframe has the variables you want for merging later
rt_df.head()

#get clean rows of the dataframe for merging (i.e., drop the two capture groups that shouldn't have time-locked epochs)
clean_events = event_table_raw.query('log_evcodes < 20000 and anchor_tick_delta <= 0')

# set the index for merging later
clean_events.set_index(['data_group','anchor_code'],inplace=True)

# check the dataframe has the variables you want for merging later; display only a few variables for demonstration
# anchor_tick_delta is negative for the product event because the time-locked event is before the anchor code
clean_events[['crw_ticks','regexp','match_code','Stimulus','expt', 'anchor_tick_delta']].head(6)

# merge response ticks and clean dataframes together 
clean_rt = clean_events.join(rt_df,on=['data_group','anchor_code'])

# reset the index to the default (the rest of mkpy expects a certain index structure)
clean_rt.reset_index(['anchor_code'],inplace=True)

# check the dataframe; display only a few variables for demonstration
# response ticks only merge onto the product rows since that is what the response is to
clean_rt[['crw_ticks','regexp','match_code','Stimulus', 'expt', 'anchor_tick_delta','response_ticks']].head(8)

#### Merge in data from Excel

# set columns of interest from the spreadsheet
npsych_coi = [
    'Subj', 'Gndr', 'Age', 'NativeLang', 'Bilingual', 'Major', 'GoodMath',
    'Rhand','Lhand', 'Famhand', 'WhoLH', 'ARTCorrect', 'ARTFoils', 
    'MRTCorrect','MRTFoils', 'MathAnxiety1', 'MathAnxiety2', 
    'BEM_M', 'BEM_F', 'BEM_N','DS_F', 'DS_B', 'DS_H'
]
# read the Excel spreadsheet into pandas and do some data transformation; 
# look up pd.read_excel for arguments
stmath_neuro = (
    pd.read_excel(
        "/home/kadelong/Exps/STMath/Neuro/Neuro.xlsx",
        header=2,
        nrows=30)
    .loc[:, npsych_coi]
    .rename(columns={"Subj": "data_group"})
    .set_index('data_group')
)
# check the data imported properly; display only a few variables for demo
stmath_neuro[['Rhand','Lhand','ARTCorrect','MRTCorrect', 'DS_F']].head()

#### Merge dataframes together 
This gets a final event_table dataframe for exporting by merging all the other dataframes you already created.

# merge neuropsych dataframe with response ticks dataframe
event_table=clean_rt.join(stmath_neuro, on="data_group")

# reset the index to the default (the rest of mkpy expects a certain index structure)
event_table.reset_index(['data_group'],inplace=True)

# display columns and a few variables to check everything merged correctly
display(event_table.columns)
event_table[['data_group','crw_ticks','regexp','Stimulus','expt','response_ticks','Rhand','Lhand']].head(8)

## Set epochs
Set epochs with all the new added columns. Same as the single subject example.

myh5.set_epochs('stmath', event_table, -100, 900) # tmin ms, tmax ms,



```{note}
The warnings above `data error` happens when the pause mark happened outside of the window you set to be epoched (i.e., -40ms to 40ms)

```

## Export epochs

# set columns of interest for export to reduce file size, can also reorder thiem this way. 
# some columns are required for other software in the lab, so be careful when dropping
COI = ['epoch_id','match_time','data_group', 'Item', 'List', 
       'ThreatCondition', 'Condition', 'Stimulus', 'ResponseAccuracy', 
       'Operand1', 'Operand2', 'Operand3', 'ShownProduct', 'CorrectProduct',
       'Gndr', 'Age', 'NativeLang', 'Bilingual','Major', 'GoodMath', 
       'Rhand', 'Lhand', 'Famhand', 'WhoLH', 'ARTCorrect', 'ARTFoils', 
       'MRTCorrect', 'MRTFoils', 'MathAnxiety1', 'MathAnxiety2',
       'BEM_M', 'BEM_F', 'BEM_N', 'DS_F', 'DS_B', 'DS_H',
       'response_ticks', 'log_evcodes', 'log_flags', 
       'lle', 'lhz', 'MiPf', 'LLPf', 'RLPf', 'LMPf', 'RMPf', 'LDFr', 'RDFr', 
       'LLFr', 'RLFr', 'LMFr', 'RMFr', 'LMCe', 'RMCe', 'MiCe', 'MiPa', 'LDCe', 
       'RDCe', 'LDPa', 'RDPa', 'LMOc', 'RMOc', 'LLTe', 'RLTe', 'LLOc', 'RLOc', 
       'MiOc', 'A2', 'HEOG', 'rle', 'rhz']   

# export epochs
myh5.export_epochs('stmath', epochtable, file_format='h5', columns=COI)
    
print('done stmath1')