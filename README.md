# PicosecDataAnalysis
Tools for Picosec Analysis:

`analyze_SPErun.py` is for the analysis of the single photo-electron response 

## Requirements
- install python packages in `requirements.txt`
```pip3 install -r requirements.txt```
- change `path.txt` following your needs. `run_path` is the directory where are stored the raw scope data. `result_path` is the directory where are stored the analysis results. `trk_path` is the directory where are stored the tracker data.

# Analyze Single PhotoElectron Run
`analyze_SPErun.py` is for the analysis of the single photo-electron response.
```python3 analyze_SPErun.py -options```

- `-r` number of the run contained in the standard_path (REMEMBER THE 0 if <100)
- `-d` any value allows to draw all waveform, default None
- `-b` Run ROOT in batch mode, default=1
- `-c` channel to analyze, default=2
- `-s` limit in the number of files to analyze, defalut=all
- `-po` any value will disable the complex polya fit, default None
- `-n` put a name for the SignalScope object if you want, default=test
- `-w` any value will disable the csv results writing, default None

## Description
The program starts by executing `path.txt` lines. 
Here it takes every path useful to take data and to write results. If the `result_path` doesn't exist it will be created further. `trk_path` is not needed for the single photoelectron response study.
After that, there are some definitions of functions that are used to create histograms and graphs. Here you can change some default parameters like the number of channels in histograms or the graphic design of the output.
Then the options written above are set. For the options that can only be on/off the default is defined as `None` and every value the user types will change the state.

Later `run_path` and `result_path` are updated depending on the `-r` value specified by the user.


After is created the results folder, if it doesn't exist yet, and a file ROOT named `result_path/Run_*run_num*.root`.

Then is take the number of files to analyse. If is not specified by the user the program will analyse every file in the selected run. Files are sorted by channel number (the default channel is 2). 

After are taked the files separately and is used the class `ScopeSequence` that is defined in `waveform`. Initialising a `ScopeSequence` object defines automatically some wave and scope parameters like impedance and point per wave. With the function `GetWaves()` every wave is taken singularly. The time elapsed collecting waves is computed and shown in the terminal.

Later is created the `RawWaveForm` folder in the main ROOT directory. 

Then is started the analysis. 





# Analyze Multi PhotoElectron Run
# Analyze Timing Run