import numpy, traceback
from scipy import integrate

def nogos(data_dict,fbi_left_event,fbi_right_event,fbi_left_event_norm,
          fbi_right_event_norm, i_time_event,idx_ant_onset,idx_stim_onset,len_keylist):
    
    data_dict = {key: (value + [numpy.nan] if 18 < key_idx < len_keylist else value) for key_idx, (key, value) in enumerate(data_dict.items())}


    data_dict['MaxNOGOleft'].append(numpy.max(fbi_left_event[idx_stim_onset:idx_ant_onset]))
    data_dict['MaxNOGOright'].append(numpy.max(fbi_right_event[idx_stim_onset:idx_ant_onset]))
    data_dict['MaxNOGOleft_Norm'].append(numpy.max(fbi_left_event_norm[idx_stim_onset:idx_ant_onset]))
    data_dict['MaxNOGOright_Norm'].append(numpy.max(fbi_right_event_norm[idx_stim_onset:idx_ant_onset]))
    # data_dict['MaxANTleft'].append(numpy.max(fbi_left_event[idx_ant_onset:]))
    # data_dict['MaxANTright'].append(numpy.max(fbi_right_event[idx_ant_onset:]))
    # data_dict['MaxANTleft_Norm'].append(numpy.max(fbi_left_event_norm[idx_ant_onset:]))
    # data_dict['MaxANTright_Norm'].append(numpy.max(fbi_right_event_norm[idx_ant_onset:]))
    
    try:
        data_dict['AucNOGOleft'].append(integrate.simpson(fbi_left_event[idx_stim_onset:idx_ant_onset],i_time_event[idx_stim_onset:idx_ant_onset]))
        data_dict['AucNOGOleft_Norm'].append(integrate.simpson(fbi_left_event_norm[idx_stim_onset:idx_ant_onset],i_time_event[idx_stim_onset:idx_ant_onset]))
    except Exception as ex:
        data_dict['AucNOGOleft'].append(0)
        data_dict['AucNOGOleft_Norm'].append(0)
        print(ex)
        traceback.print_exc()

    try:
        data_dict['AucNOGOright'].append(integrate.simpson(fbi_right_event[idx_stim_onset:idx_ant_onset],i_time_event[idx_stim_onset:idx_ant_onset]))
        data_dict['AucNOGOright_Norm'].append(integrate.simpson(fbi_right_event_norm[idx_stim_onset:idx_ant_onset],i_time_event[idx_stim_onset:idx_ant_onset]))
    except Exception as ex:
        data_dict['AucNOGOright'].append(0)
        data_dict['AucNOGOright_Norm'].append(0)
        print(ex)
        traceback.print_exc()

    # try:
    #     data_dict['AucANTleft'].append(integrate.simpson(fbi_left_event[idx_ant_onset:],i_time_event[idx_ant_onset:]))
    #     data_dict['AucANTleft_Norm'].append(integrate.simpson(fbi_left_event_norm[idx_ant_onset:],i_time_event[idx_ant_onset:]))
    # except Exception as ex:
    #     data_dict['AucANTleft'].append(0)
    #     data_dict['AucANTleft_Norm'].append(0)
    #     print(ex)
    #     traceback.print_exc()

    # try:
    #     data_dict['AucANTright'].append(integrate.simpson(fbi_right_event[idx_ant_onset:],i_time_event[idx_ant_onset:]))
    #     data_dict['AucANTright_Norm'].append(integrate.simpson(fbi_right_event_norm[idx_ant_onset:],i_time_event[idx_ant_onset:]))
    # except Exception as ex:
    #     data_dict['AucANTright'].append(0)
    #     data_dict['AucANTright_Norm'].append(0)
    #     print(ex)
    #     traceback.print_exc()

    return data_dict