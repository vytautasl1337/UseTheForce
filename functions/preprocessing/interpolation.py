import numpy
def interpol(source_time_event,source_left_event,source_right_event,source_left_event_norm,source_right_event_norm):
    
    sampling_frq = 120
    sample_rt = 1/sampling_frq  #(120Hz)
    
    i_time_event = numpy.arange(source_time_event[0],source_time_event[-1],sample_rt)
    i_left_event = numpy.interp(i_time_event,source_time_event,source_left_event)
    i_right_event = numpy.interp(i_time_event,source_time_event,source_right_event)
    # Normalized data interpolation
    i_left_event_norm = numpy.interp(i_time_event,source_time_event,source_left_event_norm)
    i_right_event_norm = numpy.interp(i_time_event,source_time_event,source_right_event_norm)
    
    return i_time_event,i_left_event,i_right_event,i_left_event_norm,i_right_event_norm,sample_rt