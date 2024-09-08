import os,re
from collections import defaultdict
from glob import glob
import scipy.io as sio 
from colorama import Back,Style
from functions.dataCheckAndGet.matRecovery import data_recovery

def qualityCheck(subject_folder_path):
    
    #Get ExpInfo file
    try:
        exp_info_path = glob(os.path.join(subject_folder_path,'*ExpInfo*'))
        exp_info=sio.loadmat(exp_info_path[0])
        print('At least one *ExpInfo* file was found. Always make sure there are no duplicate files!')
        totBlcNr = int(exp_info['Blocks_in_run'])
        evntBlc  = int(exp_info['Events_in_block'])
    except:
        print('*ExpInfo* file was not found')

    data_to_get,list_of_blocks = [],[0]
    print('\nData files in the subject folder:')
    for file in sorted(os.listdir(subject_folder_path)):
        if file.endswith('.mat') and file.startswith('data_'):
            
            data_check=sio.loadmat((subject_folder_path+'/'+file))
            
            if (len(data_check['Trial_Nr'][0]) == (totBlcNr*evntBlc)) and ('Block_time' in data_check): #all data saved well
                print(Back.GREEN + file + '|| File status:OK ||' + Style.RESET_ALL)
                data_to_get.append((subject_folder_path+'/'+file))
                
            elif 'Block_time' not in data_check: 
                #experiment crashed at the end and mat file did not save properly, will attempt to look for a txt file
                print(Back.YELLOW + file + '|| FILE IS INCOMPLETE (possible failed save) ||' + Style.RESET_ALL)
                try:
                    print('Attempting to locate a \'txt\' file')
                    output = data_recovery(subject_folder_path,file)
                    data_check=sio.loadmat((subject_folder_path+'/'+output))
                    #data_to_get.append((subject_folder_path+'/'+output))
                except:
                    print('Recovery failed. Check if relevant txt file exists, otherwise remove the run')
            
            elif len(data_check['Trial_Nr'][0]) < totBlcNr*evntBlc:
                print(Back.RED + file + '|| VALUES MISSING ||' + Style.RESET_ALL)
                data_to_get.append((subject_folder_path+'/'+file))
                
            else:
                print(Back.BLUE + file + '|| MERGED DATA ||' + Style.RESET_ALL)
                data_to_get.append((subject_folder_path+'/'+file))
                
            list_of_blocks.append(list_of_blocks[-1]+len(data_check['Block_time'][0]))
    print('\n')
    return totBlcNr,evntBlc,exp_info,list_of_blocks,data_to_get

def getData(subject_folder_path,data_to_get):
    # Load data_***.mat files
    data,run_list = [],[]
    run_nr=0
    for file in data_to_get:#sorted(os.listdir(subject_folder_path)):
        #if file.endswith('.mat') and file.startswith('data_'):
        data.append(sio.loadmat(file))
        run_nr += 1
        m=re.search('run_(\d+)', file, re.IGNORECASE)
        run_list.append(m.group(1))
    
    merged_data = defaultdict(list)
    for d in data:
        for k, v in d.items():
            merged_data[k].append(v)
    print('Data copied')
    
    return merged_data,run_list,run_nr
        

    
    
    
    
    


    