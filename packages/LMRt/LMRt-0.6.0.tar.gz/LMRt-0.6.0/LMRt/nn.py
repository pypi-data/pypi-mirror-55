''' the module for neural network
'''
import numpy as np
import pandas as pd
import pickle
import os
import statsmodels.api as sm

from . import utils


def norm(values, time=None, ref_period=None):
    ''' normalize a timeseries w.r.t the ref_period
    '''
    if time is None or ref_period is None:
        values -= np.mean(values)
        values /= np.std(values)
    else:
        mask = (time >= ref_period[0]) & (time <= ref_period[1])
        values -= np.mean(values[mask])
        values /= np.std(values[mask])
    return values


def prep_data(time_endog, endog, time_exog, exog, lookback=0,
              endog_col='endog', exog_col='exog',
              normalize=True, ref_period=None,
              merge_exogs=True, jump=1, mode='annual'):
    ''' prepare data for LSTM

    Args:
        time_endog (array): time axis of the endogenous timeseries, assuming evenly-spaced
        endog (array): endogenous timeseries (i.e., dependent variable), assuming evenly-spaced
        time_exog (array): time axis of the exogenous timeseries, assuming evenly-spaced
        exog (array): exogenous timeseries (i.e., independent variable), assuming evenly-spaced
        lookback (int): the number of timesteps to lookback
        jump (int): keep every `jump` rows

    Returns:
        df_out (DataFrame): the DataFrame with lagged exog values
    '''

    # normalization
    if normalize:
        exog = norm(exog, time=time_exog, ref_period=ref_period)
        endog = norm(endog, time=time_endog, ref_period=ref_period)

    # store in a DataFrame
    df = pd.DataFrame({'time': time_exog, f'{exog_col}_lag0': exog})
    for i in range(1, lookback):
        df[f'{exog_col}_lag{i}'] = df[f'{exog_col}_lag0']
        df[f'{exog_col}_lag{i}'] = df[f'{exog_col}_lag{i}'].shift(i)

    df.set_index('time', drop=True, inplace=True)
    df = df.dropna()

    if merge_exogs:
        matrix = df.values[:, ::-1]

        df_out = pd.DataFrame({'time': df.index})
        df_out[exog_col] = np.nan
        df_out[exog_col] = df_out[exog_col].astype(object)
        df_out.set_index('time', drop=True, inplace=True)

        i = 0
        for idx, row in df.iterrows():
            df_out.at[idx, exog_col] = matrix[i, :]
            i += 1

        df_out = df_out[::jump]

        if mode == 'annual':
            idx = df_out.index
            df_out.reset_index(drop=True, inplace=True)
            idx_year = [int(i) for i in idx]
            df_out['time'] = idx_year
            df_out.set_index('time', drop=True, inplace=True)

    else:
        df_out = df

    df_endog = pd.DataFrame({'time': time_endog, endog_col: endog})
    df_out = df_out.merge(df_endog, how='inner', on='time')
    df_out.set_index('time', drop=True, inplace=True)

    return df_out


def split_data(df, X_col='exog', y_col='endog', frac=0.7, calib_range=None, valid_range=None):

    time = df.index
    if calib_range is None or valid_range is None:
        nt = np.size(time)
        df_calib = df[:int(nt*frac)]
        df_valid = df[int(nt*frac):]
    else:
        calib_mask = (time >= calib_range[0]) & (time <= calib_range[1])
        valid_mask = (time >= valid_range[0]) & (time <= valid_range[1])
        df_calib = df[calib_mask]
        df_valid = df[valid_mask]

    # reshape data
    X_calib = np.stack(df_calib[X_col].values)
    X_calib_reshaped = X_calib.reshape(np.shape(X_calib)[0], np.shape(X_calib)[1], 1)
    y_calib = df_calib[y_col].values

    X_valid = np.stack(df_valid[X_col].values)
    X_valid_reshaped = X_valid.reshape(np.shape(X_valid)[0], np.shape(X_valid)[1], 1)
    y_valid = df_valid[y_col].values

    # output
    data_dict = {
        'time': time,
        'time_calib': df_calib.index,
        'time_valid': df_valid.index,
        'X': df[X_col].values,
        'y': df[y_col].values,
        'X_calib': X_calib,
        'X_calib_reshaped': X_calib_reshaped,
        'y_calib': y_calib,
        'X_valid': X_valid,
        'X_valid_reshaped': X_valid_reshaped,
        'y_valid': y_valid,
    }

    return data_dict


