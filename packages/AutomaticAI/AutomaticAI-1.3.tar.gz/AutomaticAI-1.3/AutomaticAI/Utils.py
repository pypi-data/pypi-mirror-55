# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 12:35:38 2019

@author: czzo
"""

import numpy as np

# Classification metrics
from sklearn.metrics import accuracy_score

# Prediction metrics
from sklearn.metrics import r2_score

# Geometrical functions
from scipy.spatial import distance as dc


# Classification algorithm factories
from . import LogisticRegressionAlgorithmFactory as lrcaf
from . import KnnAlgorithmFactory as kaf
from . import RandomForestAlgorithmFactory as rfaf
from . import ExtraTreeClassifierAlgorithmFactory as etcaf
from . import DecisionTreeClassifierAlgorithmFactory as dtcaf
from . import RidgeClassifierAlgorithmFactory as rcaf
from . import PassiveAgressiveClassifierAlgorithmFactory as pacaf
from . import AdaBoostClassifierAlgorithmFactory as abcaf
from . import SVCAlgorithmFactory as svcaf
from . import BaggingClassifierAlgorithmFactory as bcaf
from . import GradientBoostingClassifierAlgorithmFactory as gbcaf
from . import SGDClassifierAlgorithmFactory as sgdcaf
from . import ExtraTreesClassifierAlgorithmFactory as etscaf
#import AlgorithmFactories.ClassificationAlgorithmFactories.XGBoostClassifierAlgorithmFactory as xgbcaf

# Regression algorithm factories
from . import DecisionTreeRegressorAlgorithmFactory as dtrf
from . import LinearRegressionAlgorithmFactory as lraf
from . import RidgeRegressionAlgorithmFactory as rraf
from . import KNNRegressionAlgorithmFactory as knnraf
from . import RandomForestRegressionAlgorithmFactory as rfraf
from . import AdaBoostRegressionAlgorithmFactory as abraf
from . import ExtraTreeRegressionAlgorithmFactory as etraf
from . import ExtraTreesRegressionAlgorithmFactory as etsraf
from . import GradientBoostingRegressionAlgorithmFactory as gbraf
from . import SGDRegressionAlgorithmFactory as sgdraf
from . import KernelRidgeRegressionAlgorithmFactory as krraf
from . import SVRAlgorithmFactory as svraf
from . import LassoRegressionAlgorithmFactory as lraf
from . import ElasticNetAlgorithmFactory as enraf
from . import LarsRegressionAlgorithmFactory as larsraf
from . import LarsLassoRegressionAlgorithmFactory as llraf
from . import OrthogonalMatchingPursuitRegressionAlgorthmFactory as ompraf
from . import PassiveAgressiveRegressionAlgorithmFactory as paraf
from . import BayesianRidgeRegressionAlgorithmFactory as brraf
from . import ARDRegressionAlgorithmFactory as ardraf
#import AlgorithmFactories.RegressionAlgorithmFactories.XGBoostRegressionAlgorithmFactory as xgbraf


classification_algorithms = [lrcaf.get_algorithm(),
                             kaf.get_algorithm(),
                             rfaf.get_algorithm(),
                             etcaf.get_algorithm(),
                             dtcaf.get_algorithm(),
                             rcaf.get_algorithm(),
                             pacaf.get_algorithm(),
                             #abcaf.get_algorithm(),
                             #gbcaf.get_algorithm(),
                             sgdcaf.get_algorithm(),
                             etscaf.get_algorithm(),
                             #xgbcaf.get_algorithm(),
                             ]

regression_algorithms = [dtrf.get_algorithm(),
                         lraf.get_algorithm(),
                         rraf.get_algorithm(),
                         knnraf.get_algorithm(),
                         rfraf.get_algorithm(),
                         #abraf.get_algorithm(),
                         etraf.get_algorithm(),
                         etsraf.get_algorithm(),
                         #gbraf.get_algorithm()
                         sgdraf.get_algorithm(),
                         krraf.get_algorithm(),
                         #svraf.get_algorithm(),
                         lraf.get_algorithm(),
                         enraf.get_algorithm(),
                         larsraf.get_algorithm(),
                         llraf.get_algorithm(),
                         ompraf.get_algorithm(),
                         paraf.get_algorithm(),
                         brraf.get_algorithm(),
                         #ardraf.get_algorithm(),
                         #xgbraf.get_algorithm(),
                         ]


def space_gen(xmin, xmax, len, min_dist, result=[]):
    if len:
        for x in range(xmin, xmax - (len - 1) * min_dist):
            yield from space_gen(x + min_dist, xmax, len - 1, min_dist, result + [x])
    else:
        yield result


def calculate_min_distance(list_of_vectors, vector):
    minimum = 99999
    if len(list_of_vectors) > 0:
        distances = dc.cdist(list_of_vectors,[vector])
        minimum = np.min(distances)

    return minimum


def generate_initial_parameters(particle_count, bounds, distance_between_initial_particles = 0.7):
    initial=[]  
    
    for i in range(particle_count):
        hyper_parameter_list = []
        minimum_distance = 0
        while minimum_distance < distance_between_initial_particles:
           hyper_parameter_list = []
           for j in range(len(bounds)):
               min_bound = bounds[j][0]
               max_bound = bounds[j][1]
               initial_parameter_value = np.random.uniform(min_bound, max_bound)
               hyper_parameter_list.append(initial_parameter_value)
           minimum_distance = calculate_min_distance(initial, hyper_parameter_list)
        initial.append(hyper_parameter_list)
    
    return initial


def generate_initial_best_positions(algorithms):
    pos = []
    
    current_algorithm_name = ""
    
    for algorithm in algorithms:
        if algorithm.algorithm_name != current_algorithm_name:
            current_algorithm_name = algorithm.algorithm_name
            algorithm_best_positions = []
            for i in range(len(algorithm.bounds)):
                algorithm_best_positions.append(0.0)
            pos.append(algorithm_best_positions)
    
    return pos


def train_algorithm(curr_params, param, Xtrain, Xvalid, Ytrain, Yvalid, algorithm, metric=accuracy_score):
    params_copy = param.copy()
    params_copy.update(curr_params)
    model = algorithm(**params_copy)
    model.fit(Xtrain, Ytrain)
    preds = model.predict(Xvalid)
    metric_val = metric(Yvalid, preds)
    
    return model, metric_val


def train_regression_algorithm(curr_params, param, Xtrain, Xvalid, Ytrain, Yvalid, algorithm, metric=r2_score):
    return train_algorithm(curr_params, param, Xtrain, Xvalid, Ytrain, Yvalid, algorithm, metric=metric)


def get_classification_algorithm_mapping():
    algorithm_mapping = {}
    index = 0
    for algorithm in classification_algorithms:
        key = algorithm.algorithm_name
        algorithm_mapping[key] = index
        index += 1
    
    return algorithm_mapping 


def get_regression_algorithm_mapping():
    algorithm_mapping = {}
    index = 0
    for algorithm in regression_algorithms:
        key = algorithm.algorithm_name
        algorithm_mapping[key] = index
        index += 1
    
    return algorithm_mapping


def create_all_supported_algorithm_list(particle_count):
    algorithm_type_list = []
    
    for algorithm in classification_algorithms:
        for i in range(particle_count):
            algorithm_type_list.append(algorithm)
            
    return algorithm_type_list
    

def create_all_supported_regresion_algorithm_list(particle_count):
    algorithm_type_list = []
    
    for algorithm in regression_algorithms:
        total = particle_count
        if algorithm.algorithm_name == lraf.get_algorithm().algorithm_name:
            total = 3
        for i in range(total):
            algorithm_type_list.append(algorithm)
            
    return algorithm_type_list


def generate_initial_particle_positions(num_particles=10, distance_between_initial_particles=0.7):
    initial = []
    for algorithm in classification_algorithms:
        initial_of_algorithm = generate_initial_parameters(num_particles, algorithm.bounds, distance_between_initial_particles)
        initial.extend(initial_of_algorithm)
    
    return initial


def generate_initial_particle_positions_for_regression(num_particles=10, distance_between_initial_particles=0.7):
    initial = []
    for algorithm in regression_algorithms:
        if algorithm.algorithm_name == lraf.get_algorithm().algorithm_name:
            initial_of_algorithm = generate_initial_parameters(3, algorithm.bounds, distance_between_initial_particles)
        else:
            initial_of_algorithm = generate_initial_parameters(num_particles, algorithm.bounds, distance_between_initial_particles) 
        initial.extend(initial_of_algorithm)
    
    return initial
