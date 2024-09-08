import numpy
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt

def plotITI(self,merged_data,exp_info,left,right,times,list_of_blocks,runs,fig):
    self.button_save.state(['!disabled'])
    for widget1,widget2 in zip(self.plot_frame.winfo_children(),self.tool_frame.winfo_children()):
        widget1.destroy()
        widget2.destroy()
    fig,axs = plt.subplots(2,runs, figsize=(15,10), sharey=True)
    fig.suptitle('Averaged baseline ITIs through the experiment', fontsize=20)
    plt.setp(axs,ylim=(-.1,1))
    for i in range(runs):
        left_iti, right_iti = [],[]
        left_run = numpy.asarray(numpy.reshape((numpy.concatenate(left[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        right_run = numpy.asarray(numpy.reshape((numpy.concatenate(right[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        time_run = numpy.asarray(numpy.reshape((numpy.concatenate(times[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        iti_run = merged_data['ITI_onset'][i]
        stim_run = merged_data['Stimulus_Onset'][i]
        for event in range(iti_run.size):
            idx_iti_onset = (numpy.abs(time_run - iti_run[0][event])).argmin()
            idx_stim_onset = (numpy.abs(time_run - stim_run[0][event])).argmin()
            left_iti.append(numpy.mean(left_run[idx_iti_onset:idx_stim_onset]))
            right_iti.append(numpy.mean(right_run[idx_iti_onset:idx_stim_onset]))
            axs[0,i].scatter(event,left_iti[event])
            axs[1,i].scatter(event,right_iti[event])
        axs[0,i].set_title('Run {}'.format(i+1))
        axs[0,i].axhline(float(exp_info['Error_threshold_left']),color='red',ls='--')
        axs[1,i].axhline(float(exp_info['Error_threshold_right']),color='red',ls='--')
        axs[0,i].set(ylabel='Average left hand force output')
        axs[1,i].set(xlabel='Event nr.', ylabel='Average right hand force output')
        del iti_run, time_run
    for ax in axs.flat:
        ax.label_outer()
    canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
    canvas.draw()
    self.plot_frame.pack_propagate(False)
    canvas._tkcanvas.pack(fill=tk.BOTH, expand=0)

    toolbar = NavigationToolbar2Tk(canvas, self.tool_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=0)