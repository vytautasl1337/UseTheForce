import numpy,os,traceback,pandas,datetime
from scipy.io import savemat
from pathlib import Path
from functions.preprocessing.concatenate import concat
from functions.preprocessing.myFilter import myFilter
from functions.preprocessing.interpolation import interpol
from functions.preprocessing.baseline import baseline
from functions.preprocessing.norm_event import norm_event
from functions.preprocessing.newton import linear_reg
from functions.dictionary_values.addValues import addValues
from functions.dictionary_values.addValues import createSubjectsDictionary
from functions.dictionary_values.addValues import createGroupOutputs
from functions.dictionary_values.dict_lists import dictionary_
from functions.dataCheckAndGet.data_handle import qualityCheck
from functions.dataCheckAndGet.data_handle import getData
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages
from functions.plots.plot_subjects import plot2pdf
from functions.plots.plot_subjects_nogo import plot2pdf_nogo
from functions.vars.nogo import nogos
from functions.vars.myVars import *
from colorama import Back,Style

# Run group analysis
def getVar_group(self,folder_group):
    
    # Check for data folder and get path
    try:
        group_folders = [f for f in sorted(os.listdir(folder_group))]
        print('Folders found: ',group_folders)
    except: 
        print('An error occured. Please check the data folder.')
        
    # Check for the .xlsx file to guide the script
    try:
        fn = list(Path(folder_group).glob("*.xlsx"))
        if len(fn) == 1:
            question_table = pandas.read_excel(fn[0])
            print('Participants\' list found.')
    except:
        print('An error occured. Please make sure there is only one .xlsx file inside the folder.')
        
    # Check if file contains required columns
    try:
        columns_to_check = ['id','data','delay','group','gender','age','calibration'] #required
        columns_found = question_table.columns.values.tolist()
        for col in columns_to_check:
            if col in columns_found:
                pass
        print('All keywords found.')
    except Exception as error:
        print("An error occured. Keyword ", error, ' is missing')
            
    # Create output folder
    save_destination = os.path.join(folder_group,
        'Results/Group_output_%s'%str(datetime.datetime.now().strftime('%Y%m%d%H%M')))
    if not os.path.isdir(save_destination):
       savepath = os.makedirs(save_destination)                               
    if os.path.isdir(save_destination):
        savepath = save_destination

    print('--------------------------------------')
    
    # Create dictionary to store values for output
    data_dict,dict_ext,len_keylist = dictionary_(question_table)

    subject_in_analysis = 0
    to_analyze = question_table['data'].sum()
    
    slopes_dict,grips_dict = createGroupOutputs()
    
    # Loop through each subject
    for subject in range(len(question_table)):
        
        # If 'data' is equal to 1 - proceed
        if question_table['data'][subject]==1:
            
            raw_force_output,force_preprocessed,slope_preprocessed,force_preprocessed_newton,slope_preprocessed_newton = createSubjectsDictionary(question_table)
            
            # Make subject folder
            sub_output = os.path.join(savepath,question_table['id'][subject])
            if not os.path.isdir(sub_output):
                sub_destination = os.makedirs(sub_output)                               
            if os.path.isdir(sub_output):
                sub_destination = sub_output
            
            # Get calibration data for the device:
            try:
                slopeL,interceptL,slopeR,interceptR = linear_reg(question_table['calibration'][subject])
            except:
                print(Back.RED + 'Could not find calibration data!' + Style.RESET_ALL)
            
            try:
                # Print detected files in the current directory
                print('Analyzing participant: ',question_table['id'][subject])
                
                subject_folder_path = os.path.join(folder_group,'%s/Task/source_data'%(question_table['id'][subject]))
                if os.path.isdir(subject_folder_path):
                    pass
                else: #older version
                    subject_folder_path = os.path.join(folder_group,'%s/Experiment_data'%(question_table['id'][subject]))
                print('Subject folder: ', subject_folder_path)
                    
                # Check files to load and if they are ok
                totBlcNr,evntBlc,exp_info,list_of_blocks,data_to_get = qualityCheck(subject_folder_path)
                
                # Get data
                merged_data,run_list,run_nr = getData(subject_folder_path,data_to_get)
                
                # Separate data into left, right and time    
                left = numpy.squeeze(numpy.column_stack(merged_data['Block_data_left']))
                right = numpy.squeeze(numpy.column_stack(merged_data['Block_data_right']))
                times = numpy.squeeze(numpy.column_stack(merged_data['Block_time']))
                
                    
                incr=0
                # Fetch max grips from the training and the minimum thresholds
                max_grip_left = float(exp_info['Max_Force_left'])
                max_grip_right = float(exp_info['Max_Force_right'])
                min_grip_left = float(exp_info['Error_threshold_left'])
                min_grip_right = float(exp_info['Error_threshold_right'])
                
                print('Analyzing participant...')
                
                with PdfPages(os.path.join(sub_destination,
                                           '{}_responses.pdf'.format(question_table['id'][subject]))) as pdf: 
                    
                    for i in range(run_nr):
                        # Concatenate data for <i> run
                        time_run,left_run,right_run = concat(times, left, right, list_of_blocks, i)
                        
                        # Get <i> run onsets
                        if list_of_blocks[-1]-list_of_blocks[-2]<=totBlcNr:
                            iti_run = merged_data['ITI_onset'][i]
                            stim_run = merged_data['Stimulus_Onset'][i]
                            rew_onset_run = merged_data['Trial_Reward_Onset'][i]
                            corr_run = merged_data['Correct'][i]
                            rew_run = merged_data['Reward_Probability'][i]
                            grip_run = merged_data['GoNoGo_target'][i]
                            sub_resp = merged_data['Sub_Response'][i]
                            gen_run = merged_data['Gender_of_Distractor'][i]
                            emo_run = merged_data['Emotion_of_Distractor'][i]
                            block_nr = merged_data['Block_Nr'][i]
                            won_loss_blc = merged_data['Monetary_rewards'][i]
                            ant_dur = merged_data['Anticipation_duration'][i]
                        else: # older version
                            list_of_events=[z*int(run_list[0]) for z in list_of_blocks] 
                            iti_run = merged_data['ITI_onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                            iti_run = iti_run.reshape(-1,iti_run.size)       
                            stim_run = merged_data['Stimulus_Onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                            stim_run = stim_run.reshape(-1,stim_run.size) 
                            rew_onset_run = merged_data['Trial_Reward_Onset'][0][0][list_of_events[i]:list_of_events[i+1]]
                            rew_onset_run = rew_onset_run.reshape(-1,rew_onset_run.size)
                            corr_run = merged_data['Correct'][0][0][list_of_events[i]:list_of_events[i+1]]
                            corr_run = corr_run.reshape(-1,corr_run.size)
                            rew_run = numpy.array(merged_data['Reward_Probability'][0][list_of_events[i]:list_of_events[i+1]])                              
                            grip_run=merged_data['GoNoGo_target'][0][0][list_of_events[i]:list_of_events[i+1]]
                            grip_run = grip_run.reshape(-1,grip_run.size)
                            sub_resp = merged_data['Sub_Response'][0][0][list_of_events[i]:list_of_events[i+1]]
                            sub_resp = sub_resp.reshape(-1,sub_resp.size)
                            gen_run = merged_data['Gender_of_Distractor'][0][0][list_of_events[i]:list_of_events[i+1]]
                            gen_run = gen_run.reshape(-1,gen_run.size) 
                            emo_run = merged_data['Emotion_of_Distractor'][0][0][list_of_events[i]:list_of_events[i+1]]
                            emo_run = emo_run.reshape(-1,emo_run.size) 
                            block_nr=merged_data['Block_Nr'][0][0][list_of_events[i]:list_of_events[i+1]]
                            block_nr=block_nr.reshape(-1,block_nr.size)
                            won_loss_blc=merged_data['Monetary_rewards'][0][0][list_of_events[i]:list_of_events[i+1]]
                            won_loss_blc = won_loss_blc.reshape(-1,won_loss_blc.size)
                            ant_dur = merged_data['Anticipation_duration'][0][0][list_of_events[i]:list_of_events[i+1]]
                            ant_dur = ant_dur.reshape(-1,ant_dur.size)
                            trl_nr=merged_data['Trial_Nr'][0][0][list_of_events[i]:list_of_events[i+1]]
                            trl_nr=trl_nr.reshape(-1,trl_nr.size)
                            behruns = [t for t in range(1, (list_of_events[i+1]//(totBlcNr*evntBlc))+1) for _ in range(totBlcNr*evntBlc)]                            
                            
                        try:
                            blocks_to_take = list_of_blocks[i+1]-list_of_blocks[i]
                            #for event in range(won_loss_blc.size):
                            for event in range(blocks_to_take*evntBlc):
                                incr+=1
                                ##################################
                                data_dict['SubjectNr'].append(subject+1)
                                if list_of_blocks[-1]-list_of_blocks[-2]<=totBlcNr:
                                    data_dict['Run'].append(int(run_list[i]))
                                    data_dict['TrialNr'].append(event+1)
                                else:
                                    data_dict['Run'].append(behruns[event])
                                    data_dict['TrialNr'].append(trl_nr[0][event])
                                data_dict['TotalTrialNr'].append(incr)
                                data_dict['BlockNr'].append(block_nr[0][event])
                                data_dict['FaceGender'].append(gen_run[0][event])
                                data_dict['FaceEmotion'].append(emo_run[0][event])
                                data_dict['RewardReceived'].append(won_loss_blc[0][event])
                                data_dict['SymbolTarget'].append(grip_run[0][event])
                                data_dict['GripResponse'].append(sub_resp[0][event])
                                data_dict['Correct'].append(corr_run[0][event])
                                if rew_run[event]=='high':
                                    data_dict['RewardPromise'].append(1)
                                else:
                                    data_dict['RewardPromise'].append(-1)

                                if dict_ext == 1:
                                    data_dict = addValues(question_table,subject,data_dict)
                                
                                if question_table['delay'][subject]!=0:
                                    idx_iti_onset = (numpy.abs(time_run - (iti_run[0][event]+question_table['delay'][subject]))).argmin()
                                    idx_stim_onset = (numpy.abs(time_run - (stim_run[0][event]+question_table['delay'][subject]))).argmin()
                                    idx_rew_onset = (numpy.abs(time_run - (rew_onset_run[0][event]+question_table['delay'][subject]))).argmin() 
                                else: 
                                    idx_iti_onset = (numpy.abs(time_run - iti_run[0][event])).argmin()
                                    idx_stim_onset = (numpy.abs(time_run - stim_run[0][event])).argmin()
                                    idx_rew_onset = (numpy.abs(time_run - rew_onset_run[0][event])).argmin() 
                                
                                # Extract left and right source events using indexes
                                source_time_event = time_run[idx_iti_onset:idx_rew_onset]
                                source_right_event = right_run[idx_iti_onset:idx_rew_onset]
                                source_left_event = left_run[idx_iti_onset:idx_rew_onset]

                                
                                # Save raw data
                                raw_force_output['time'].append(source_time_event)
                                raw_force_output['left'].append(source_left_event)
                                raw_force_output['right'].append(source_right_event)
                                
                                # Normalize event
                                source_left_event_norm,source_right_event_norm=norm_event(max_grip_left,max_grip_right,source_left_event,source_right_event)

                                # Interpolation
                                i_time_event,i_left_event,i_right_event,i_left_event_norm,i_right_event_norm,sample_rt=interpol(source_time_event,
                                                                                                                                source_left_event,
                                                                                                                                source_right_event,
                                                                                                                                source_left_event_norm,
                                                                                                                                source_right_event_norm)

                                # Correct baseline of current event
                                bi_right_event, bi_left_event,bi_right_event_norm, bi_left_event_norm, bi_right_event_newton, bi_left_event_newton=baseline(i_left_event,
                                                                                                                                                            i_right_event,
                                                                                                                                                            right_run,
                                                                                                                                                            left_run,
                                                                                                                                                            idx_iti_onset,
                                                                                                                                                            idx_stim_onset,
                                                                                                                                                            i_left_event_norm,
                                                                                                                                                            i_right_event_norm,
                                                                                                                                                            slopeL,
                                                                                                                                                            interceptL,
                                                                                                                                                            slopeR,
                                                                                                                                                            interceptR)

                                # Filter right and left events
                                fbi_left_event,fbi_right_event,fbi_left_event_norm,fbi_right_event_norm,fbi_right_event_newton,fbi_left_event_newton=myFilter(i_time_event,
                                                                                                                                                                bi_left_event,
                                                                                                                                                                bi_right_event, 
                                                                                                                                                                bi_left_event_norm,
                                                                                                                                                                bi_right_event_norm,
                                                                                                                                                                bi_right_event_newton, 
                                                                                                                                                                bi_left_event_newton)

                                # Save pre-processed data
                                force_preprocessed['time'].append(i_time_event)
                                force_preprocessed['left'].append(fbi_left_event)
                                force_preprocessed['right'].append(fbi_right_event)
                                
                                force_preprocessed_newton['time'].append(i_time_event)
                                force_preprocessed_newton['left'].append(fbi_left_event_newton)
                                force_preprocessed_newton['right'].append(fbi_right_event_newton)
                                
                                # Recalculate indexes for single events
                                if question_table['delay'][subject]!=0:
                                    idx_iti_onset = (numpy.abs(i_time_event - (iti_run[0][event]+question_table['delay'][subject]))).argmin()
                                    idx_stim_onset = (numpy.abs(i_time_event - (stim_run[0][event]+question_table['delay'][subject]))).argmin()
                                    idx_rew_onset = (numpy.abs(i_time_event - (rew_onset_run[0][event]+question_table['delay'][subject]))).argmin() 
                                else: 
                                    idx_iti_onset = (numpy.abs(i_time_event - iti_run[0][event])).argmin()
                                    idx_stim_onset = (numpy.abs(i_time_event - stim_run[0][event])).argmin()
                                    idx_rew_onset = (numpy.abs(i_time_event - rew_onset_run[0][event])).argmin() 

                                # Anticipation onset
                                idx_ant_onset = (numpy.abs(i_time_event-(rew_onset_run[0][event] - ant_dur[0][event]))).argmin()
                                
                                # MAX ANTICIPATION
                                data_dict=var_antmax(idx_ant_onset,data_dict,fbi_left_event,fbi_right_event,
                                                    fbi_left_event_norm,fbi_right_event_norm)

                                # AUC ANTICIPATION
                                data_dict=var_antauc(idx_ant_onset,data_dict,i_time_event,fbi_left_event,
                                                    fbi_right_event,fbi_left_event_norm,fbi_right_event_norm)

                                slope_preprocessed['time'].append(i_time_event)
                                slope_preprocessed_newton['time'].append(i_time_event)
                                
                                time_event_corr = [x - i_time_event[0] for x in i_time_event]
                                
                                if sub_resp[0][event] != 0: # grip response either correct or not
                                    
                                    #  go response
                                    if sub_resp[0][event] == 1: #correct
                                        curr_resp = 'Right'
                                        data = fbi_right_event
                                        data_not_used = fbi_left_event
                                        data_norm = fbi_right_event_norm
                                        min_response = min_grip_right
                                        data_newton = fbi_right_event_newton
                                        data_not_used_newton = fbi_left_event_newton
                                        
                                        derivative = numpy.gradient(data,1/sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_newton,1/sample_rt).tolist()
                                        slope_preprocessed['right'].append(derivative)
                                        slope_preprocessed_newton['right'].append(derivative_newton)
                                        
                                        derivative = numpy.gradient(data_not_used,1/sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_not_used_newton,1/sample_rt).tolist()
                                        slope_preprocessed['left'].append(derivative)
                                        slope_preprocessed_newton['left'].append(derivative_newton)
                                        #--- MIRROR RESPONSE ---# double check in output
                                        if numpy.max(data_not_used)>=min_grip_left:
                                            data_dict['Mirror'].append(1)
                                        else:
                                            data_dict['Mirror'].append(0)
                                        
                                        
                                    if sub_resp[0][event] == -1:
                                        curr_resp = 'Left'
                                        data = fbi_left_event
                                        data_not_used = fbi_right_event
                                        data_norm = fbi_left_event_norm
                                        min_response = min_grip_left
                                        data_newton = fbi_left_event_newton
                                        data_not_used_newton = fbi_right_event_newton
                                        derivative = numpy.gradient(data,1/sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_newton,1/sample_rt).tolist()
                                        slope_preprocessed['left'].append(derivative)
                                        slope_preprocessed_newton['left'].append(derivative_newton)
                                        
                                        derivative = numpy.gradient(data_not_used,1/sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_not_used_newton,1/sample_rt).tolist()
                                        slope_preprocessed['right'].append(derivative)
                                        slope_preprocessed_newton['right'].append(derivative_newton)
                                        #--- MIRROR RESPONSE ---# double check in output
                                        if numpy.max(data_not_used)>=min_grip_right:
                                            data_dict['Mirror'].append(1)
                                        else:
                                            data_dict['Mirror'].append(0)

                                    #--- GET VALUES ---#

                                    # REACTION TIMEs
                                    data_dict=var_RT(min_response,data_dict,sample_rt,time_event_corr,i_time_event,
                                                        data,idx_stim_onset,time_=i_time_event[0],
                                                        stimulus_onset=stim_run[0][event])

                                    # SETTLING TIME
                                    data_dict=var_set_time(data_dict,i_time_event,data,min_response,stimulus_onset=stim_run[0][event])

                                    # REACTION TIME at maximum acceleration point
                                    data_dict=var_RTacc(data_dict,sample_rt,i_time_event,data,data_norm,stimulus_onset=stim_run[0][event])

                                    # MAX PEAK
                                    data_dict=var_max_peak(data_dict,data,data_norm,data_newton)

                                    # TIME OF MAX PEAK
                                    data_dict=var_max_time(data_dict,i_time_event,data,stimulus_onset=stim_run[0][event])

                                    # SLOPE
                                    data_dict=var_slope(sample_rt,data_dict,data,data_norm,data_newton)

                                    # ACCELERATION
                                    data_dict=var_acc(sample_rt,data_dict,data,data_norm,data_newton)

                                    # AUC
                                    data_dict=var_auc(min_response,data_dict,i_time_event,data,data_norm,idx_stim_onset)

                                    # GRIP TIME
                                    data_dict=var_griptime(min_response,data_dict,i_time_event,data,idx_stim_onset,stimulus_onset=stim_run[0][event])

                                    # RISE TIME
                                    data_dict=var_rise(min_response,data_dict,i_time_event,data,idx_stim_onset)

                                    # FALL TIME
                                    data_dict=var_fall(data_dict,i_time_event,data)

                                    # DE-SLOPE
                                    data_dict=var_deslope(sample_rt,data_dict,data,data_norm,data_newton)

                                    # DE-ACCELERATION
                                    data_dict=var_deacc(sample_rt,data_dict,data,data_norm,data_newton)
                                    
                                    
                                    slopes_dict,grips_dict=plot2pdf(pdf=pdf,
                                                question_table=question_table,slopes_dict=slopes_dict,grips_dict=grips_dict,
                                                data_dict=data_dict,data_newton=data_newton,
                                                data_not_used_newton=data_not_used_newton,
                                                data=data,data_not_used=data_not_used,
                                                time_event_corr=time_event_corr,
                                                i_time_event=i_time_event,
                                                time_=i_time_event[0],stim_pos_=stim_run[0][event],
                                                iter_=data_dict['Run'][-1],sample_rt=sample_rt,min_response=min_response,
                                                subject=subject,event=event,curr_resp=curr_resp)
                                    
                                    # LOG NOGO NANs
                                    data_dict['MaxNOGOright'].append(numpy.nan)
                                    data_dict['MaxNOGOleft'].append(numpy.nan)
                                    data_dict['AucNOGOright'].append(numpy.nan)
                                    data_dict['AucNOGOleft'].append(numpy.nan)
                                    data_dict['MaxNOGOright_Norm'].append(numpy.nan)
                                    data_dict['MaxNOGOleft_Norm'].append(numpy.nan)
                                    data_dict['AucNOGOright_Norm'].append(numpy.nan)
                                    data_dict['AucNOGOleft_Norm'].append(numpy.nan)
                                    
                                elif sub_resp[0][event] == 0:# and grip_run[0][event] == 0:
                                        
                                        data_dict['Mirror'].append(0)
                                        
                                        curr_resp = 'NoGo'
                                        data1 = fbi_right_event
                                        data2 = fbi_left_event
                                        data_norm1 = fbi_right_event_norm
                                        data_norm2 = fbi_left_event_norm
                                        data_newton1 = fbi_right_event_newton
                                        data_newton2 = fbi_left_event_newton
                                        
                                        derivative = numpy.gradient(data2,sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_newton2,sample_rt).tolist()
                                        slope_preprocessed['left'].append(derivative)
                                        slope_preprocessed_newton['left'].append(derivative_newton)
                                        
                                        derivative = numpy.gradient(data1,sample_rt).tolist()
                                        derivative_newton = numpy.gradient(data_newton1,sample_rt).tolist()
                                        slope_preprocessed['right'].append(derivative)
                                        slope_preprocessed_newton['right'].append(derivative_newton)
                                        
                                        if corr_run[0][event] == 1: 
                                            data_dict=nogos(data_dict,fbi_left_event,fbi_right_event,fbi_left_event_norm,
                                                            fbi_right_event_norm,i_time_event,idx_ant_onset,idx_stim_onset,len_keylist)
                                        elif corr_run[0][event] == 0:
                                            data_dict = {key: (value + [numpy.nan] if 18 < key_idx < len_keylist else value) for key_idx, (key, value) in enumerate(data_dict.items())}

                                        plot2pdf_nogo(pdf=pdf,question_table=question_table,data_dict=data_dict,
                                                      data_newton1=data_newton1,data_newton2=data_newton2,
                                                      data1=data1,data2=data2,time_event_corr=time_event_corr,
                                                      i_time_event=i_time_event,sample_rt=sample_rt,
                                                      event=event,subject=subject,time_=i_time_event[0],
                                                      stim_pos_=stim_run[0][event],iter_=data_dict['Run'][-1])
                                
                                del source_time_event,source_left_event,source_right_event   
                                del i_time_event,fbi_right_event,fbi_left_event,fbi_left_event_newton,fbi_right_event_newton
                                    
                        except Exception as ex:
                            print(ex)
                            traceback.print_exc()
                            pass

                print("Saving force data of ", question_table['id'][subject])
                savemat(os.path.join(sub_destination,'raw_force.mat'), raw_force_output)
                savemat(os.path.join(sub_destination,'force_preprocessed.mat'), force_preprocessed)
                savemat(os.path.join(sub_destination,'force_preprocessed_newton.mat'), force_preprocessed_newton)
                print("Saving slope data...")
                savemat(os.path.join(sub_destination,'slope_preprocessed.mat'), slope_preprocessed)
                savemat(os.path.join(sub_destination,'slope_preprocessed_newton.mat'), slope_preprocessed_newton)
            
            except Exception as ex:
                print('Subject {} not found.'.format(question_table['id'][subject]))
                print(ex)
                traceback.print_exc()
                pass  
            subject_in_analysis+=1         
            print('Progress:...',("%.2f" %((subject_in_analysis/to_analyze)*100)),'%')
            
    print('Analysis finished. Preparing group output...')
    
    try:
        df = pandas.DataFrame(data_dict)
    except ValueError as e:
        if str(e) == 'arrays must all be same length' or str(e) == 'All arrays must be of the same length':
            df = pandas.DataFrame.from_dict(data_dict, orient='index')
            df = df.transpose()


    df.to_excel(os.path.join(savepath,'behavioral_group_output.xlsx'),sheet_name='Output', index=False)
    print('Group data file saved and can be found in ',savepath)
    
    print('Saving group grip force outputs')
    savemat(os.path.join(savepath,'grips.mat'), grips_dict)
    savemat(os.path.join(savepath,'slopes.mat'), slopes_dict)

    #from functions.plots.plot_grips import plotGrips
    #plotGrips(savepath,slope_output,curve_output,question_table)
    
    print('Analysis finished')