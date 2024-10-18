import warnings
warnings.filterwarnings('ignore')
import statistics
import scipy
import pandas as pd
import numpy as np
import json
from json import load,dump,loads,dumps
import matplotlib.pyplot as plt

# function name: get_distribution_statistics
# purpose: analyse a given numeric variable
# input: a list containing the values of a numeric variable
# ouput: a json object that contains the statistics 

def get_distribution_statistics(orig_vector:list)->json:

    vector=[]
    for val in orig_vector:
        if pd.isnull(val)==False:
            vector.append(val)
  
    stats=dict()
    stats["missing_value_percentage"]= round(pd.Series(orig_vector).isna().sum()/len(orig_vector)*100.00,3)
    stats["count"]=len(vector)
    stats["min"]=min(vector)
    stats["max"]=max(vector)
    stats["range"]=stats["max"]-stats["min"]
    stats["mean"]=np.nanmean(vector)
    stats["median"]=np.nanmedian(vector)
    stats["mode"]=statistics.mode(vector)
    stats["skew"]=scipy.stats.skew(vector,bias=False)
    stats["kurtosis"]=scipy.stats.kurtosis(vector,bias=False)
    stats["25th_percentile"]=np.percentile(vector,25)
    stats["50th_percentile"]=np.percentile(vector,50)
    stats["75th_percentile"]=np.percentile(vector,75)
    stats["IQR"]=stats["75th_percentile"]-stats["25th_percentile"]
    stats["std"]=np.nanstd(vector)
    

    stats["range_one_std"]=dict()

    stats["range_one_std"]["mean-1std"]=stats["mean"]-1*stats["std"]
    stats["range_one_std"]["mean+1std"]=stats["mean"]+1*stats["std"]

    stats["upper_bound"]=stats["75th_percentile"]+stats["IQR"]*1.5
    stats["lower_bound"]=stats["25th_percentile"]-stats["IQR"]*1.5

    if stats["IQR"]<abs(stats["std"])*2:
        stats["is_jamed"]=1
    else:
        stats["is_jamed"]=0


    if stats["kurtosis"] >= 3:
        stats["is_fat_tailed"]=1
    else:
        stats["is_fat_tailed"]=0
    

    if stats["skew"] >1:
        stats["skew_type"]='highly_positively_skewed'
        
    elif stats["skew"] <-1:
        stats["skew_type"]='highly_negatively_skewed'

    elif stats["skew"] >0.5:
        stats["skew_type"]='moderately_positivel_skewed'

    elif stats["skew"] <-0.5:
        stats["skew_type"]='moderately_negatively_skewed'   

    else:
        stats["skew_type"]='approximately_symmetric'


    if(len(vector)<=50):
        if(scipy.stats.shapiro(vector).pvalue<=0.05):
            stats["is_normally_distributed"]=False
        else:
            stats["is_normally_distributed"]=True
    else:
        if(scipy.stats.kstest(vector, "norm").pvalue<=0.05):
            stats["is_normally_distributed"]=False
        else:
            stats["is_normally_distributed"]=True

    stats["outliers"]=return_outliers(vector,stats["is_normally_distributed"])

    stats["proportion_outliers (%)"]=round(len(list(stats["outliers"]))/len(vector)*100,3)
        
    # stats["z_scores"]=scipy.stats.zscore(vector)

    return stats


def return_outliers(vector,is_normal=False)->list:
    outliers=[]
    if is_normal:
        z_scores=scipy.stats.zscore(vector)
        for i in range(len(vector)):
            if(z_scores[i]>3):
                outliers.append((vector[i],z_scores[i]))
    else:
        iqr=scipy.stats.iqr(vector)
        lower_limit=np.percentile(vector,25)-iqr*1.5
        upper_limit=np.percentile(vector,75)+iqr*1.5
        for i in range(len(vector)):
            if(vector[i]<lower_limit or vector[i]>upper_limit):
                outliers.append(vector[i])
        
    return outliers

