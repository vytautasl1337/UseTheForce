'''
Just work in progress script.
As the amount of data increases, this script should append new subjects 
you added in recent experiments to the ones you processed before.
This will only work if there is only single sheet in the file

How it works:
    1. Pre-process new subject(s) as you usually do - for this you need to create 
        new folder, with subject folders and .xlsx file (just like usual)
    2. Make sure .xlsx file only process new data ('data' column 1)
    3. As soon as it is done, run this script. Make sure you enter the directories 
        correctly (parent path is the old output, child path is a path to the new output 
        you wish to append to the parent).Number of columns must also match.
    4. Output will be saved in the parent directory (_updated.xlsx or change to whatever
        you want)
'''

import os
import pandas as pd

# Parent folder (which has the majority of your subjects to append TO)
parent_path = '/mnt/projects/PBCTI/combined/Results/Group_output_202402081541/'
parent_file = pd.read_excel(os.path.join(parent_path,'behavioral_group_output.xlsx'))

# Child folder (new pre-processed subjects which you want to append to the parent)
child_path = '/mnt/projects/PBCTI/combined/Results/Group_output_202402081112/'
child_file = pd.read_excel(os.path.join(child_path,'behavioral_group_output.xlsx'))

merged_df = pd.concat([parent_file,child_file])

# saves file in parent_path but can be changed to anywhere
with pd.ExcelWriter(os.path.join(parent_path,'behavioral_group_output_updated.xlsx'), 
                    engine='openpyxl') as writer:
    merged_df.to_excel(writer, index=False)
    
    






