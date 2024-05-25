import os
import warnings

import matplotlib.pyplot as plt

import numpy as np
import scipy.signal

import statsmodels
import statsmodels.tsa
import statsmodels.tsa.stattools
import statsmodels.tools
#import statsmodels.tools.sm_exceptions
from statsmodels.tools.sm_exceptions import InterpolationWarning

import emd
import copent

import aluminium_prediction.stationarity



def cross_correlation(p, q, stationarize=False):
    """
    source: https://www.datainsightonline.com/post/cross-correlation-with-two-time-series-in-python#google_vignette
    """
    if stationarize is True:
        p = aluminium_prediction.stationarity.remove_residual_emd(p, n=1)
        q = aluminium_prediction.stationarity.remove_residual_emd(q, n=1)
    p = (p - np.mean(p)) / (np.std(p) * len(p))
    q = (q - np.mean(q)) / (np.std(q))  
    lags = scipy.signal.correlation_lags(len(p), len(q))
    return lags, np.correlate(p, q, 'full')


def cross_correlation_plot(lags, ccf_values, title='', show=True, fig=None, ax=None):
    """
    source: https://www.datainsightonline.com/post/cross-correlation-with-two-time-series-in-python#google_vignette
    """
    if (fig is None) or (ax is None):
        fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(lags, ccf_values)
    ax.axhline(-2/np.sqrt(23), color='red', label='5% confidence interval')
    ax.axhline(2/np.sqrt(23), color='red')
    ax.axvline(x = 0, color = 'black', lw = 1)
    ax.axhline(y = 0, color = 'black', lw = 1)
    ax.axhline(y = np.max(ccf_values), color = 'blue', lw = 1, linestyle='--', label = 'highest +/- correlation')
    ax.axhline(y = np.min(ccf_values), color = 'blue', lw = 1, linestyle='--')
    ax.set(ylim = [-1, 1])
    ax.set_title(title, weight='bold', fontsize = 15)
    ax.set_ylabel('Correlation Coefficients', weight='bold', fontsize = 12)
    ax.set_xlabel('Time Lags', weight='bold', fontsize = 12)
    plt.legend()
    if show is True:
        plt.show()
    else:
        return fig, ax


def transfer_entropy(p, q, nlags=30, stationarize=False):
    """_summary_

    Args:
        p (_type_): _description_
        q (_type_): _description_
        nlags (int, optional): _description_. Defaults to 30.
        stationarize (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_

    source: https://www.kaggle.com/code/singh2299/transfer-entropy-causal
    
    """
    if stationarize is True:
        p = aluminium_prediction.stationarity.remove_residual_emd(p, n=1)
        q = aluminium_prediction.stationarity.remove_residual_emd(q, n=1)

    lags = np.arange(1,nlags+1)
    te = np.zeros(nlags)

    for lag in lags:
        te[lag-1] = copent.transent(p,q,lag)
    
    return lags, te