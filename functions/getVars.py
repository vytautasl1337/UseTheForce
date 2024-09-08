import numpy,os,traceback,pandas,datetime,itertools
import scipy.io as sio
from collections import defaultdict
from functions.preprocessing.concatenate import concat
from functions.preprocessing.myFilter import myFilter
from functions.preprocessing.interpolation import interpol
from functions.preprocessing.baseline import baseline
from functions.preprocessing.norm_event import norm_event
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from functions.vars.myVars import (var_RT,var_max_peak,var_max_time,var_slope,
                                    var_acc)



def getVar(self,exp_info,folder_single):
    
    save_destination = os.path.join(os.path.curdir,'Saved_Data/Single_subjects/%s'%(str(exp_info['ParticipantID']).strip("['']")))    
    if not os.path.isdir(save_destination):
       savepath = os.makedirs(save_destination)                               
    if os.path.isdir(save_destination):
        savepath = save_destination
        
    (log_RT_init,log_RT_init_Norm,log_MaxTime,log_MaxTime_Norm,
    log_MaxGrip,log_MaxGrip_Norm,log_Slope,log_Slope_Norm,
    log_Acceleration,log_Acceleration_Norm)= ([] for x in range(10))
    
    try:
        print('Analyzing participant: ',str(exp_info['ParticipantID']).strip("['']"))
        subject_folder_path = folder_single
        
        data,exp_info = [],[]
        file_nr=0
        for file in sorted(os.listdir(subject_folder_path)):
            if file.endswith('.mat'):
                print('Loading data from: ',subject_folder_path+'/'+file)
                if file.startswith('data'):
                    data.append(sio.loadmat((subject_folder_path+'/'+file)))
                    file_nr += 1
                elif file.startswith('ExpInfo'):
                    exp_info=sio.loadmat((subject_folder_path+'/'+file))
        print('--------------------------------------')
        merged_data = defaultdict(list)
        for d in data:
            for k, v in d.items():
                merged_data[k].append(v)
        runs=int(exp_info['Runs'])
        left = numpy.squeeze(numpy.column_stack(merged_data['Block_data_left']))
        right = numpy.squeeze(numpy.column_stack(merged_data['Block_data_right']))
        times = numpy.squeeze(numpy.column_stack(merged_data['Block_time']))
        #print(times)
        list_of_blocks = [x for x in range(int(runs*exp_info['Blocks_in_run'])) if x % int(exp_info['Blocks_in_run']) == 0]
        list_of_blocks.append(int(numpy.shape(left)[0]))

        
                
        incr=0
        # Fetch max grips from the training and the minimum thresholds
        max_grip_left = float(exp_info['Max_Force_left'])
        max_grip_right = float(exp_info['Max_Force_right'])
        min_grip_left = float(exp_info['Error_threshold_left'])
        min_grip_right = float(exp_info['Error_threshold_right'])
        
        # Loop through each run
        with PdfPages(os.path.join(savepath,'{}_single_trial_responses.pdf'.format(str(exp_info['ParticipantID']).strip("['']")))) as pdf: 

            for i in range(runs):
                
                # Concatenate data for <i> run
                time_run,left_run,right_run = concat(times, left, right, list_of_blocks, i)
                # Get <i> run onsets
                if file_nr!=1:
                    iti_run = merged_data['ITI_onset'][i]
                    stim_run = merged_data['Stimulus_Onset'][i]
                    rew_onset_run = merged_data['Trial_Reward_Onset'][i]
                    # Get <i> run variables
                    corr_run = merged_data['Correct'][i]
                    rew_run = merged_data['Reward_Probability'][i]
                    grip_run = merged_data['GoNoGo_target'][i]
                    sub_resp = merged_data['Sub_Response'][i]
                    gen_run = merged_data['Gender_of_Distractor'][i]
                    emo_run = merged_data['Emotion_of_Distractor'][i]
                    block_nr = merged_data['Block_Nr'][i]
                    won_loss_blc = merged_data['Monetary_rewards'][i]
                    ant_dur = merged_data['Anticipation_duration'][i]
                    #gender = str(exp_info['Gender']).strip("['']")
                else:
                    list_of_events=[z*runs for z in list_of_blocks] 
                    iti_run = merged_data['ITI_onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                    iti_run = iti_run.reshape(-1,iti_run.size)           
                    #iti_run = numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['ITI_onset'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    stim_run = merged_data['Stimulus_Onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                    stim_run = stim_run.reshape(-1,stim_run.size) 
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Stimulus_Onset'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    rew_onset_run = merged_data['Trial_Reward_Onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                    rew_onset_run = rew_onset_run.reshape(-1,rew_onset_run.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Trial_Reward_Onset'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]

                    corr_run = merged_data['Correct'][0][0][list_of_events[i]:list_of_events[i+1]]
                    corr_run = corr_run.reshape(-1,corr_run.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Correct'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    rew_run = numpy.array(merged_data['Reward_Probability'][0][list_of_events[i]:list_of_events[i+1]])  
                    #numpy.array(merged_data['Reward_Probability'][0][list_of_events[i]:list_of_events[i+1]])
                    
                    grip_run=merged_data['GoNoGo_target'][0][0][list_of_events[i]:list_of_events[i+1]]
                    grip_run = grip_run.reshape(-1,grip_run.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['GoNoGo_target'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #sub_resp = numpy.array(merged_data['Sub_Response'])
                    sub_resp = merged_data['Sub_Response'][0][0][list_of_events[i]:list_of_events[i+1]]
                    sub_resp = sub_resp.reshape(-1,sub_resp.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Sub_Response'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #gen_run = numpy.array(merged_data['Gender_of_Distractor'])
                    gen_run = merged_data['Gender_of_Distractor'][0][0][list_of_events[i]:list_of_events[i+1]]
                    gen_run = gen_run.reshape(-1,gen_run.size) 
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Gender_of_Distractor'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #emo_run = numpy.array(merged_data['Emotion_of_Distractor'])
                    emo_run = merged_data['Emotion_of_Distractor'][0][0][list_of_events[i]:list_of_events[i+1]]
                    emo_run = emo_run.reshape(-1,emo_run.size) 
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Emotion_of_Distractor'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #block_nr = numpy.array(merged_data['Block_Nr'])
                    block_nr=merged_data['Block_Nr'][0][0][list_of_events[i]:list_of_events[i+1]]
                    block_nr=block_nr.reshape(-1,block_nr.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Block_Nr'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #won_loss_blc = numpy.array(merged_data['Monetary_rewards'])
                    won_loss_blc=merged_data['Monetary_rewards'][0][0][list_of_events[i]:list_of_events[i+1]]
                    won_loss_blc = won_loss_blc.reshape(-1,won_loss_blc.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Monetary_rewards'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    #ant_dur = numpy.array(merged_data['Anticipation_duration'])
                    ant_dur = merged_data['Anticipation_duration'][0][0][list_of_events[i]:list_of_events[i+1]]
                    ant_dur = ant_dur.reshape(-1,ant_dur.size)
                    #numpy.asarray(numpy.reshape((numpy.concatenate(merged_data['Anticipation_duration'][(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))[list_of_events[i]:list_of_events[i+1]]
                    gender = str(exp_info['Gender']).strip("['']")
                    
                try:
                    #with PdfPages(os.path.join(savepath,'{}_single_trial_responses.pdf'.format(question_table['participant_id'][subject]))) as pdf: 
                    for event in range(rew_onset_run.size):
                        incr+=1
                        
                        #####################################
                        if corr_run[0][event] == 1:
                            # Get indexes of the events CORRECT FOR 60ms DELAY IN THE SCANNER!
                            idx_iti_onset = (numpy.abs(time_run - iti_run[0][event])).argmin()
                            idx_stim_onset = (numpy.abs(time_run - stim_run[0][event])).argmin()
                            idx_rew_onset = (numpy.abs(time_run - rew_onset_run[0][event])).argmin() 
                            # Extract left and right source events using indexes
                            source_time_event = time_run[idx_iti_onset:idx_rew_onset]
                            source_right_event = right_run[idx_iti_onset:idx_rew_onset]
                            source_left_event = left_run[idx_iti_onset:idx_rew_onset]
                            
                            # Normalize event
                            source_left_event_norm,source_right_event_norm=norm_event(max_grip_left,max_grip_right,source_left_event,source_right_event)

                            # Interpolation
                            i_time_event,i_left_event,i_right_event,i_left_event_norm,i_right_event_norm,sample_rt=interpol(source_time_event,source_left_event,source_right_event,source_left_event_norm,source_right_event_norm)
                            
                            # Correct baseline of current event
                            bi_right_event, bi_left_event, bi_right_event_norm, bi_left_event_norm=baseline(i_left_event,i_right_event,right_run,left_run,idx_iti_onset,idx_stim_onset,i_left_event_norm,i_right_event_norm)

                            # Filter right and left events
                            fbi_left_event,fbi_right_event,fbi_left_event_norm,fbi_right_event_norm=myFilter(i_time_event,bi_left_event,bi_right_event, bi_left_event_norm,bi_right_event_norm)

                            # Recalculate indexes for single events

                            idx_iti_onset = (numpy.abs(i_time_event - iti_run[0][event])).argmin()
                            idx_stim_onset = (numpy.abs(i_time_event - stim_run[0][event])).argmin()
                            idx_rew_onset = (numpy.abs(i_time_event - rew_onset_run[0][event])).argmin() 

                            # Anticipation onset
                            idx_ant_onset = (numpy.abs(i_time_event-(rew_onset_run[0][event] - ant_dur[0][event]))).argmin()

                            if grip_run[0][event] == 1 or grip_run[0][event] == -1:
                                
                                # Grip events to data
                                if grip_run[0][event] == 1:
                                    data = fbi_right_event
                                    data_not_used = fbi_left_event
                                    data_norm = fbi_right_event_norm
                                    min_response = min_grip_right
                                elif grip_run[0][event] == -1:
                                    data = fbi_left_event
                                    data_not_used = fbi_right_event
                                    data_norm = fbi_left_event_norm
                                    min_response = min_grip_left
                                    
                                log_RT_init,log_RT_init_Norm=var_RT(min_response,log_RT_init,log_RT_init_Norm,i_time_event,data,idx_stim_onset,stimulus_onset=stim_run[0][event])
                                log_MaxGrip,log_MaxGrip_Norm=var_max_peak(log_MaxGrip,log_MaxGrip_Norm,data,data_norm)
                                log_MaxTime,log_MaxTime_Norm=var_max_time(log_MaxTime,log_MaxTime_Norm,i_time_event,data,stimulus_onset=stim_run[0][event])
                                log_Slope,log_Slope_Norm=var_slope(sample_rt,log_Slope,log_Slope_Norm,data,data_norm)
                                log_Acceleration,log_Acceleration_Norm=var_acc(sample_rt,log_Acceleration,log_Acceleration_Norm,data,data_norm)
                                

                                TITLES = ['Reaction initiation','Maximum grip','Maximum slope','Maximum acceleration']
                                EVENT_CURVE = ['Force curve','Force curve','Slope curve','Acceleration curve']
                                PLOT_COLOR = ['blue','blue','pink','purple']
                                DOT_COLOR = ['red','green','orange','cyan']
                                DOT_TEXT = ['Reaction','Maximum','Maximum slope','Maximum acceleration']
                                PLOT_UNUSED_ALPHA = [.3,.3,0,0]
                                LIMITS = [[-.1,1],[-.1,1],[-.001,.001],[-.0000025,.0000025]]
                                
                                # fig, axes = plt.subplots(nrows=2, ncols=2)
                                fig, axes = plt.subplots(num=1,clear=True)
                                fig, axes = plt.subplots(nrows=2, ncols=2)
                                max_point = numpy.argmax(data)
                                slope = numpy.gradient(data[:max_point],1/sample_rt).tolist()
                                slope_ymax = numpy.max(slope)
                                xpos = slope.index(slope_ymax)
                                slope_xmax = i_time_event[xpos]
                                
                                
                                acc = numpy.gradient(slope,1/sample_rt).tolist()
                                acc_ymax = numpy.max(acc)
                                xpos = acc.index(acc_ymax)
                                acc_xmax = i_time_event[xpos]
                                
                                slope = numpy.gradient(data,1/sample_rt).tolist()
                                acc = numpy.gradient(slope,1/sample_rt).tolist()
                                
                                
                                y_axes = [data,data,slope,acc]
                                y_unused = [data_not_used,data_not_used,data_not_used,data_not_used]
                                y_scatter = [0,log_MaxGrip[-1],log_Slope[-1],log_Acceleration[-1]]
                                x_scatter = [log_RT_init[-1] + stim_run[0][event],
                                                log_MaxTime[-1] + stim_run[0][event],
                                                slope_xmax,
                                                acc_xmax]
                                
                                for img_counter, (i_row, j_col) in enumerate(
                                            itertools.product(range(2), range(2))
                                        ):
                                    ax = axes[i_row, j_col]
                                    ax.plot(i_time_event,y_axes[img_counter], color = PLOT_COLOR[img_counter])
                                    ax.plot(i_time_event,y_unused[img_counter], color = 'grey', alpha = PLOT_UNUSED_ALPHA[img_counter])
                                    ax.scatter(x_scatter[img_counter],y_scatter[img_counter], color = DOT_COLOR[img_counter])
                                    ax.scatter(stim_run[0][event],0, marker = 'x', color = 'black')
                                    
                                    ax.set_ylim(LIMITS[img_counter])
                                    ax.set_title(TITLES[img_counter])
                                    
                                    handles, labels = plt.gca().get_legend_handles_labels()
                                    line = Line2D([0], [0], label=EVENT_CURVE[img_counter], color=PLOT_COLOR[img_counter])
                                    point = Line2D([0], [0], label=DOT_TEXT[img_counter], marker='o', 
                                                    markeredgecolor=DOT_COLOR[img_counter],
                                                    markerfacecolor=DOT_COLOR[img_counter], linestyle='')
                                    point1 = Line2D([0], [0], label='Stimulus', marker='x', 
                                                    markeredgecolor='black',markerfacecolor='black', linestyle='')
                                    if img_counter<2:
                                        line1 = Line2D([0], [0], label='Other device', color='grey')
                                        handles.extend([line,line1,point,point1])
                                        ax.legend(handles=handles)
                                    else:
                                        handles.extend([line,point,point1])
                                        ax.legend(handles=handles)
                                
                                
                                fig.suptitle('Participant {}: Run {}. Trial {}'.format(str(exp_info['ParticipantID']).strip("['']"),
                                            i+1,event+1))
                                
                                fig.set_size_inches(12, 8)
                                
                                pdf.savefig()
                                fig.clear() 
                                plt.close(fig)
                                
 
                except Exception as ex:
                    print(ex)
                    traceback.print_exc()
                    pass
    except Exception as ex:
        print('Subject {} not found.'.format(str(exp_info['ParticipantID']).strip("['']")))
        print(ex)
        traceback.print_exc()
        pass                 


    print('Plots saved')


