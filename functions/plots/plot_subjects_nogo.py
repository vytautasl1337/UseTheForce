import matplotlib,mpl_axes_aligner,numpy
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import LogFormatterSciNotation
#from functions.dictionary_values.addValues import updateSubjectsDictionary


def plot2pdf_nogo(pdf,question_table,data_dict,data_newton1,data_newton2,
                    data1,data2,time_event_corr,i_time_event,sample_rt,
                    event,subject,time_,stim_pos_,iter_):
    
    PLOT_COLOR = ['blue','skyblue']
    
    stim_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stim_pos_-time_)))
    end_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stim_pos_-time_+2))) #2 seconds from stimulus
    
    # Get time event
    x_ = time_event_corr[stim_pos[0]:end_pos[0]] 
    
    # Correct so each trial starts at 0
    time_event_corr_ = [x-x_[0] for x in x_]

    # Get data values from devices

    data_plot_newton1 = data_newton1[stim_pos[0]:end_pos[0]]
    data_plot_newton2 = data_newton2[stim_pos[0]:end_pos[0]] 
    
    data_plot1 = data1[stim_pos[0]:end_pos[0]]
    data_plot2 = data2[stim_pos[0]:end_pos[0]] 

    y_axes1 = [data_plot1,data_plot2]
    y_axes2 = [data_plot_newton1,data_plot_newton2]
    

    fig, ((ax1, ax2)) = plt.subplots(2, 1, sharex=True)
    fig.suptitle('Group {}. Participant {}: Run {}. Trial {}. NoGo'.format(int(question_table['group'][subject]),
                                                                              question_table['id'][subject],
                                                                            iter_,event+1), fontsize=14, 
                                                                            fontweight='bold')
    
    plt.xlabel('Time, s', fontsize=15)
    

    ax1.plot(time_event_corr_,y_axes1[0], color = PLOT_COLOR[0], zorder=0,linestyle='dashed')
    ax1.plot(time_event_corr_,y_axes1[1], color = PLOT_COLOR[1], zorder=0)
    ax2.plot(time_event_corr_,y_axes2[0], color = PLOT_COLOR[0], zorder=0,linestyle='dashed')
    ax2.plot(time_event_corr_,y_axes2[1], color = PLOT_COLOR[1], zorder=0)
    
    ax1.set_ylim(-1,1)
    ax2.set_ylim(-200,200)
        
    ax1.set_ylabel('Force output, a.u.', color = 'blue', fontsize=13)
    ax2.set_ylabel('Force output (Newtons)', color = 'blue', fontsize=13)
    
    
    plt.gca().yaxis.set_major_formatter(LogFormatterSciNotation(base=10,minor_thresholds=(numpy.inf,numpy.inf),labelOnlyBase=False))
    
    #mpl_axes_aligner.align.yaxes(ax1, 0, ax12, 0, 0.5) #aligns ax and ax2 axes at 0, in the middle of y axis
    #mpl_axes_aligner.align.yaxes(ax2, 0, ax22, 0, 0.5) 

    fig.tight_layout()
    pdf.savefig()
    plt.close(fig)
    

    