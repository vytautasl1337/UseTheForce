# A python script to recover missing mat files from txt files
from scipy.io import savemat
import scipy.io as sio 
import os

def data_recovery(subject_folder_path,file):
    
    txt_file = file.replace('.mat', '.txt')
    with open((subject_folder_path+'/'+txt_file), 'r') as file2:
        txt_data = file2.read()
    print('A replacement file found')
    
    file_dict = {}
    
    for var in txt_data.split('\n'):
        if var:
            key, values = var.split(' : ')
            file_dict[key.strip()] = eval(values.strip())
    
    index = file.index('.mat')
    output = file[:index] + '_recovered' + file[index:]
    sio.savemat(os.path.join(subject_folder_path,output), file_dict)
    
    print(txt_file, ' saved as ',output)

    return output