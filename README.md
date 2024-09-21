# GRIP FORCE BEHAVIORAL DATA PROCESSING PIPELINE

---

Scripts to analyze behavioral data from the grip force/reward task used in Precision-BCT, ADAPT-PD (and maybe future?) projects. The pipeline is wrapped in a GUI, allowing to analyze one's data with little effort. There are two main flows of the pipeline:

- Single subject outcome visualization (incomplete, but most likely abandoned) - allows to visualize grip responses in various conditions. At the moment mainly used for data quality checks.

- Group analysis - outputs a table of detailed trial performance and estimations of relevant grip curve metrics - reaction times, maximum grip values etc. The output can be easily read by any statistical software.

---

## Getting started :beginner:

__Getting the scripts__ :arrow_down:

Originally, intended to sync two local repositories, but it proved to be more complicated than it was worth it. You can now get the latest scripts by using the following commands:

Navigate to the directory where you will store the scripts:

    cd <path to folder>

If you are here for the first time:

    // Clone the code from GitLab //
    git clone https://git.drcmr.dk/vytautasl/behavioral-data-analysis-toolbox.git

If you have already had UseTheForce and want to update the scripts to enjoy the latest new features:

    // Go to the directory where you store the scripts //
    git pull origin main

You can also later copy the scripts to other directories :) 

    cp -r <source_directory> <destination_directory>


## Setting things up :beginner:

To run the toolbox you will need some sort of IDE for Python (personal preference - VSCode, but you should be ok using Spyder or PyCharm). To run everything successfully you will need to set up Anaconda first.

__Getting Anaconda (stolen from wiki with zero shame)__ :snake:

