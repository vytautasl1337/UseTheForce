import numpy, traceback
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.signal import find_peaks, peak_widths

#-----------------------------------------------------------------------------
# Get RT_init
def var_RT(min_response,data_dict,sample_rt,time_event_corr,i_time_event,data,idx_stim_onset,time_,stimulus_onset):

    stim_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stimulus_onset-time_)))
    end_pos = min(enumerate(time_event_corr), key=lambda x: abs(x[1]-(stimulus_onset-time_+4))) 
    # Get time event
    data_ = data[stim_pos[0]:end_pos[0]]
    x_ = time_event_corr[stim_pos[0]:end_pos[0]] 
    time_event_corr_ = [x-x_[0] for x in x_]
    # RT_onset
    #slope = numpy.gradient(data_,1/sample_rt)
    try:
        _data_=numpy.array(data_)
        peaks, _ = find_peaks(_data_)
        largest_peak = peaks[numpy.argmax(_data_[peaks])]
        results_full99 = peak_widths(_data_, [largest_peak], rel_height=0.99)
        results_full95 = peak_widths(_data_, [largest_peak], rel_height=0.95)
        onset_to_largest_peak95 = int(results_full95[2][0])
        onset_to_largest_peak99 = int(results_full99[2][0])
        data_dict['RT_99'].append(time_event_corr_[onset_to_largest_peak99])
        data_dict['RT_95'].append(time_event_corr_[onset_to_largest_peak95])
    except:
        data_dict['RT_99'].append(numpy.nan)
        data_dict['RT_95'].append(numpy.nan)
    
    # RT_init - original
    increase,sld=0,0
    try:
        for sld in range(len(data_)):
            if data_[sld+1]>data_[sld]:
                increase+=1
            elif data_[sld+1]<=data_[sld]:
                increase=0
            #if increase == 15:
            if (data_[sld]>=min_response and increase >= 5):
                RT_idx = (sld-increase)+idx_stim_onset
                break
        data_dict['RT_init'].append(i_time_event[RT_idx]-stimulus_onset)
        #data_dict['RT_init'].append(time_event_corr_[RT_idx])
        #print(i_time_event[RT_idx]-stimulus_onset)

    except Exception as ex:
        data_dict['RT_init'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get RT_acc
def var_RTacc(data_dict,sample_rt,i_time_event,data,data_norm,stimulus_onset):
    try:
        max_point = numpy.argmax(data)
        max_point_norm = numpy.argmax(data_norm)
        slope = numpy.gradient(data[:max_point],sample_rt)
        slope_norm = numpy.gradient(data_norm[:max_point_norm],sample_rt)
        acc = numpy.gradient(slope,sample_rt)
        acc_norm = numpy.gradient(slope_norm,sample_rt)
        data_dict['RT_acc'].append(i_time_event[numpy.argmax(acc)]-stimulus_onset)
    except Exception as ex:
        data_dict['RT_acc'].append(numpy.nan)
        #data_dict['RT_acc_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get max peak
def var_max_peak(data_dict,data,data_norm,data_newton):
    try:
        data_dict['MaxGrip'].append(numpy.max(data))
        data_dict['MaxGrip_Norm'].append(numpy.max(data_norm))
        data_dict['MaxGrip_New'].append(numpy.max(data_newton))
    except Exception as ex:
        data_dict['MaxGrip'].append(numpy.nan)
        data_dict['MaxGrip_Norm'].append(numpy.nan)
        data_dict['MaxGrip_New'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get max peak time
def var_max_time(data_dict,i_time_event,data,stimulus_onset):
    try:
        index_max = numpy.argmax(data)
        data_dict['MaxTime'].append(i_time_event[index_max]-stimulus_onset)
        #data_dict['MaxTime_Norm'].append(data_dict['MaxTime'][-1])
    except Exception as ex:
        data_dict['MaxTime'].append(numpy.nan)
        #data_dict['MaxTime_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get slope
def var_slope(sample_rt,data_dict,data,data_norm,data_newton):
    try:
        max_point = numpy.argmax(data)
        max_point_norm = numpy.argmax(data_norm)
        slope = numpy.gradient(data[:max_point],sample_rt)
        slope_norm = numpy.gradient(data_norm[:max_point_norm],sample_rt)
        data_dict['Slope'].append(numpy.max(slope))
        data_dict['Slope_Norm'].append(numpy.max(slope_norm))
        
        max_point = numpy.argmax(data_newton)
        slope = numpy.gradient(data_newton[:max_point],sample_rt)
        data_dict['Slope_New'].append(numpy.max(slope))
    except Exception as ex:
        data_dict['Slope'].append(numpy.nan)
        data_dict['Slope_Norm'].append(numpy.nan)
        data_dict['Slope_New'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get acceleration
def var_acc(sample_rt,data_dict,data,data_norm,data_newton):
    try:
        max_point = numpy.argmax(data)
        max_point_norm = numpy.argmax(data_norm)
        slope = numpy.gradient(data[:max_point],sample_rt)
        slope_norm = numpy.gradient(data_norm[:max_point_norm],sample_rt)
        acc = numpy.gradient(slope,sample_rt)
        acc_norm = numpy.gradient(slope_norm,sample_rt)
        data_dict['Acceleration'].append(numpy.max(acc))
        data_dict['Acceleration_Norm'].append(numpy.max(acc_norm))
        
        max_point = numpy.argmax(data_newton)
        slope = numpy.gradient(data_newton[:max_point],sample_rt)
        acc = numpy.gradient(slope,sample_rt)
        data_dict['Acceleration_New'].append(numpy.max(acc))
    except Exception as ex:
        data_dict['Acceleration'].append(numpy.nan)
        data_dict['Acceleration_Norm'].append(numpy.nan)
        data_dict['Acceleration_New'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get area under the curve
def var_auc(min_response,data_dict,i_time_event,data,data_norm,idx_stim_onset):
    increase,sld=0,0
    try:
        for sld in range(len(data)):
            if data[sld+1]>data[sld] and sld>idx_stim_onset:
                increase+=1
            elif data[sld+1]<=data[sld]:
                increase=0
            if data[sld]>=min_response:
                RT_idx = sld-increase
                break
        max_point = numpy.argmax(data)
        dec_sig = data[max_point:]
        dec_time = i_time_event[max_point:]
        decrease,sld = 0,0
        for sld in range(len(dec_sig)):
            if dec_sig[sld+1]>=dec_sig[sld]:
                decrease+=1
            elif dec_sig[sld+1]<dec_sig[sld]:
                decrease=0
            if decrease == 5:
                ST_idx = sld-5
                ST_idx = ST_idx+len(data[:max_point])
                break 
        data_dict['AUC'].append(integrate.simpson(data[RT_idx:ST_idx],i_time_event[RT_idx:ST_idx]))
        #data_dict['AUC_Norm'].append(integrate.simpson(data_norm[RT_idx:ST_idx],i_time_event[RT_idx:ST_idx]))
    except Exception as ex:
        data_dict['AUC'].append(numpy.nan)
        #data_dict['AUC_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get grip time
def var_griptime(min_response,data_dict,i_time_event,data,idx_stim_onset,stimulus_onset):
    increase,sld=0,0
    try:
        _data_=numpy.array(data)
        peaks, _ = find_peaks(_data_)
        largest_peak = peaks[numpy.argmax(_data_[peaks])]
        results_full95 = peak_widths(_data_, [largest_peak], rel_height=0.95)
        offset_to_largest_peak95 = int(results_full95[3][0])
        onset_to_largest_peak95 = int(results_full95[2][0])
        # for sld in range(len(data)):
        #     if data[sld+1]>data[sld] and sld>idx_stim_onset:
        #         increase+=1
        #     elif data[sld+1]<=data[sld]:
        #         increase=0
        #     if data[sld]>=min_response:
        #         RT_idx = sld-increase
        #         break
        # max_point = numpy.argmax(data)
        # dec_sig = data[max_point:]
        # dec_time = i_time_event[max_point:]
        # decrease,sld = 0,0
        # for sld in range(len(dec_sig)):
        #     if dec_sig[sld+1]>=dec_sig[sld]:
        #         decrease+=1
        #     elif dec_sig[sld+1]<dec_sig[sld]:
        #         decrease=0
        #     if decrease == 5:
        #         ST_idx = sld-5
        #         break 
        data_dict['GripDuration'].append(i_time_event[offset_to_largest_peak95]-i_time_event[onset_to_largest_peak95])
        #data_dict['GripLength_Norm'].append(data_dict['GripLength'][-1])
    except Exception as ex:
        data_dict['GripDuration'].append(numpy.nan)
        #data_dict['GripLength_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get rise time (10% to 90% duration)
def var_rise(min_response,data_dict,i_time_event,data,idx_stim_onset):
    increase,sld=0,0
    try:
        for sld in range(len(data)):
            if data[sld+1]>data[sld] and sld>idx_stim_onset:
                increase+=1
            elif data[sld+1]<=data[sld]:
                increase=0
            if data[sld]>=min_response:
                RT_idx = sld-increase
                break
        index_max = numpy.argmax(data)
        incr_sig = data[RT_idx:index_max]
        incr_time = i_time_event[RT_idx:index_max]
        idx10 = numpy.abs(incr_sig-(numpy.max(incr_sig)*10/100)).argmin()
        idx90 = numpy.abs(incr_sig-(numpy.max(incr_sig)*90/100)).argmin()
        data_dict['RiseTime'].append(incr_time[idx90]-incr_time[idx10])
        #data_dict['RiseTime_Norm'].append(data_dict['RiseTime'][-1])
    except Exception as ex:
        data_dict['RiseTime'].append(numpy.nan)
        #data_dict['RiseTime_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get fall time (90% to 10% duration)
def var_fall(data_dict,i_time_event,data):
    decrease,sld=0,0
    try:
        max_point = numpy.argmax(data)
        dec_sig = data[max_point:]
        for sld in range(len(dec_sig)):
            if dec_sig[sld+1]>=dec_sig[sld]:
                decrease+=1
            elif dec_sig[sld+1]<dec_sig[sld]:
                decrease=0
            if decrease == 5:
                ST_idx = sld-5
                ST_idx = ST_idx+len(data[:max_point])
                break 
        index_max = numpy.argmax(data)
        decr_sig = data[index_max:ST_idx]
        decr_time = i_time_event[index_max:ST_idx]
        idx10 = numpy.abs(decr_sig-(numpy.max(decr_sig)*90/100)).argmin()
        idx90 = numpy.abs(decr_sig-(numpy.max(decr_sig)*10/100)).argmin()
        data_dict['FallTime'].append(decr_time[idx90]-decr_time[idx10])
        #data_dict['FallTime_Norm'].append(data_dict['FallTime'][-1])
    except Exception as ex:
        data_dict['FallTime'].append(numpy.nan)
        #data_dict['FallTime_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get signal settling time
def var_set_time(data_dict,i_time_event,data,min_response,stimulus_onset):
    try: #find peak width and find 5% of signal
        _data_=numpy.array(data)
        peaks, _ = find_peaks(_data_)
        largest_peak = peaks[numpy.argmax(_data_[peaks])]
        results_full95 = peak_widths(_data_, [largest_peak], rel_height=0.95)
        offset_to_largest_peak95 = int(results_full95[3][0])
        onset_to_largest_peak95 = int(results_full95[2][0])

        data_dict['SettlingTime'].append(i_time_event[offset_to_largest_peak95]-i_time_event[onset_to_largest_peak95]+data_dict['RT_init'][-1]) 
    except Exception as ex:
        data_dict['SettlingTime'].append(numpy.nan)
        #data_dict['SettingTime_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get negative slope (descent)
def var_deslope(sample_rt,data_dict,data,data_norm,data_newton):
    try:
        max_point = numpy.argmax(data)
        max_point_norm = numpy.argmax(data_norm)
        slope = numpy.gradient(data[max_point:],sample_rt)
        slope_norm = numpy.gradient(data_norm[max_point_norm:],sample_rt)
        data_dict['DeSlope'].append(numpy.min(slope))
        data_dict['DeSlope_Norm'].append(numpy.min(slope_norm))
        
        max_point = numpy.argmax(data_newton)
        slope = numpy.gradient(data_newton[max_point:],sample_rt)
        data_dict['DeSlope_New'].append(numpy.min(slope))
    except Exception as ex:
        data_dict['DeSlope'].append(numpy.nan)
        data_dict['DeSlope_Norm'].append(numpy.nan)
        data_dict['DeSlope_New'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get max de-Acceleration
def var_deacc(sample_rt,data_dict,data,data_norm,data_newton):
    try:
        max_point = numpy.argmax(data)
        max_point_norm = numpy.argmax(data_norm)
        slope = numpy.gradient(data[max_point:],sample_rt)
        slope_norm = numpy.gradient(data[max_point_norm:],sample_rt)
        acc = numpy.gradient(slope,sample_rt)
        acc_norm = numpy.gradient(slope_norm,sample_rt)
        data_dict['DeAcceleration'].append(numpy.min(acc))
        data_dict['DeAcceleration_Norm'].append(numpy.min(acc_norm))
        
        max_point = numpy.argmax(data_newton)
        slope = numpy.gradient(data_newton[max_point:],sample_rt)
        acc = numpy.gradient(slope,sample_rt)
        data_dict['DeAcceleration_New'].append(numpy.min(acc))
    except Exception as ex:
        data_dict['DeAcceleration'].append(numpy.nan)
        data_dict['DeAcceleration_Norm'].append(numpy.nan)
        data_dict['DeAcceleration_New'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get anticipation max values
def var_antmax(idx_ant_onset,data_dict,fbi_left_event,fbi_right_event,
                fbi_left_event_norm,fbi_right_event_norm):
    try:
        data_dict['MaxANTleft'].append(numpy.max(fbi_left_event[idx_ant_onset:]))
        data_dict['MaxANTright'].append(numpy.max(fbi_right_event[idx_ant_onset:]))
        data_dict['MaxANTleft_Norm'].append(numpy.max(fbi_left_event_norm[idx_ant_onset:]))
        data_dict['MaxANTright_Norm'].append(numpy.max(fbi_right_event_norm[idx_ant_onset:]))
    except Exception as ex:
        data_dict['MaxANTleft'].append(numpy.nan)
        data_dict['MaxANTright'].append(numpy.nan)
        data_dict['MaxANTleft_Norm'].append(numpy.nan)
        data_dict['MaxANTright_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict

# Get anticipation AUC
def var_antauc(idx_ant_onset,data_dict,i_time_event,fbi_left_event,fbi_right_event,
               fbi_left_event_norm,fbi_right_event_norm):
    try:
        data_dict['AucANTleft'].append(integrate.simpson(fbi_left_event[idx_ant_onset:],i_time_event[idx_ant_onset:]))
        data_dict['AucANTright'].append(integrate.simpson(fbi_right_event[idx_ant_onset:],i_time_event[idx_ant_onset:]))
        data_dict['AucANTleft_Norm'].append(integrate.simpson(fbi_left_event_norm[idx_ant_onset:],i_time_event[idx_ant_onset:]))
        data_dict['AucANTright_Norm'].append(integrate.simpson(fbi_right_event_norm[idx_ant_onset:],i_time_event[idx_ant_onset:]))
    except Exception as ex:
        data_dict['AucANTleft'].append(numpy.nan)
        data_dict['AucANTright'].append(numpy.nan)
        data_dict['AucANTleft_Norm'].append(numpy.nan)
        data_dict['AucANTright_Norm'].append(numpy.nan)
        print(ex)
        traceback.print_exc()
    return data_dict






