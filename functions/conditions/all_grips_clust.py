import numpy
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt

def all_grips_clust(self,merged_data,left,right,times,list_of_blocks,runs,fig):
    self.button_save.state(['!disabled'])
    for widget1,widget2 in zip(self.plot_frame.winfo_children(),self.tool_frame.winfo_children()):
        widget1.destroy()
        widget2.destroy()
    fig,axs = plt.subplots(2,1, figsize=(15,10), sharey=True)
    fig.suptitle('Clustered responses (all)', fontsize=20)
    plt.setp(axs,ylim=(-.1,1))
    for i in range(runs):
        left_run = numpy.asarray(numpy.reshape((numpy.concatenate(left[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        right_run = numpy.asarray(numpy.reshape((numpy.concatenate(right[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        time_run = numpy.asarray(numpy.reshape((numpy.concatenate(times[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
        iti_run = merged_data['ITI_onset'][i]
        ant_run = merged_data['Trial_Reward_Onset'][i]
        for event in range(ant_run.size):
            idx_iti_onset = (numpy.abs(time_run - iti_run[0][event])).argmin()
            idx_ant_onset = (numpy.abs(time_run - ant_run[0][event])).argmin()               
            axs[0].plot(left_run[idx_iti_onset:idx_ant_onset])
            axs[1].plot(right_run[idx_iti_onset:idx_ant_onset])
        #axs[0,1].set_title('Run {}'.format(i+1))
        axs[0].set(ylabel='Left hand force output')
        axs[1].set(xlabel='X', ylabel='Right hand force output')
    for ax in axs.flat:
        ax.label_outer()
    canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
    canvas.draw()
    self.plot_frame.pack_propagate(False)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.X, expand=0)

    toolbar = NavigationToolbar2Tk(canvas, self.tool_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=0)