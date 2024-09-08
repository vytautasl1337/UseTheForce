from scipy import signal

def myFilter(i_time_event,bi_left_event,bi_right_event, 
             bi_left_event_norm, bi_right_event_norm,
             bi_right_event_newton,bi_left_event_newton):
    time_length = i_time_event[-1]-i_time_event[0]
    nyquist  = (len(i_time_event)/time_length)/2
    freq=15
    cutoff = freq/nyquist
    b, a = signal.butter(2, cutoff, btype = 'lowpass')
    
    # Filter raw data
    fbi_left_event = signal.filtfilt(b, a, bi_left_event)
    fbi_right_event = signal.filtfilt(b, a, bi_right_event)
    # Filter normalized data
    fbi_left_event_norm = signal.filtfilt(b,a,bi_left_event_norm)
    fbi_right_event_norm = signal.filtfilt(b,a,bi_right_event_norm)
    # Filter data in Newtons
    fbi_left_event_newton = signal.filtfilt(b, a, bi_left_event_newton)
    fbi_right_event_newton = signal.filtfilt(b, a, bi_right_event_newton)
        
    return fbi_left_event, fbi_right_event, fbi_left_event_norm, fbi_right_event_norm, fbi_right_event_newton, fbi_left_event_newton