# PicosecDataAnalysis

Tools for Picosec Analysis:

- `analyze_SPErun.py` is for the analysis of the single photo-electron response
- `analyze_PErun.py` is for the analysis of the multi-photo-electron response
- `process_TIMErun.py` is for the processing of the time resolution runs
- `analyze_TIMErun.py` is for the analysis of the timing runs after the processing

### Requirements

- install python packages in `requirements.txt`
```pip3 install -r requirements.txt```
- change `path.txt` following your needs. Two different configurations are possible depending if you have a testbeam like structure (path/Scope/Run+run_num) or if you have a generic folder containing all the data to analyze.
You have to define a `base_path` as the folder containing the data (usually named month+year) with a slash at the end. Define `scope` as the directory containing the runs folders (usually Pool+scope number). Define `run_path` as the concatenation of base_path+scope+Run without slash, the code will append here the run number and the complete run_path will be created. `result_path` indicates the root directory where to store the results, here a folder will be created named Run+run_num. `trk_path` and `csv_path` have to point respectively to the folder containing the tracker data (used only in PE and TIME) and the path where to save the output.
- Use the template already present in `path.txt`. *Davide PC* and *Picosec PC* may be used for setting test beam-like folders. *Local test RD51* is useful to set up the folders for usage with a generic folder hierarchy.

## Analyze Single PhotoElectron Run

`analyze_SPErun.py` is for the analysis of the single photo-electron response.
```python3 analyze_SPErun.py -options```

- `-r` number of the run contained in the standard_path (REMEMBER THE 0 if <100)
- `-d` any value allows to draw all waveform, default None
- `-b` Run ROOT in batch mode, default=1
- `-c` channel to analyze, default=2
- `-s` limit in the number of files to analyze, defalut=all
- `-po` any value will disable the complex polya fit, default None
- `-n` put a name for the SignalScope object if you want, default=test
- `-w` any value will disable the .csv results writing, default None
- `deb` print the reason for some bad flags

### Description

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

## Analyze Multi PhotoElectron Runù

The code structure is the same as SPE analysis so in the following are described only the differences between them.

### Highlights

Differences in cuts:

- The signal peak must be over 5 times the standard deviation of the baseline
- Geocut: there is a geometrical cut at an adjustable radius around the center of the detector in order to take into account only the events in which the Cherenkov cone is totally contained in the active surface of the detector. `-g` is used to select the radius of the geocut, the default is 2mm.

### Description

When you are analyzing PE Runs you need the tracker information, so when the code gets the signal files it takes also the tracker files. After that, those files are sorted to couple the tracker data to the right signal. Then both files are "unpacked".

Then the code takes the spatial information from the `.dat` file and set the correct index for the event reconstructed.

After, the events not reconstructed are discarded and those who survive are checked to be good or bad. Signals can be bad if the rise time is less than the cut (E-9) or if the peak is not above the threshold mentioned before. The spatial information is now attached to the events that passed these tests, allowing the code to perform the geocut. The cut is a simple check if the distance between the particle impact point and the center of the detector is less than the selected radius, if is not the event is not taken into account. The fraction of events excluded is computed and printed.

In addition to the same plot of the SPE code, are drawn the 2D maps of charges, amplitudes, and rise times as a function of the position.

Then the fit part is the same as the SPE analysis.

## Analyze Timing Run

The code is divided into two parts for easy processing of data. `process_TIMErun.py` process the run and output a ROOT file with the output. The `analyze_TIMErun.py` take the raw data and applies the cut and performs the plotting.

### Processing

For now, no cuts are made so all the waveforms are passed.

### Analizing

Lorem ipsum.