import pandas as pd
import numpy as np

# Machine Learning Library
from sklearn.svm import NuSVR
from hyperopt import hp

def nusvr(X_train, y_train, hyperparameter_dictionary):
    """ X_train: Input of Training Data
        y_train: Output of Training Data 
        hyperparameter_dictionary: A dictionary of 'hyperparamter names' as keys and 'list for ranges or categories' as values"""
    
    #####################################################################################################
    ########### Separating Hyperparameter Names and Values from Hyperparameter Dictionary ###############
    #####################################################################################################
    
    # Getting List of hyperparamter names from hyperparamter_dictionary
    hyperparamter_name_list= list(hyperparameter_dictionary.keys())
    
    # Getting List of hyperparamter values from hyperparamter_dictionary
    hyperpramter_value_list= [];
    for i in range(len(hyperparamter_name_list)): 
        hyperpramter_value_list.append(hyperparameter_dictionary[hyperparamter_name_list[i]])

    ######################################################################################################
    ####################################### 1. Objective Function ########################################
    ######################################################################################################
    scores= [];
    def objective(hyperparameters):
        """ Objective function to minimize error """
        print(hyperparameters)
        # Importing machine learning model
        
        # Putting the arguements for the machine learning model into one string
        arg= '';
        for i in range(len(hyperparamter_name_list)):
            
            # Check if hyperparameter type is int
            if(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])== int):
                arg= arg+hyperparamter_name_list[i]+'='+str(int(hyperparameters[i]))  
            # Check if hyperparameter type is str
            elif(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])== str):
                arg= arg+hyperparamter_name_list[i]+'= \''+str((hyperparameters[i]))+'\'' 
            # Else for hyperparameter type bool or float values    
            else:
                arg= arg+hyperparamter_name_list[i]+'='+str((hyperparameters[i]))
                
            if(i!=(len(hyperparamter_name_list)-1)):
                arg=arg+','
        
        function= 'reg= NuSVR('+arg+')'
        #reg= BayesianRidge(compute_score=True, verbose=verbose, alpha_1=alpha_1, alpha_2= alpha_2)
        
        # Executing the string which gives the model along with its arguemnts
        #exec(function)
        
        def get_model(function):
            ldict = {}
            exec(function,globals(),ldict)
            reg = ldict['reg']
            return reg
        
        reg= get_model(function)
        
        # Cross validating the model with training data
        from sklearn.model_selection import cross_validate
        cv_results = cross_validate(reg, X_train, y_train, cv=5, scoring= 'neg_mean_squared_error')
        
        # Taking average score from cross validating result
        score= -1*np.mean(cv_results['test_score'])
        

        scores.append(score)
        return score
    
    #######################################################################################################
    ###################################### 2. Domain Space ################################################
    #######################################################################################################
    space= 'domain= [';
    for i in range(len(hyperparamter_name_list)):
        # String Value
        if(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])==str or type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])==bool):
            space= space+'hp.choice(' + '\'' + str(hyperparamter_name_list[i]) +'\',' + str(hyperparameter_dictionary[hyperparamter_name_list[i]]) + ')'
        # Integer Value
        elif(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])==int):
            space= space+'hp.quniform(' + '\'' + str(hyperparamter_name_list[i]) +'\',' + str(hyperparameter_dictionary[hyperparamter_name_list[i]])[1:-1] + ',1)'
        # Floating Value
        elif(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])==float):
            space= space+'hp.uniform(' + '\'' + str(hyperparamter_name_list[i]) +'\',' + str(hyperparameter_dictionary[hyperparamter_name_list[i]])[1:-1] + ')'

        if (i!= (len(hyperparamter_name_list)-1)):
            space= space+','
    space= space+']'

    def get_domain(space):
        ldict = {}
        exec(space,globals(),ldict)
        domain = ldict['domain']
        return domain
    
    domain= get_domain(space)

    

    ########################################################################################################
    ################################### 3. Optimization Algortihm ##########################################
    ########################################################################################################
    from hyperopt import tpe
    # Create the algorithm
    tpe_algo = tpe.suggest
    
    ########################################################################################################
    ######################################### 4. Results ###################################################
    ########################################################################################################
    from hyperopt import Trials
    # Create a trials object
    tpe_trials = Trials()
    
    ########################################################################################################
    ######################################## 5. Optimization ###############################################
    ########################################################################################################
    
    from hyperopt import fmin
    # Run 200 evals with the tpe algorithm
    tpe_best = fmin(fn=objective, space=domain, 
                    algo=tpe_algo, trials=tpe_trials,
                    max_evals=100)
    print(tpe_best)
    
#    import matplotlib.pyplot as plt
#    plt.figure(num=None, figsize=(8, 6))
#    plt.plot(scores, 'r-')
#    plt.xlabel('Number of Itteration')
#    plt.ylabel('Average Cross Validation Score')
    
    
    #########################################################################################################
    ################################### 6. Final Optimized Model ############################################
    #########################################################################################################

    
#     reg = BayesianRidge(compute_score=True, verbose=True,  alpha_1=tpe_best['alpha_1'], alpha_2= tpe_best['alpha_2'])
#     reg.fit(X_train, y_train)
    
    
    # Putting the arguements for the machine learning model into one string
    arg= '';
    for i in range(len(hyperparamter_name_list)):

        # Check if hyperparameter type is int
        if(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])== int):
            arg= arg+hyperparamter_name_list[i]+'='+str(int(tpe_best[hyperparamter_name_list[i]]))  
        # Check if hyperparameter type is str
        elif(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])== str):
            arg= arg+hyperparamter_name_list[i]+'= \''+str(hyperparameter_dictionary[hyperparamter_name_list[i]][tpe_best[hyperparamter_name_list[i]]])+'\'' 
        # Else for hyperparameter type bool or float values    
        elif(type(hyperparameter_dictionary[hyperparamter_name_list[i]][0])== bool):
            if str((tpe_best[hyperparamter_name_list[i]]))=='1':
                arg= arg+hyperparamter_name_list[i]+'='+'True'
            else:
                arg= arg+hyperparamter_name_list[i]+'='+'False'
        else:
            arg= arg+hyperparamter_name_list[i]+'='+str((tpe_best[hyperparamter_name_list[i]]))

        if(i!=(len(hyperparamter_name_list)-1)):
            arg=arg+','

    function= 'reg= NuSVR('+arg+')'
    
    
    def get_model(function):
        ldict = {}
        exec(function,globals(),ldict)
        reg = ldict['reg']
        return reg
        
    reg= get_model(function)
    reg.fit(X_train, y_train)
    
    return reg