def run_LSTM(data_dict, neurons=[5], activations=['relu'], dropouts=[0], epochs=100, verbose=False,
             loss='mse', optimizer='adam', model_save_path=None, history_save_path=None,
             backend='theano', seed=2333):

    os.environ['KERAS_BACKEND'] = backend
    np.random.seed(seed)

    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import LSTM
    from keras.layers import Dropout

    # define model
    model = Sequential()
    nlayer = np.size(neurons)

    for i in range(nlayer-1):
        model.add(LSTM(neurons[i], activation=activations[i], return_sequences=True))
        model.add(Dropout(dropouts[i]))

    model.add(LSTM(neurons[nlayer-1], activation=activations[nlayer-1]))
    model.add(Dropout(dropouts[nlayer-1]))

    model.add(Dense(1))

    # compile model
    model.compile(loss=loss, optimizer=optimizer)

    # fit model
    history = model.fit(
        data_dict['X_calib_reshaped'], data_dict['y_calib'],
        epochs=epochs, shuffle=False, verbose=verbose,
        validation_data=(data_dict['X_valid_reshaped'], data_dict['y_valid']),
    )

    if model_save_path is not None:
        model.save(model_save_path)

    if history_save_path is not None:
        with open(history_save_path, 'wb') as f:
            pickle.dump(history.history, f)

    return model, history.history


def evaluate_model(model, data_dict, name='LSTM',
                   calib_col='Calibration', valid_col='Validation',
                   calib_range=None, valid_range=None):

    if name == 'LSTM':
        predict_calib = model.predict(data_dict['X_calib_reshaped'])[:, 0]
        predict_valid = model.predict(data_dict['X_valid_reshaped'])[:, 0]
    elif name == 'OLS':
        predict_calib = model.predict(exog=sm.add_constant(data_dict['X_calib']))
        predict_valid = model.predict(exog=sm.add_constant(data_dict['X_valid']))
    else:
        raise KeyError('ERROR: the given model name `{name}` is not supported yet!')

    mean_calib = np.mean(predict_calib)
    mean_valid = np.mean(predict_valid)
    var_calib = np.var(predict_calib)
    var_valid = np.var(predict_valid)

    corr_calib, _, p_calib = utils.corr_sig(data_dict['y_calib'], predict_calib)
    corr_valid, _, p_valid = utils.corr_sig(data_dict['y_valid'], predict_valid)

    mean_calib_truth = np.mean(data_dict['y_calib'])
    mean_valid_truth = np.mean(data_dict['y_valid'])
    var_calib_truth = np.var(data_dict['y_calib'])
    var_valid_truth = np.var(data_dict['y_valid'])

    resid_calib = data_dict['y_calib'] - predict_calib
    resid_valid = data_dict['y_valid'] - predict_valid
    mse_calib = np.mean(resid_calib**2)
    mse_valid = np.mean(resid_valid**2)

    yw_calib = sm.regression.yule_walker(resid_calib, order=1)
    yw_valid = sm.regression.yule_walker(resid_valid, order=1)

    metric_list = [
        'mean',
        'var',
        'corr',
        'pvalue',
        'resid_rho',
        'resid_MSE',
    ]

    if calib_range is not None:
        calib_col = f'{calib_col} [{calib_range[0]}, {calib_range[1]}]'

    if valid_range is not None:
        valid_col = f'{valid_col} [{valid_range[0]}, {valid_range[1]}]'

    df_eval = pd.DataFrame({calib_col: None, valid_col: None, 'Metric': metric_list})
    df_eval.set_index('Metric', drop=True, inplace=True)

    df_eval.loc['mean', calib_col] = f'({mean_calib:.2f}, {mean_calib_truth:.2f})'
    df_eval.loc['mean', valid_col] = f'({mean_valid:.2f}, {mean_valid_truth:.2f})'
    df_eval.loc['var', calib_col] = f'({var_calib:.2f}, {var_calib_truth:.2f})'
    df_eval.loc['var', valid_col] = f'({var_valid:.2f}, {var_valid_truth:.2f})'
    df_eval.loc['corr', calib_col] = f'{corr_calib:.2f}'
    df_eval.loc['corr', valid_col] = f'{corr_valid:.2f}'
    df_eval.loc['pvalue', calib_col] = f'{p_calib:.2f}'
    df_eval.loc['pvalue', valid_col] = f'{p_valid:.2f}'
    df_eval.loc['resid_rho', calib_col] = f'{yw_calib[0][0]:.2f}'
    df_eval.loc['resid_rho', valid_col] = f'{yw_valid[0][0]:.2f}'
    df_eval.loc['resid_MSE', calib_col] = f'{mse_calib:.2f}'
    df_eval.loc['resid_MSE', valid_col] = f'{mse_valid:.2f}'

    res_dict = {
        'summary': df_eval,
        'predict_calib': predict_calib,
        'predict_valid': predict_valid,
    }

    return res_dict
