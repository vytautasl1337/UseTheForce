import numpy

def baseline(i_left_event,i_right_event,right_run,left_run,
             idx_iti_onset,idx_stim_onset,i_left_event_norm,i_right_event_norm,
             slopeL,interceptL,slopeR,interceptR):

    bi_right_event = [x-(numpy.mean(right_run[idx_iti_onset:idx_stim_onset])) for x in i_right_event]
    bi_left_event = [x-(numpy.mean(left_run[idx_iti_onset:idx_stim_onset])) for x in i_left_event]
    # Baseline normalized data
    bi_right_event_norm = [x-numpy.mean(i_right_event_norm[1:50]) for x in i_right_event_norm]
    bi_left_event_norm = [x-numpy.mean(i_left_event_norm[1:50]) for x in i_left_event_norm]
    
    #--- TRANSFORM DATA INTO NEWTONS AND BASELINE---#
    from functions.preprocessing.newton import to_newtons
    left_newton,right_newton = to_newtons(i_right_event,i_left_event,slopeL,interceptL,slopeR,interceptR)
    
    bi_right_event_newton = [x-(numpy.mean(right_newton[1:50])) for x in right_newton]
    bi_left_event_newton = [x-(numpy.mean(left_newton[1:50])) for x in left_newton]
    
    return bi_right_event, bi_left_event,bi_right_event_norm, bi_left_event_norm, bi_right_event_newton, bi_left_event_newton