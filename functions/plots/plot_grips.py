# Function to plot force_curves.mat data
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import re,os

###########################################################################################

def plotGrips(savepath,slope_output,curve_output,question_table):
    
    group_nr = question_table['group'].dropna().unique()
    group_nr = group_nr.astype(int)
    
    data_keys = list(curve_output.keys())
    
    for i, key in enumerate(data_keys):
        fig = plt.figure() 
        mean = np.mean(np.array(curve_output[key]),axis=0)
        for p in curve_output[key]:
            plt.plot(p,linestyle='dashed', alpha=0.2)
            
        plt.plot(mean, color='black', linewidth=3)
        plt.ylim([-20,220])
        plt.ylabel('Force output, Newton',fontsize=15)
        title = re.match(r'([a-zA-Z]+)', key).group(1)
        plt.title(title,fontsize=15, fontweight='bold')
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        plt.savefig(os.path.join(savepath,'Group_{}_{}.png'.format(int(re.search(r'\d+$', key).group()),title)))
        
    for i, key in enumerate(data_keys):
        fig = plt.figure() 
        mean = np.mean(np.array(slope_output[key]),axis=0)
        for p in slope_output[key]:
            plt.plot(p,linestyle='dashed', alpha=0.2)
              
        plt.plot(mean, color='black', linewidth=3)
        plt.ylim([-.3,.3])
        plt.ylabel('Slope, Newton/s',fontsize=15)
        title = re.match(r'([a-zA-Z]+)', key).group(1)
        plt.title(title,fontsize=15, fontweight='bold')
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        plt.savefig(os.path.join(savepath,'Slope_Group_{}_{}.png'.format(int(re.search(r'\d+$', key).group()),title)))
        
