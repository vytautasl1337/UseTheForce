import random
import string
import numpy

def addValues(question_table,subject,data_dict):
    
    for key,item_list in data_dict.items():
        if key in question_table:
            item_list.append(question_table[key][subject])
            
    return data_dict


def createSubjectsDictionary(question_table):
    
    # Every trial will be saved by row
    raw_force_output,force_preprocessed,slope_preprocessed, force_preprocessed_newton, slope_preprocessed_newton={},{},{},{},{}
    ref_dict={}
    for key in ['time','left','right']:
        ref_dict[key] = []
    
        raw_force_output[key] = list(ref_dict[key])
        force_preprocessed[key] = list(ref_dict[key])
        slope_preprocessed[key] = list(ref_dict[key])
        force_preprocessed_newton[key] = list(ref_dict[key])
        slope_preprocessed_newton[key] = list(ref_dict[key])
        
    return raw_force_output,force_preprocessed,slope_preprocessed,force_preprocessed_newton,slope_preprocessed_newton

def createGroupOutputs():
    slopes_dict, grips_dict = {},{}
    ref_dict={}
    for key in ['time','output']:
        ref_dict[key] = []
    
        slopes_dict[key] = list(ref_dict[key])
        grips_dict[key] = list(ref_dict[key])
    return slopes_dict,grips_dict

    
    