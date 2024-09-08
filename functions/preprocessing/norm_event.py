
def norm_event(max_grip_left,max_grip_right,source_left_event,source_right_event):
    source_left_event_norm=[x/max_grip_left for x in source_left_event]
    source_right_event_norm=[x/max_grip_right for x in source_right_event]
    return source_left_event_norm,source_right_event_norm