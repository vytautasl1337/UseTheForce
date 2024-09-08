import numpy
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt

def plotRuns(self,exp_info,left,right,times,list_of_blocks,runs,fig):
    self.button_save.state(['!disabled'])
    for widget1,widget2 in zip(self.plot_frame.winfo_children(),self.tool_frame.winfo_children()):
        widget1.destroy()
        widget2.destroy()
    fig,axs = plt.subplots(2,runs, figsize=(15,10), sharey=True)
    fig.suptitle('Participant responses through the experiment', fontsize=20)
    plt.setp(axs,ylim=(-.1,1))
    for i in range(runs):
        left_data = numpy.reshape((numpy.concatenate(left[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1)
        right_data = numpy.reshape((numpy.concatenate(right[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1)
        time_series = numpy.reshape((numpy.concatenate(times[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1)
        axs[0,i].plot(time_series,left_data)
        axs[0,i].set_title('Run {}'.format(i+1))
        axs[0,i].axhline(float(exp_info['Error_threshold_left']),color='red',ls='--')
        axs[0,i].set(ylabel='Left hand force output')
        axs[1,i].plot(time_series,right_data)
        axs[1,i].axhline(float(exp_info['Error_threshold_right']),color='red',ls='--')
        axs[1,i].set(xlabel='Time, s', ylabel='Right hand force output')
    for ax in axs.flat:
        ax.label_outer()
    canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
    canvas.draw()
    self.plot_frame.pack_propagate(False)
    canvas._tkcanvas.pack(fill=tk.BOTH, expand=0)

    toolbar = NavigationToolbar2Tk(canvas, self.tool_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=0)