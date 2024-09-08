import matplotlib,mpl_axes_aligner,numpy
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import LogFormatterSciNotation
#from functions.dictionary_values.addValues import updateSubjectsDictionary


def plot2pdf(pdf,question_table,slopes_dict,grips_dict,data_dict,data_newton,data_not_used_newton,
             data,data_not_used,time_event_corr,i_time_event,sample_rt,min_response,
             event,subject,time_,stim_pos_,iter_,curr_resp):
    
    PLOT_COLOR = ['blue','skyblue','pink']
    DOT_COLOR = ['red','purple','magenta','green','orange']
    TEXT = ['RT_init','RT_95','RT_99','','']

    #DOT_TEXT = ['Reaction time','Max grip','Max slope']
    
    stim_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stim_pos_-time_)))
    end_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stim_pos_-time_+2))) #2 seconds from stimulus
    
    # Get time event
    x_ = time_event_corr[stim_pos[0]:end_pos[0]] 
    
    # Correct so each trial starts at 0
    time_event_corr_ = [x-x_[0] for x in x_]

    # Get data values from devices

    data_plot_newton = data_newton[stim_pos[0]:end_pos[0]]
    data_not_used_plot_newton = data_not_used_newton[stim_pos[0]:end_pos[0]] 
    data_plot = data[stim_pos[0]:end_pos[0]]
    data_not_used_plot = data_not_used[stim_pos[0]:end_pos[0]] 
    
    grips_dict['output'].append(data_plot_newton)
    grips_dict['time'].append(time_event_corr_)
    
    slope = numpy.gradient(data_plot,sample_rt).tolist()
    slope_newton = numpy.gradient(data_plot_newton,sample_rt).tolist()
    
    slopes_dict['output'].append(slope_newton)
    slopes_dict['time'].append(time_event_corr_)
    
    slope_ymax = numpy.max(slope)
    xpos = slope.index(slope_ymax)
    slope_xmax = time_event_corr_[xpos] 
    
    slope_ymax_newton = numpy.max(slope_newton)
    xpos_newton = slope_newton.index(slope_ymax_newton)
    slope_xmax_newton = time_event_corr_[xpos_newton] 

    y_axes1 = [data_plot,data_not_used_plot,slope]
    y_axes2 = [data_plot_newton,data_not_used_plot_newton,slope_newton]
    
    # y_scatter = [0,data_dict['MaxGrip'][-1],slope_ymax]
    # y_scatter_newton = [0,data_dict['MaxGrip_New'][-1],slope_ymax_newton]
    
    # x_scatter = [data_dict['RT_init'][-1] + stim_pos_-time_-x_[0],
    #                 data_dict['MaxTime'][-1] + stim_pos_-time_-x_[0],
    #                 slope_xmax,
    #             ]
    # x_scatter_newton = [data_dict['RT_init'][-1] + stim_pos_-time_-x_[0],
    #             data_dict['MaxTime'][-1] + stim_pos_-time_-x_[0],
    #             slope_xmax_newton,
    #         ]
    
    # to plot all available RT times!!!
    y_scatter = [0,0,0,data_dict['MaxGrip'][-1],slope_ymax]
    y_scatter_newton = [0,0,0,data_dict['MaxGrip_New'][-1],slope_ymax_newton]
    
    x_scatter = [data_dict['RT_init'][-1] + stim_pos_-time_-x_[0],
                 data_dict['RT_95'][-1] + stim_pos_-time_-x_[0],
                 data_dict['RT_99'][-1] + stim_pos_-time_-x_[0],
                data_dict['MaxTime'][-1] + stim_pos_-time_-x_[0],
                slope_xmax,
                ]
    x_scatter_newton = [data_dict['RT_init'][-1] + stim_pos_-time_-x_[0],
                        data_dict['RT_95'][-1] + stim_pos_-time_-x_[0],
                        data_dict['RT_99'][-1] + stim_pos_-time_-x_[0],
                        data_dict['MaxTime'][-1] + stim_pos_-time_-x_[0],
                        slope_xmax_newton,
            ]

    fig, ((ax1, ax2)) = plt.subplots(2, 1, sharex=True)
    fig.suptitle('Group {}. Participant {}: Run {}. Trial {}. Grip {}'.format(int(question_table['group'][subject]),
                                                                              question_table['id'][subject],
                                                                            iter_,event+1,curr_resp), fontsize=14, 
                                                                            fontweight='bold')
    
    plt.xlabel('Time, s', fontsize=15)
    
    ax12 = ax1.twinx() 
    ax22 = ax2.twinx()
    
    ax1.axhline(y = min_response, color='black',linestyle='dashed')
    

    for ax_counter in range(len(y_axes1)): 
        if ax_counter!=2:
            ax1.plot(time_event_corr_,y_axes1[ax_counter], color = PLOT_COLOR[ax_counter], zorder=0, linewidth=3)
            ax2.plot(time_event_corr_,y_axes2[ax_counter], color = PLOT_COLOR[ax_counter], zorder=0, linewidth=3)
        else:
            ax12.plot(time_event_corr_,y_axes1[ax_counter], color = PLOT_COLOR[ax_counter], zorder=1)
            ax22.plot(time_event_corr_,y_axes2[ax_counter], color = PLOT_COLOR[ax_counter], zorder=1)
        
        
    ax1.scatter(stim_pos_-time_-x_[0],0, marker = 'x', color = 'black', zorder=2)
    ax2.scatter(stim_pos_-time_-x_[0],0, marker = 'x', color = 'black', zorder=2)
        
    for ax_counter in range(len(y_scatter)):
        #if ax_counter!=2:
        if ax_counter!=4:
            ax1.scatter(x_scatter[ax_counter],y_scatter[ax_counter], color = DOT_COLOR[ax_counter], zorder=3)
            ax2.scatter(x_scatter_newton[ax_counter],y_scatter_newton[ax_counter], color = DOT_COLOR[ax_counter], zorder=3)
            ax1.annotate(TEXT[ax_counter],(x_scatter[ax_counter],0.1*(ax_counter+1)))
        else:
            ax12.scatter(x_scatter[ax_counter],y_scatter[ax_counter], color = DOT_COLOR[ax_counter], zorder=4)
            ax22.scatter(x_scatter_newton[ax_counter],y_scatter_newton[ax_counter], color = DOT_COLOR[ax_counter], zorder=4)
            ax12.annotate(TEXT[ax_counter],(x_scatter[ax_counter],0.1*(ax_counter+1)))
    
    ax1.set_ylabel('Force output, a.u.', color = 'blue', fontsize=13)
    ax2.set_ylabel('Force output (Newtons)', color = 'blue', fontsize=13)
    
    ax12.set_ylabel('Slope (a.u./s)', color = 'pink', fontsize=13)
    ax22.set_ylabel('Slope (Newton/s)', color = 'pink', fontsize=13)
    
    
    plt.gca().yaxis.set_major_formatter(LogFormatterSciNotation(base=10,minor_thresholds=(numpy.inf,numpy.inf),labelOnlyBase=False))
    
    mpl_axes_aligner.align.yaxes(ax1, 0, ax12, 0, 0.5) #aligns ax and ax2 axes at 0, in the middle of y axis
    mpl_axes_aligner.align.yaxes(ax2, 0, ax22, 0, 0.5) 

    fig.tight_layout()
    pdf.savefig()
    plt.close(fig)
    
    return slopes_dict,grips_dict
    
    # curve_output,slope_output = updateSubjectsDictionary(curve_output,slope_output,
    #                                                   data_plot_newton,
    #                                                   slope_newton,question_table,
    #                                                   subject,curr_resp)

    # return curve_output,slope_output
    