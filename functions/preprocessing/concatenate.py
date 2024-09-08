import numpy

def concat(times, left, right, list_of_blocks, i):

    time_run = numpy.asarray(numpy.reshape((numpy.concatenate(times[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
    left_run = numpy.asarray(numpy.reshape((numpy.concatenate(left[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
    right_run = numpy.asarray(numpy.reshape((numpy.concatenate(right[(list_of_blocks[i]):(list_of_blocks[i+1])], axis = 1)),-1))
    return time_run,left_run,right_run