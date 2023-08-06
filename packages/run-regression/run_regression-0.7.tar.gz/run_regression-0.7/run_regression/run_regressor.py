# import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Preprocessing modules
from run_regression.data_preprocessing.handle_missing import MissingValues
from run_regression.data_preprocessing.remove_outliers import Outliers
from run_regression.data_preprocessing.remove_constant_columns import ConstantColumns
from run_regression.data_preprocessing.normalize_numerical_columns import Standardize
from run_regression.data_preprocessing.encode_categorical_data import Encode


# Models module
# Machine Learning Funtions
from run_regression.models.NUSVRFunction import nusvr
from run_regression.models.ElasticNetFunction import elasticnet
from run_regression.models.RidgeRegressionFunction import ridge
from run_regression.models.BayesianRidgeRegressionModel import bayesianridge
from run_regression.models.RandomForestRegressorFunction import randomforestregressor

def reg_main(model_configurations, data_filename):
    
    # model_configurations
    input_features = 'Auto'
    target_feature = 'CD'
    model = 'randomforestregressor'
    hyperparameters = {'n_estimators': [10,1000], 'min_samples_split':[2, 10], 'max_features':['auto', 'sqrt', 'log2']}
    
    ###############################################################################
    ############################ 1. Read Data #####################################
    ###############################################################################
    # Read Filename
    try:
        df= pd.read_csv(data_filename, encoding ='latin1')
    except:
        df= pd.read_excel(data_filename)





    ###############################################################################
    ############################ 2. Data Preprocess ###############################
    ###############################################################################
    missing_values = MissingValues()
    remove_outliers = Outliers()
    remove_constant_columns = ConstantColumns()
    normalize_numerical_columns = Standardize ()
    encode_categorical_data = Encode()
    
    df = missing_values.fit_transform(df)
    df = remove_constant_columns.fit_transform(df)
    #df = remove_outliers.fit_transform(df)
    normalize_numerical_columns.strategy = 'MinMax'
    df = normalize_numerical_columns.transform(df)
    df = encode_categorical_data.transform(df)
    
    
    
    ###############################################################################
    ############################ 3. Test-Train Split ##############################
    ###############################################################################
    
    columns = list(df)
    
    # y_columns = ['rate_retention']
    #y_columns = ['CD']
    y_columns = [target_feature]
    
    if input_features == 'Auto':
        x_columns = list(set(columns)-set(y_columns))
    else:
        x_columns = input_features
    
    x = df[x_columns]
    y = df[y_columns]
    

    
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
    print(X_train)
    
    #y_test = np.concatenate(y_test.values, axis=0 )
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    ###############################################################################
    ############################ 4. Model Building ################################
    ###############################################################################
    # Hyperparamter Dictionary
    hyperparameter_dictionary = hyperparameters
    
    # Make string for execution
    function = 'reg= '+ model + '(X_train, y_train, hyperparameter_dictionary)'

    # Execution Function
    def get_model(function, X_train, y_train, hyperparameter_dictionary):
        ldict = {'X_train': X_train, 'y_train': y_train, 'hyperparameter_dictionary': hyperparameter_dictionary}
       # glist = {'X_train': X_train, 'y_train': y_train, 'hyperparameter_dictionary: hyperparameter_dictionary}
        exec(function, globals(),ldict)
        reg = ldict['reg']
        return reg
    
    # Machine Learning Model
    reg = get_model(function, X_train, y_train, hyperparameter_dictionary)

    ###############################################################################
    ############################### 5. Predict ####################################
    ###############################################################################
    y_predict= reg.predict(X_test)


    ###############################################################################
    ############################### 6. Visualize ##################################
    ###############################################################################
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_squared_error
    print('MSE: '+str(mean_squared_error(y_test, y_predict)))
    
    strng = target_feature
    plt.xlabel('Actual ' + strng)
    plt.ylabel('Predicted ' + strng)
    
    
    y_plot = np.ravel(y)
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(y_plot,y_plot)
    
    line= slope*np.array(y_plot)+intercept
    # Plot prediction    
    plt.plot(y_plot, y_plot, 'g', label = 'Actual')
    
    # Scatter Test
    plt.scatter(y_test, y_predict,c ='b', label = 'Test Data')
    
    # Scatter Train
    y_train_pred = reg.predict(X_train)
    plt.scatter(y_train, y_train_pred, c ='r', label = 'Train Data')
    

    #plt.plot(y_train, 'ro', y_test, line)
    #y = reg.predict(X_train)
    plt.legend()
    
    ###############################################################################
    ############################## Return #########################################
    ###############################################################################
    return plt


