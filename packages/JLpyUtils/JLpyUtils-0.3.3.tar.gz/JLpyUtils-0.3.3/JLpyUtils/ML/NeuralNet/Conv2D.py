"""
functions related to a keras implementation of a generic 2D convolutional neural network
"""

import numpy as _np

import tensorflow as _tf
import tensorflow.keras as _keras
import tensorflow.keras.layers as _layers


from . import utils as _utils

_pooling_layer = _tf.keras.layers.MaxPool2D
_loss= _tf.keras.losses.categorical_crossentropy
_optimizer = _tf.keras.optimizers.Adam


def model(img_shape = (256, 256, 3),
              batch_size = None ,
              n_outputs_per_img = 2,
              layers_per_group =  1,
              initial_filter_size = 16,
              max_filter_size = 512,
              filter_scaling_factor = 2,
              dense_scaling_factor = 20,
              kernel_size = (2,2),
              activation = 'relu',
              pooling_layer = _pooling_layer,
              pool_size = (2,2),
              batch_norm_rate = None,
              dropout_layer_rate = None,
              dropout_rate = 0.5,
              loss= _loss,
              learning_rate = 0.001,
              optimizer= _optimizer,
              metrics=['accuracy'],
              verbose = 0):
    """
    Build a keras-based 2D Conv. Net computational graph (model) which can be fit to a given dataset
    
    Arguments:
    ---------
        hyperparams_dict: Dictionary containing hyperparameters used to define neural net structure. 
            layers_per_group: how many Conv2D layers stacked back to back before each pooling operation
            initial_filter_size: size of first filter for first conv layer (i.e. the image has 3 colors channels & if 0th filter size is 64, this will be expanded to 64 channels)
            max_filter_size: upper limit on Conv2D filter size. After this limit is reach, the Conv2D layer will be flattened for input into the dense net  
            filter_scaling_factor: int. the multiplicative factor the filter size will be increased by for each group of conv2D layers (higher value will make the network shrink faster)
            dense_scaling_factor: the multiplicative factor the dense net units (following the conv net groups) will be decreased by for each group of Dense layers
            kernel_size: kernel size for Conv2D layers
            activation: activation function to be used
            pooling_layer: the type of pooling layer to be used (must be keras.layer method)
            batch_norm_rate: The rate at which a batch norm layer will be inserted. i.e. for a value of 2, a batch norm layer will be inserted on every other group of layers
            dropout_layer_rate: similar to batch_norm_rate, this defines the how often a dropout layer is inserted into a given group of layers
            dropout_rate: the number of nodes to be dropped in a given dropout layer
    
    Returns:
    --------
        model: tensorflow-keras model object
    """

    _keras.backend.clear_session()
    
    model_dict = {}

    model_dict['inputs'] = _layers.Input(shape= img_shape, 
                                        batch_size= batch_size,
                                        dtype = _tf.float32,
                                        name = 'inputs')

    flat_length = _np.inf
    g = 0 #group index
    idx_dict = {'batch_norm_rate':0,
                'dropout_layer_rate':0}

    #define function to apply batch norm and dropouts at appropriate group iteratation
    BatchNorm_Dropout_dict = {'batch_norm_rate':batch_norm_rate,
                              'dropout_layer_rate': dropout_layer_rate,
                              'dropout_rate':dropout_rate}

    #build groups of conv2d, batch norm, dropout, and pooling layers
    filters = initial_filter_size
    xy_shape = _np.inf
    while filters <= max_filter_size and xy_shape != 1:
        for gl in range(layers_per_group):  #group layer index
            name = 'G'+str(g)+'_L'+str(gl)+'_Conv2D'
            model_dict[name] = _layers.Conv2D(filters = filters, 
                                               kernel_size = kernel_size, 
                                               padding='same', 
                                               activation=activation, 
                                               kernel_initializer='glorot_uniform', 
                                               bias_initializer='zeros',
                                               name = name
                                              )(model_dict[list(model_dict.keys())[-1]])
            if verbose >= 3: print(name, model_dict[name])

        gl+=1
        
        #add batch norm and/or dropout layers
        model_dict, BatchNorm_Dropout_dict, idx_dict, g, gl = _utils.Apply_BatchNorm_Dropouts(model_dict, BatchNorm_Dropout_dict, idx_dict, g, gl)

        name = 'G'+str(g)+'_L'+str(gl)+'_Pool'
        model_dict[name] = pooling_layer(pool_size = pool_size,
                                                             name = name
                                                            )(model_dict[list(model_dict.keys())[-1]])

        if verbose >= 3: print(name, model_dict[name])
        gl+=1

        xy_shape = (model_dict[list(model_dict.keys())[-1]]).shape[1]
        if verbose >= 3: print('xy_shape:',xy_shape)

        filters = int(filters * filter_scaling_factor)

        flat_length = _layers.Flatten()(model_dict[list(model_dict.keys())[-1]]).shape[1]
        if verbose >= 3: print('flat_length:',flat_length)

        g+=1

    #flatten the conv groups output
    gl=0
    name = 'G'+str(g)+'_L'+str(gl)+'_Flatten'
    model_dict[name] = _layers.Flatten(name = name)(model_dict[list(model_dict.keys())[-1]])
    g+=1; gl+=1

    #build dense net layers
    units = int(int(flat_length)/dense_scaling_factor)

    while units > n_outputs_per_img:
        gl=0
        for gl in range(layers_per_group):  #group layer index
            name = 'G'+str(g)+'_L'+str(gl)+'_Dense'
            model_dict[name]= _layers.Dense(units, 
                                           activation=activation, 
                                           kernel_initializer='glorot_uniform', 
                                           bias_initializer='zeros',
                                           name = name
                                          )(model_dict[list(model_dict.keys())[-1]])
            gl+=1 
            model_dict, BatchNorm_Dropout_dict, idx_dict, g, gl = _utils.Apply_BatchNorm_Dropouts(model_dict, BatchNorm_Dropout_dict, idx_dict, g, gl)

        units = units/dense_scaling_factor
        g+=1

    gl=0
    name = 'outputs'
    model_dict[name] = _layers.Dense(n_outputs_per_img,
                                           activation = 'softmax',
                                           kernel_initializer='glorot_uniform', 
                                           bias_initializer='zeros',
                                          name = name
                                          )(model_dict[list(model_dict.keys())[-1]])
    model = _keras.Model(inputs = model_dict['inputs'],
                                            outputs = model_dict['outputs'])
    model.compile(loss=loss,
                  optimizer=optimizer(lr=learning_rate),
                  metrics=metrics)
    return model
    
