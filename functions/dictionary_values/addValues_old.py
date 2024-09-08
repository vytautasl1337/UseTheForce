import random
import string
import numpy

def addValues(question_table,subject,data_dict):
    
    for key,item_list in data_dict.items():
        if key in question_table:
            item_list.append(question_table[key][subject])
            
    return data_dict


def createGroupDictionary(question_table):
    
    group_nr = question_table['group'].dropna().unique()
    group_nr = group_nr.astype(int)
    
    hands = ['Left','Right']
    curve_output,slope_output={},{}
    
    for grp in group_nr:
        force_dict,slope_dict = {},{}
        for hand in hands:
            key = f'{hand}{grp}'
            force_dict[key] = []
            slope_dict[key] = []
        curve_output.update(force_dict)
        slope_output.update(slope_dict)
        
    return curve_output,slope_output

def updateGroupDictionary(curve_output,slope_output,data_plot_newton,slope_newton,question_table,subject,curr_resp):
    
    grp = int(question_table['group'][subject])
    key = f'{curr_resp}{grp}'
    
    curve_output[key].append(data_plot_newton)
    slope_output[key].append(slope_newton)
    
    return curve_output,slope_output
    
    