import joblib
import xarray as xr
import pandas as pd
import gc

gc.enable()

def shap_analysis(province_no):

    model_path = '/data/datasets/Projects/TuringCoccolithophoreBlooms/no_backup/TuringCoccolithophoreBlooms/models/random_forest_'+str(province_no)+'.joblib'
    rf_1 = joblib.load(open(model_path, "rb"))

    province_file = '/data/datasets/Projects/TuringCoccolithophoreBlooms/no_backup/TuringCoccolithophoreBlooms/province_dataframes/province_'+str(province_no)+'.nc'
    d_1 = xr.load_dataset(province_file)

    #slices
    slice_1 = slice('1998-01-01','2000-12-01')
    slice_2 = slice('2001-01-01','2004-12-01')
    slice_3 = slice('2005-01-01','2008-12-01')
    slice_4 = slice('2009-01-01','2012-12-01')
    slice_5 = slice('2013-01-01','2016-12-01')


    #fold 3
    test_1 = d_1.sel(time=slice_3)


    stacked = d_1.stack(coord=['longitude', 'latitude']).rrs.to_dataframe()
    stacked.drop(columns=['spatial_ref','longitude', 'latitude'],inplace=True)
    stacked.dropna(inplace=True)
    stacked.reset_index(drop=True,inplace=True)
    std_1 = stacked.std()[0]

    del stacked
    gc.collect()
    
    del d_1
    gc.collect()
    
    stacked_test = test_1.stack(coord=['longitude', 'latitude']).to_dataframe()
    stacked_test.drop(columns=['spatial_ref','longitude', 'latitude'],inplace=True)
    stacked_test.dropna(inplace=True)
    stacked_test.reset_index(drop=True,inplace=True)

    stacked_test['rrs'].where(stacked_test['rrs']<std_1, other=1, inplace=True)
    rrs_ones = (stacked_test['rrs'] == 1).sum()
    rrs_zeros = (stacked_test['rrs'] == 0).sum()

    non_zero = stacked_test.loc[stacked_test['rrs'] == 1.]
    non_zero = non_zero[stacked_test.columns]

    zero = stacked_test.loc[stacked_test['rrs'] == 0.]
    zero = zero[stacked_test.columns]
    zero_samp = zero.sample(rrs_ones)

    full_test_1 = pd.concat([zero,non_zero])
    X_test_1 = full_test_1.drop(columns='rrs')
    y_test_1 = full_test_1['rrs']

    test_accuracy = rf_1.score(X_test_1, y_test_1)

    import shap
    sh_1 = shap.TreeExplainer(rf_1,X_test_1,model_output='probability',feature_perturbation='interventional')

    try:
        sample_1 = X_test_1.sample(2000)
    except:
        sample_1 = X_test_1

    sh_val_1 = sh_1.shap_values(sample_1)

    from matplotlib.colors import LinearSegmentedColormap
    colors = [(0, 24/255, 95/255),(0, 154/255, 162/255),(126/255, 201/255, 201/255),(173/255, 255/255, 251/255)]#,'#C5FFFC']
    cmap = LinearSegmentedColormap.from_list('coccolithphores', colors, N=100)

    import matplotlib.pyplot as plt
    shap.summary_plot(sh_val_1[1],sample_1,plot_type='dot',cmap=cmap,show=False) #show=False)
    ax = plt.gca()
    ax.set_xlim(-0.4, 0.4) 
    plt.title('Province '+str(province_no))
    plt.savefig('/home/jovyan/lustre_scratch/Figures/model_shap_analysis_redo/province_'+str(province_no)+'.png')
    plt.show()
   
    import csv
    import numpy as np
    a = [str(province_no),str(round(test_accuracy, 3))]
    print(np.shape(sh_val_1[1]))


    global_values = [np.mean(i) for i in np.rollaxis(abs(sh_val_1[1]), 1)]
    print(global_values)
    names = ['Province_no','Score']
    names = names+X_test_1.columns.values.tolist()
    print(names)
    array = [province_no,test_accuracy]
    array = array+global_values
    print(np.shape(np.array(array).reshape(1,-1)))
    import numpy as np
    df = pd.DataFrame(np.array(array).reshape(1,-1),index=[0],columns=names)
    
    output_path = '/home/jovyan/lustre_scratch/Figures/model_shap_analysis_redo/model_analysis.csv'

    import os
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

    #with open('/home/jovyan/lustre_scratch/Figures/model_shap_analysis/model_scores.csv', "a", newline="") as f:
    #    wr
    #    writer.writerows(a)

