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

Then is take the number of files to analyze. If is not specified by the user the program will analyze every file in the selected run. Files are sorted by channel number (the default channel is 2). 

After are taked the files separately and is used the class `ScopeSequence` that is defined in `waveform`. Initialising a `ScopeSequence` object defines automatically some wave and scope parameters like impedance and point per wave. With the function `GetWaves()` every wave is taken singularly. The time elapsed collecting waves is computed and shown in the terminal.

Later is created the `RawWaveForm` folder in the main ROOT directory. 

Then is started the analysis. 

- no cuts are made to take also the noise pedestal
- first the gaussian on the maximum to get the pedestal then the gaus+polya fit

If waves aren't drawn the analysis is parallelysed.
At the end, the results are stored in a data frame. 
The columns of the data frame are:
- `BadFlag`, which is a boolean and is True when the signal is bad, in this program should be always False since there are no cuts,
 - `SigmaOutNoise`, which is the difference between the signal peak and the pedestal in terms of standard deviation,
 - `Baseline` which is the measure of the noise,
 - `Epeakcharge`, which is the maximum of the peak 
 - `RiseTime`
 - `AmpMin`, which is the time of start of the electron peak.



 Then histograms are created with the results obtained for noises, baseline, charge, differences between signal and noise and rise time.

 Once created, the amplitude histograms are fitted, first with a gaussian in a small range around the peak to get the pedestal, then the fit parameters are used as starting parameters for a gaussian+polya fit.
 If option `-po` is activated the fit is done only with the polya.

 After that the code will append the main results in a `.csv` file named `resultsPE`.



 



# Analyze Multi PhotoElectron Run


# Analyze Timing Run
The code is divided into two parts for easy processing of data. `process_TIMErun.py` process the run and output a ROOT file with the output. The `analyze_TIMErun.py` take the raw data and applies the cut and performs the plotting.
## Processing
For now, no cuts are made so all the waveforms are passed.

## Analizing