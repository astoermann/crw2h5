# Spudtr
Use [spudtr](https://kutaslab.github.io/spudtr) to do some processing on your epoched file.

## Conda environment
*always activate a conda environment before starting. This notebook uses [mkconda](https://anaconda.org/kutaslab/mkconda) 0.0.11*

conda activate mkconda-0.0.11

## Python Libraries

import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
from spudtr import epf

## Read in epochs file

MKPY_DIR = Path("../../mkpy")

stmath_df = pd.read_hdf(MKPY_DIR / ("stmath.epochs.h5"), key='stmath')
## Display the data to check it loaded in correctly
stmath_df[['epoch_id','match_time','data_group','Stimulus','response_ticks','Rhand','Lhand', 'MiPf']]

## Change column names and specify variables for later
Do not change epoch_id or match_times if you intend to use fitgrid <br>
<br>
If you do not specify a channels variable, you will have to type the channels for every command.

# munge dataframe columns
new_names={
    "data_group": "sub_id",
    "log_flags": "garv_reject",
}
stmath_df.rename(columns=new_names, inplace=True)

CHANNELS = [
    'lle', 'lhz', 'MiPf', 'LLPf', 'RLPf', 'LMPf', 'RMPf', 'LDFr', 
    'RDFr', 'LLFr', 'RLFr', 'LMFr', 'RMFr', 'LMCe', 'RMCe', 'MiCe',
    'MiPa', 'LDCe', 'RDCe', 'LDPa', 'RDPa', 'LMOc', 'RMOc', 'LLTe',
    'RLTe', 'LLOc', 'RLOc', 'MiOc', 'A2', 'HEOG', 'rle', 'rhz'
]

## Re-referencing
Can do linked pair (from one online reference to the average of two), new common reference (pick a new reference), or common average reference (subtract the average of all channels from each channel)<br>
<br>
This example uses linked pair since it is what we most commonly use

```{note}
There is no output for the re-referencing, baselining, or artifact rejection unless you ask for it since we are overwritting the dataframe each time to save the data transformation.
```

stmath_df = epf.re_reference(
    stmath_df,
    CHANNELS,
    'A2',
    "linked_pair",
    epoch_id="epoch_id", time="match_time",
)


## Baselining
center the epoch around a prestimulus interval set with the start and stop variables

start = -100
stop = 0
stmath_df = epf.center_eeg(
    stmath_df,
    CHANNELS,
    start,
    stop,
    epoch_id='epoch_id',
    time='match_time'
)

## Artifact Rejection
method used for if you created the h5 file using an .x.log to preserve garv flags<br>
<br>
```{note} 
above I renamed the appropriate column to garv_reject to be more transparent about what I was doing
```

good_epochs = epf.drop_bad_epochs(
    stmath_df,
    bads_column="garv_reject",
    epoch_id='epoch_id',
    time='match_time',
)

print("Total number of epoch ids: ", len(stmath_df["epoch_id"].unique()))
print("Number of good epoch ids: ", len(good_epochs["epoch_id"].unique()))

## Save file to be loaded later

good_epochs.to_hdf('../../mkpy/stmath_cleaned_epochs.h5', key='stmath_good_epochs', mode='w')