def model_dict(img_shape,
                  batch_size  ,
                  n_outputs_per_img,
                  layers_per_group,
                  initial_filter_size,
                  max_filter_size,
                  filter_scaling_factor,
                  dense_scaling_factor,
                  kernel_size,
                  activation ,
                  pooling_layer,
                  pool_size ,
                  batch_norm_rate,
                  dropout_layer_rate,
                  dropout_rate ,
                  loss,
                  learning_rate,
                  optimizer,
                  metrics,
                  verbose):
    
    
    assert(type(n_features)==int), 'n_features must be of type int'
    assert(type(n_labels)==int), 'n_labels must be of type int'
    
    model_dict = {}
    model_dict['model'] = model
    
    model_dict['param_grid'] = {'img_shape': [img_shape],
                                   'batch_size' : [batch_size],
                                   'n_outputs_per_img': [n_outputs_per_img],
                                   'layers_per_group': [1,2],
                                   'initial_filter_size': [16, 32, 64],
                                   'max_filter_size': [128, 256, 512, 1024],
                                   'filter_scaling_factor': [2, 3, 4],
                                   'dense_scaling_factor': [10,20,100, 1000],
                                   'kernel_size': [(2,2),(3,3),(4,4)],
                                   'activation': ['relu', 'elu'], 
                                   'pooling_layer': [_layers.MaxPool2D, _layers.AvgPool2D],
                                   'pool_size': [(2,2), (3,3), (4,4)],
                                   'batch_norm_rate': [None, 1, 2, 3],
                                   'dropout_layer_rate': [None, 1, 2, 3],
                                   'dropout_rate': [0.9,0.5,0.1],
                                   'loss': [loss],
                                   'learning_rate': [0.01, 0.001, 0.0001],
                                   'optimizer':[optimizer],
                                   'metrics': [metrics]}
    return model_dict
