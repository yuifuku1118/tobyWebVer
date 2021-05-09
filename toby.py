from platform import processor
from tkinter import*
from tkinter import messagebox
from pandas import Series,DataFrame
import pandas as pd
import numpy as np
from processor import pre_process, processing
from reply import autoreply, simple_reply, caretext, MLreply
import random
from threading import Timer
import time

####### train MLP and give a pridiction on input #####################################################################################################################################################################

def MLpredict(x):
    
    df = pd.read_csv("train.csv")

    df_X = df.copy()
    df_Y = df.copy()

    drop_idx = ["Y"]
    df_X = df_X.drop(drop_idx, axis = 1)


    drop_idx = ["because","you","me","question","fiveWH","length","JJ_score","fscore"]
    df_Y = df_Y.drop(drop_idx, axis = 1)

    test_index = x

    #MLPClassifier
    from sklearn.neural_network import MLPClassifier
    my_classifier = MLPClassifier(solver='lbfgs', random_state=0)
    my_classifier.fit(df_X,df_Y.values.ravel())
    # Predict 
    print(my_classifier.predict(test_index))
    return my_classifier.predict(test_index)

######################################################################################################################################################################################################################

################## main function ######################################################################################################################################################################################
    
def main(text):
    score = 0
    text = text.lower()
    z, possibleres = autoreply(text)
    res = ''
    if z != 1:
        list1 = pre_process(text)
        x = processing(list1[0],list1[1],list1[2],list1[3],list1[4])
        score += x[1]
        if x[1] != 0:           
            y = MLpredict(x[0])
            i, res = MLreply(y)
            if i == [-2]:
                res = caretext()
        else:
            res = simple_reply()     
        print(res)
    else:
        res = possibleres
    return res,score, list1[5]

#######################################################################################################################################################################################################################





