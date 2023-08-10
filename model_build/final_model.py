import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from imblearn.ensemble import BalancedRandomForestClassifier, EasyEnsembleClassifier
import seaborn as sns
import xarray as xr
from progress.bar import Bar
import gc

gc.enable()


def build_model_function(province_no):

    
#---LOAD DATA    
    filename = '/data/datasets/Projects/TuringCoccolithophoreBlooms/no_backup/TuringCoccolithophoreBlooms/province_dataframes/province_'+str(province_no)+'.nc'
    d = xr.load_dataset(filename)

    #Set up slices - used for crossvalidation (not shown in this model build)
    slice_0 = slice('1992-01-01','1995-12-01')
    slice_1 = slice('1996-01-01','2000-12-01')
    slice_2 = slice('2001-01-01','2004-12-01')
    slice_3 = slice('2005-01-01','2008-12-01')
    slice_4 = slice('2009-01-01','2012-12-01')
    slice_5 = slice('2013-01-01','2016-12-01')


    gc.collect()    

#---CALCULATE STANDARD DEVIATION ON FULL TIME SERIES
    stacked = d.stack(coord=['longitude', 'latitude']).to_dataframe()
    stacked.drop(columns=['spatial_ref','longitude', 'latitude'],inplace=True)
    stacked.dropna(inplace=True)
    stacked.reset_index(drop=True,inplace=True)
    std = stacked.rrs.std()
    print(std)

    del stacked
    gc.collect()

#---SPLIT TEST AND TRAINING
    training = xr.concat([d.sel(time=slice_0),d.sel(time=slice_1),d.sel(time=slice_2),d.sel(time=slice_4),d.sel(time=slice_5)],'time')
    test = d.sel(time=slice_3)   
 

#---SET UP DATA FOR MODEL BUILD
    from sklearn.metrics import confusion_matrix

    stacked_train = training.stack(coord=['longitude', 'latitude']).to_dataframe()
    stacked_test = test.stack(coord=['longitude', 'latitude']).to_dataframe()
    
    stacked_train.drop(columns=['spatial_ref','longitude', 'latitude'],inplace=True)
    stacked_test.drop(columns=['spatial_ref','longitude', 'latitude'],inplace=True)

    #remove any pixels with NaN values
    stacked_train.dropna(inplace=True)
    stacked_test.dropna(inplace=True)
    
    stacked_train.reset_index(drop=True,inplace=True)
    stacked_test.reset_index(drop=True,inplace=True)
    print(stacked_train.rrs.std())
    stacked_train['rrs'].where(stacked_train['rrs']<std, other=1, inplace=True) #set values higher than std to 1

#---CLASSIFY PIXELS FOR TRAINING DATA
    #Note we only retrain 0 and 1 (0<rrs<std are discarded)
    rrs_ones = (stacked_train['rrs'] == 1).sum()
    rrs_zeros = (stacked_train['rrs'] == 0).sum()

    non_zero = stacked_train.loc[stacked_train['rrs'] == 1.]
    non_zero = non_zero[stacked_train.columns]
    print(non_zero.shape)
    zero = stacked_train.loc[stacked_train['rrs'] == 0.]
    zero = zero[stacked_train.columns]
    #zero_samp = zero.sample(rrs_ones)

    full = pd.concat([zero,non_zero])
    print(len(full))
    stacked_train=full.sample(10000)
    
#---CLASSIFY PIXELS FOR TEST DATA    
    stacked_test['rrs'].where(stacked_test['rrs']<std, other=1, inplace=True)
    rrs_ones = (stacked_test['rrs'] == 1).sum()
    rrs_zeros = (stacked_test['rrs'] == 0).sum()

    non_zero = stacked_test.loc[stacked_test['rrs'] == 1.]
    non_zero = non_zero[stacked_test.columns]

    zero = stacked_test.loc[stacked_test['rrs'] == 0.]
    zero = zero[stacked_test.columns]
    zero_samp = zero.sample(rrs_ones)

    full_test = pd.concat([zero_samp,non_zero])
    stacked_test=full_test
    print(stacked_test.describe())
    
    gc.collect()

#---BUILD MODEL    
    X_train = stacked_train.drop(columns='rrs')
    y_train = stacked_train['rrs']
    
    X_test = stacked_test.drop(columns='rrs')
    y_test = stacked_test['rrs']
    
    rf = BalancedRandomForestClassifier(class_weight='balanced_subsample',n_estimators=500, max_depth=10)#, n_jobs=-1) 
    
    rf.fit(X_train,y_train)
    
    gc.collect()
    
    cuml_train_accuracy = rf.score(X_train, y_train)
    cuml_test_accuracy = rf.score(X_test, y_test)
    print(f'Training accuracy fold = {cuml_train_accuracy}, Test accuracy fold = {cuml_test_accuracy}')
    
    cm = confusion_matrix(y_test,rf.predict(X_test))/y_test.size
    fig, ax = plt.subplots(1,1)
    sns.heatmap(cm, annot=True, fmt='.2%', cmap='Blues')
    plt.savefig('/home/jovyan/lustre_scratch/models/province_'+str(province_no)+'_redo.png') 


#---SAVE OUT MODEL
    import joblib
    joblib.dump(rf, "/home/jovyan/lustre_scratch/models/random_forest_"+str(province_no)+".joblib", compress=3) 

    gc.collect()


for i in np.arange(0,52):
    build_model_function(i)