Run the installer in /mnt/install (at the time of writing it's named /mnt/install/Anaconda3-2020.11-Linux-x86_64.sh, but this is subject to change -- it will always be named something obvious). When prompted to specify the install location, go with the default suggestion (e.g. /mrhome/rkv/anaconda3).

The installation may take a while, so go scan a subject or something.

After a while, you'll see the following:

    installation finished.
    Do you wish the installer to initialize Anaconda3
    by running conda init? [yes|no]
    [no] >>>

What it's asking here is basically whether or not you want the installer to make the conda command to be automagically available every time you start a new terminal. This involves running some code on every terminal start, and has been observed to substantially slow down startup in some cases.

__Getting your virtual environment ready (obviously stolen from wiki)__ :deciduous_tree:

Upon activating Anaconda, you will be placed in what's called the base environment (base). It contains some version of Python:

    $ conda info -e
    # conda environments:
    #
    base                  *  /mrhome/vytautasl/anaconda3

    $ which python
    ~/anaconda3/bin/python

    $ python -V
    Python 3.8.5

Observe that the asterisk denotes the currently active environment. You can create a new one - 'force' was in my case. For stability specify python=3.8.5 version as well:

    $ conda create -n force python=3.8.5
    Collecting package metadata (current_repodata.json): done
    ...
    Proceed ([y]/n)? y
    ...
    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    #
    #To activate this environment, use
    #
    #     $ conda activate force
    #
    # To deactivate an active environment and go back to (base), use
    #
    #     $ conda deactivate


We can now activate this environment and verify that the python command now corresponds to the version installed here:

    $ conda activate brainz
    $ conda info -e
    # conda environments:
    #
    base                     /mrhome/vytautasl/anaconda3
    force                 *  /mrhome/vytautasl/anaconda3/envs/force

    $ which python
    ~/anaconda3/envs/force/bin/python

    $ python -V
    Python 3.8.5



 ## IDE :computer:

To open the scripts you will need an IDE. If you decide to use VSCode, simply type 'code' into the command window. As soon as VSCode opens, you must take care of a few things (which should be a one time job):

- Navigate to the folder where your saved toolbox scripts are located.

```
File -> Open Folder -> 'load the folder'
```

- On the right side of the screen you should see all the toolbox files and subfolders listed. Open UseTheForce.py file by clicking on it. 

- Make sure on the lower right corner of the GUI you see the 3.8.5 Python version (interpreter), and in the brackets - your predefined virtual environment name from the previous steps - 'force' was in my case. If none of this is correct, do the following:
```
In the terminal of VSCode (Terminal->New Terminal) type: conda activate \your environment name\
```
You should see your environment name now
```
Press Ctrl+Shift+P (Cmd+Shift+P on Mac) and type 'interpreter' -> 
Press Select Interpreter -> 
Select your virtual environment (in my case - Python 3.8.5 ('force')
```

This action can also be performded using the terminal if you prefer.

__Recreate environment using requirements.txt__ :page_with_curl:

Toolbox comes with requirements.txt file that lists all required packages to successfully run the scripts. If you had your environment set up before, you most likely already have all the required packages. You probably also now have your conda environment to hold all the python libraries.

To install the dependencies, simply run

```
pip install -r /path/to/requirements.txt
``` 

The packages will be installed into your current environment


## Running the analysis :beginner:

### Single subject

*...in development...*


### Group analysis 
__Input folder preparations__

For the group analysis you will need to prepare a couple of things:

+ All the subject folders (X***** folders) should be moved to an analysis folder (you can create it anywhere and call it whatever) - this folder will also hold the analysis table and other outputs - the scipt will generate a new 'Results' folder once the analysis is done.

+ Create a single .xlsx file with any name. Place it next to the subject folders. Every line in this file should be dedicated to a subject. It should look something like this:

|id|data|delay|gender|age|group|calibration|
|:----|:----|:----|:----|:----|:----|:----|
|X*****|1|60|Female|25|1|EEG|
|X*****|0|60|Female|21|2|MRI|
|X*****|1|60|Female|26|1|MRI|
|X*****|1|60|Male |29|3|BEH|

These 7 columns are required. You can add additional ones, specifying new parameters for each subject - like disease onset, handedness score etc. All the additional measures will be appended to the final output.

+ **id** - specify your subject identifier.
+ **data** - should data be analyzed. 1 for yes. All other values will force the analysis to exclude the subject on that row.
+ **delay** - in our experiment we had a projector delay of 60 ms. To account for that, 'delay' rows should hold a number in miliseconds of how much of delay to add for each participant. Otherwise, place 0.
+ **gender** - gender of the participant.
+ **age** - age of the participant.
+ **group** - subject group (healthy, patient etc., your job is to remember which number is which).
+ **calibration** - to transform the data into Newton format, each subject must have a label from one of the following: MRI,BEH or EEG. Depending on your experiment, insert an appropriate label for each subject to adjust for specific devices.

The input folder should look similar to this:

    ├── excel_file_mentioned_above.xlsx
    ├── sub-01
    │   ├── Questionnaires
    │   │   ├── EHI_Sub_01_.csv
    │   ├── Rest
    │   │   └── source_data
    │   └── Task
    │       └── source_data
    │           ├── data_task_sub-01_run_1.mat
    │           ├── data_task_sub-01_run_1.txt
    │           ├── data_task_sub-01_run_2.mat
    │           ├── data_task_sub-01_run_2.txt
    │           ├── data_task_sub-01_run_3.mat
    │           ├── data_task_sub-01_run_3.txt
    │           ├── data_task_sub-01_run_4.mat
    │           ├── data_task_sub-01_run_4.txt
    │           └── ExpInfo_task_sub-01.mat
    └── sub-02
        ├── Questionnaires
        │   ├── EHI_Sub_01_.csv
        ├── Rest
        │   └── source_data
        └── Task
            └── source_data
                ├── data_task_sub-02_run_1.mat
                ├── data_task_sub-02_run_1.txt
                ├── data_task_sub-02_run_2.mat
                ├── data_task_sub-02_run_2.txt
                ├── data_task_sub-02_run_3.mat
                ├── data_task_sub-02_run_3.txt
                ├── data_task_sub-02_run_4.mat
                ├── data_task_sub-02_run_4.txt
                └── ExpInfo_task_sub-02.mat

Always to keep in mind:

    1. Make sure the paths to the .mat or .txt files are correct.
    2. Do not allow any duplicate files of an experiment run as it can lead to unforeseen outputs.
    3. Multiple ExpInfo files for a subject are allowed, but keep in mind UseTheForce is not selective - it will pick the first ExpInfo file it encounters, so if that file does not hold the correct information, it can lead to wrong estimates.



__Run the analysis__

If you completed the steps above, it should simply work by running UseTheForce.py file. When the GUI opens, press 'Load group', navigate to your analysis folder that contains all subject folders and a single .xlsx file, and the analysis should start. Depending on the number of runs and subjects, it might take a while.

__Preprocessing__

The preprocessing was done following (Le Bouc et al., 2016)

    The events of each task run were analyzed separately. The grip device data were non-uniformly sampled and hence interpolated to 120 Hz. Each event was baseline corrected and low-pass filtered at 15 Hz using a zero-phase second-order Butterworth filter... (Labanauskas V. et al., manuscript)


## Output
The output can be found inside your data folder, inside folder Results. Here is an example tree:

    ├─ behavioral_group_output.xlsx
    ├── grips.mat
    ├── slopes.mat
    ├── sub-01
    │   ├── force_preprocessed.mat
    │   ├── force_preprocessed_newton.mat
    │   ├── raw_force.mat
    │   ├── slope_preprocessed.mat
    │   ├── slope_preprocessed_newton.mat
    │   └── sub-01_responses.pdf
    ├── sub-02
    │   ├── force_preprocessed.mat
    │   ├── force_preprocessed_newton.mat
    │   ├── raw_force.mat
    │   ├── slope_preprocessed.mat
    │   ├── slope_preprocessed_newton.mat
    │   └── sub-02_responses.pdf

The main output of the analysis is stored inside behavioral_group_output.xlsx file. Each row is a single recorded trial.

The headers of behavioral_group_output.xlsx:
+ **id** - subject id	
+ **delay** - what time delay was applied	
+ **group** - subject group	
+ **SubjectNr** - subject number in analysis	
+ **age** - subject age	
+ **gender** - subject gender	
+ **calibration** - used calibration method
+ **Run** - run number	
+ **BlockNr** - block number	
+ **TrialNr** - trial number in a run	
+ **TotalTrialNr** - trial number in the experiment	
+ **FaceGender** - emotional face gender (1 - 'Male',2 - 'Female')	
+ **FaceEmotion** - face emotion (-1 - 'sad', 0 - 'neutral', 1 - 'happy')	
+ **RewardPromise** - reward prospect condition in a block (1 - 'high reward prospect', -1 - 'low reward prospect')	
+ **RewardReceived** - money won or lost in the trial	
+ **SymbolTarget** - action cue (-1 - 'left go', 1 - 'right go', 0 - 'nogo')	
+ **GripResponse** - participant response to action cue	(-1 - 'left go', 1 - 'right go', 0 - 'nogo')	
+ **Correct** - was the trial registered as correct? (1 - yes, 0 - no; participants were allowed to correct their incorrect responses inside the response window)	
+ **Mirror** - was the other hand pressed? (1 - yes, 0 - no; responses had to exceed the 30 % threshold). Confirm in pdf files. 	
+ **RT_init** - reaction time at the response onset, s. RT_init was measured by detecting 5 consecutive increases in force that also exceed a hand threshold, then tracing back the same number of data points from where both conditions are met to determine the reaction time	
+ **RT_acc** - reaction time at maximum acceleration, s		
+ **RT_99** - reaction time at 99% of peak, s. It was calculated by detecting the largest peak in the data, then calculating the time to the onset of the peak at 99% of its relative height using scipy.signal.find_peaks
+ **RT_95** - reaction time at 95% of peak, s. It was calculated by detecting the largest peak in the data, then calculating the time to the onset of the peak at 95% of its relative height using scipy.signal.find_peaks
+ **RiseTime** - response increase duration from 10% to 90% of the whole force curve, s		
+ **FallTime** - response decrease duration from 90% to 10% of the whole force curve, s	
+ **MaxGrip** - maximum grip, a.u.	
+ **MaxGrip_Norm** - maximum grip, a.u.	(normalized data)
+ **MaxGrip_New** - maximum grip, Newtons.	
+ **MaxTime** - maximum grip time from stimulus onset, s	
+ **Slope** - maximum response slope, a.u./s. Calculated as the first time derivative.	
+ **Slope_Norm** - maximum response slope, a.u./s (normalized data)		
+ **Slope_New**	- maximum response slope, Newton/s
+ **DeSlope** - maximum slope on signal decrease, a.u./s	
+ **DeSlope_Norm** - maximum slope on signal decrease, a.u./s (normalized data)	
+ **DeSlope_New** - maximum slope on signal decrease, Newton/s	
+ **SettlingTime** - time for the signal to return to baseline after response, s		
+ **AUC** - area under response curve
+ **AUC_Norm** - area under response curve (normalized data)		
+ **GripLength** - time from grip onset to return to baseline, s		
+ **Acceleration** - maximum response acceleration, a.s/s2	
+ **Acceleration_Norm** - maximum response acceleration, a.s/s2 (normalized data)	
+ **Acceleration_New** - maximum response acceleration, Newton/s2
+ **DeAcceleration** - maximum acceleration at signal decrease, a.u/s2	
+ **DeAcceleration_Norm** - maximum acceleration at signal decrease, a.u/s2 (normalized data)
+ **DeAcceleration_New** - maximum acceleration at signal decrease, Newton/s2	
+ **MaxNOGOleft** - maximum left hand grip at nogo cue, a.u	
+ **MaxNOGOleft_Norm** - maximum left hand grip at nogo cue, a.u (normalized data)	
+ **MaxNOGOright** - maximum right hand grip at nogo cue, a.u	
+ **MaxNOGOright_Norm** - maximum right hand grip at nogo cue, a.u (normalized data)	
+ **AucNOGOleft** - left hand area under the curve at nogo cue, a.u	
+ **AucNOGOleft_Norm** - left hand area under the curve at nogo cue, a.u (normalized data)
+ **AucNOGOright** - right hand area under the curve at nogo cue, a.u	
+ **AucNOGOright_Norm** - right hand area under the curve at nogo cue, a.u (normalized data)	
+ **MaxANTleft** - left hand maximum grip during reward anticipation, a.u	
+ **MaxANTleft_Norm** - left hand maximum grip during reward anticipation, a.u (normalized data)	
+ **MaxANTright** - right hand maximum grip during reward anticipation, a.u	
+ **MaxANTright_Norm** - left hand maximum grip during reward anticipation, a.u (normalized data)	
+ **AucANTleft** - left hand area under the curve during anticipation, a.u	
+ **AucANTleft_Norm** - left hand area under the curve during anticipation, a.u (normalized data)	
+ **AucANTright** - right hand area under the curve during anticipation, a.u	
+ **AucANTright_Norm** - right hand area under the curve during anticipation, a.u (normalized data)	

Additionally, if in the input .xlsx file you have added other columns, such as questionnaire measures, they are appended at the end of these columns.

Other files:

+ **grips.mat** - contains preprocessed force measures of correct grips (output) and time measures to align the data (time) The data is vertically stacked, but can be mapped to specific trials or groups, by filtering behavioral_group_output.xlsx excluding NoGo, incorrect and mirror trials. Intended for presentations.

+ **slopes.mat** - contains preprocessed slope measures of correct grips (output) and time measures to align the data (time) The data is vertically stacked, but can be mapped to specific trials or groups, by filtering behavioral_group_output.xlsx excluding NoGo, incorrect and mirror trials. Intended for presentations.

+ **raw_force.mat** - contains raw force measures of each trial (from the ITI onset to the reward onset). Each trial is stored. The data is separated into left and right hands, as well as the time measure (unadjusted).

+ **force_preprocessed.mat** - preprocessed force data (from the ITI onset to the reward onset). Each trial is stored. The data is separated into left and right hands, as well as the time measure (unadjusted).

+ **force_preprocessed_newton.mat** - preprocessed force data transformed into Newtons (from the ITI onset to the reward onset). Each trial is stored. The data is separated into left and right hands, as well as the time measure (unadjusted).

+ **slope_preprocessed.mat** - preprocessed slope data (from the ITI onset to the reward onset). Each trial is stored. The data is separated into left and right hands, as well as the time measure (unadjusted).

+ **slope_preprocessed_newton.mat** - preprocessed slope data transformed into Newtons (from the ITI onset to the reward onset). Each trial is stored. The data is separated into left and right hands, as well as the time measure (unadjusted).

+ **sub-xx_responses.pdf** - visualized subject specific trials. All preprocessed trials are presented (from stimulus onset + 2 sec). The top row displays data in arbitrary units, the lower row - the same output but in Newtons. The suptitle shows group, participant id, task run, trial and the requested response. Blue colored line - force in the task requested hand. Light blue colored line - the opposite hand. Pink colored line - force changes (slope) for the blue colored line (not calculated in NoGo trials). Black dashed line - minimum threshold. X - stimulus onset. Red dot - RT_init. Light purple dot - RT99. Dark purple dot - RT95. Yellow dot - maximum slope. Green dot - maximum force. **Recommended: inspect each individual trial as no pipeline is fail proof.**