def dictionary_(question_table):
    
    global data_dict
    # Create dictionary
    keylist = ['id','delay','group','SubjectNr','age','gender','calibration',
               'Run','BlockNr','TrialNr','TotalTrialNr',
               'FaceGender','FaceEmotion','RewardPromise',
               'RewardReceived','SymbolTarget','GripResponse',
               'Correct','Mirror',
               'RT_init','RT_acc','RT_99','RT_95',
               'RiseTime','FallTime',
               'MaxGrip','MaxGrip_Norm','MaxGrip_New',
               'MaxTime',
               'Slope','Slope_Norm','Slope_New',
               'DeSlope','DeSlope_Norm','DeSlope_New',
               'SettlingTime',
               'AUC',#'AUC_Norm',
               'GripDuration',
               'Acceleration','Acceleration_Norm','Acceleration_New',
               'DeAcceleration','DeAcceleration_Norm','DeAcceleration_New',
               
               'MaxNOGOleft','MaxNOGOleft_Norm',
               'MaxNOGOright','MaxNOGOright_Norm',
               'AucNOGOleft','AucNOGOleft_Norm',
               'AucNOGOright','AucNOGOright_Norm',
               'MaxANTleft','MaxANTleft_Norm',
               'MaxANTright','MaxANTright_Norm',
               'AucANTleft','AucANTleft_Norm',
               'AucANTright','AucANTright_Norm']
    
    len_keylist = keylist.index('MaxNOGOleft')
    
    #len_keylist = len(keylist)
    
    data_dict = {key: [] for key in keylist}
    
    dict_ext = 1
    if question_table.shape[1]>7:
        #dict_ext = 1
        colNames = list(question_table.columns[7:].values)
        logNames = ['log_' + s for s in colNames]
        var_output = {}

        for string, key in zip(logNames, colNames):
            locals()[string] = []
            var_output[key] = locals()[string]
            
        data_dict.update(var_output)
    return data_dict,dict_ext,len_keylist
    
    