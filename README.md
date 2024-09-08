# GRIP FORCE BEHAVIORAL DATA PROCESSING PIPELINE

---

Scripts to analyze behavioral data from the grip force/reward task used in Precision-BCT and ADAPT-PD projects. The pipeline is wrapped in a GUI, allowing researchers to analyze their data with little effort. There are two main flows of the pipeline:

- Single subject outcome visualization (in development, incomplete) - allows to visualize grip responses in various conditions. At the moment mainly used for data quality checks.

- Group analysis (in development) - outputs a table of detailed trial performance and estimations of relevant grip curve metrics - reaction times, maximum grip values etc. The output can be easily read by any statistical software.

---

## Getting started :beginner:

__Getting the scripts__ :arrow_down:

So... you decided to enter the world of pain and start analyzing your data. Originally, intended to sync two local repositories, but it proved to be more complicated than it was worth it. You can now get the latest scripts by using the following commands:

Navigate to the directory where you will store the scripts:

    cd <path to folder>

If you are here for the first time:

    // Clone the code from GitLab //
    git clone https://git.drcmr.dk/vytautasl/behavioral-data-analysis-toolbox.git

If you want to update the scripts to enjoy the latest new features:

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

__Recreate environment using requirements.yml__ :page_with_curl:

Toolbox comes with requirements.yml file that lists all required packages to successfully run the scripts. If you had your environment set up before, you most likely already have all the required packages. You probably also now have your conda environment to hold all the python libraries.

```
# Re-create the environment
$ conda env create --file requirements.yml
# Activate new environment
$ conda activate your_environment_name
``` 

The packages will be installed into your current environment


## Running the analysis :beginner:

### Single subject

*...in development...*


### Group analysis 
__Preparations__

For the group analysis you will need to prepare a couple of things:

+ All the subject folders (X***** folders) should be moved to an analysis folder (you can create it anywhere and call it whatever) - this folder will also hold the analysis table and other outputs - inside a new 'Results' folder.

+ Create a single .xlsx file with any name. Every line should be dedicated subject. The toolbox will also look for a few columns. It should look something like this:

|id|data|delay|gender|age|group|calibration|
|:----|:----|:----|:----|:----|:----|:----|
|X*****|1|60|Female|25|1|EEG|
|X*****|0|60|Female|21|2|MRI|
|X*****|1|60|Female|26|1|MRI|
|X*****|1|60|Male |29|3|BEH|

These 7 columns are required. You can add additional ones, specifying new parameters for each subject - like disease onset, handedness score etc. All them will be taken and present in the final output.

+ **id** - specify your subject identifier.
+ **data** - should data be analyzed. 1 for yes. All other values will force the analysis to exclude the subject on that row.
+ **delay** - in our MRI experiment we had a projector delay of 60 ms. To account for that, 'delay' rows should hold a number in miliseconds of how much of delay to add for participant.
+ **gender** - gender of the participant
+ **age** - age of the participant
+ **group** - subject group (healthy, patient etc., your job is to remember which number is which)
+ **calibration** - to transform the data into Newton format, each subject must have a label from one of the following: MRI,BEH or EEG. Depending on your experiment, insert an appropriate label for each subject to adjust for specific devices.


__Run the analysis__

If you completed the steps above, it should simply work by running UseTheForce.py file. When the GUI opens, press 'Load group', navigate to your analysis folder that contains all subject folders and a single .xlsx file, and the analysis should start. Depending on the number of runs and subjects, it might take a while.

## Output
The output can be found inside your subjects' folder. The toolbox created a separate Results folder. The analysis run will create a folder 'Group_output' including the analysis time. Inside you will find subject specific pdf files, where you can inspect subject responses (recommended). 

The data for analysis is stored inside behavioral_group_output.xlsx file. Each row is a single recorded trial.

The headings:
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
+ **Correct** - was the trial registered as correct? (1 - yes, 0 - no; participants were able to correct incorrect responses inside response window)	
+ **Mirror** - was the other hand pressed? (1 - yes, 0 - no; responses had to exceed the 30 % threshold) 	
+ **RT_init** - reaction time at the response onset, s		
+ **RT_acc** - reaction time at maximum acceleration, s		
+ **RT_knee** - reaction time as calculated by kneed algorithm, s	
+ **RiseTime** - response increase duration from 10% to 90%, s		
+ **FallTime** - response decrease duration from 90% to 10%, s	
+ **MaxGrip** - maximum grip, a.u.	
+ **MaxGrip_Norm** - maximum grip, a.u.	(normalized data)
+ **MaxGrip_New** - maximum grip, Newtons.	
+ **MaxTime** - maximum grip time from stimulus onset, s	
+ **Slope** - maximum response slope, a.u./s	
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

Additionally, the file includes other information, which (if) was provided in the analysis xlsx file.

