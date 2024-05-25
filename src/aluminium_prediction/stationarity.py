import os
import warnings

import numpy as np
import pandas as pd

import scipy.signal

import statsmodels
import statsmodels.tsa
import statsmodels.tsa.stattools
import statsmodels.tools
#import statsmodels.tools.sm_exceptions
from statsmodels.tools.sm_exceptions import InterpolationWarning

import emd


def adf_test(timeseries, pvalue=0.05, truefalse=True):
  """
  See https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html.
  """
  # TODO: Add filtering of InterpolationWarning
  test_result = statsmodels.tsa.stattools.adfuller(timeseries, autolag='AIC')
  test_pvalue = test_result[1]

  if truefalse is True:
    return test_pvalue < pvalue
  else:
    return test_pvalue

def kpss_test(timeseries, pvalue=0.05, truefalse=True):
  with warnings.catch_warnings(record=True) as w:
    warnings.filterwarnings(action='always',
                            category=InterpolationWarning)
    test_result = statsmodels.tsa.stattools.kpss(timeseries, regression="c", nlags="auto")
    test_pvalue = test_result[1]
    if   (len(w) == 1) and ('p-value is greater' in str(w[-1].message)):
       print(str(w[-1].message))
    elif (len(w) == 1) and ('p-value is smaller' in str(w[-1].message)):
       pass
    else:
       print('KPSS Warning')
       print(w)

  if truefalse is True:
    return test_pvalue > pvalue
  else:
    return test_pvalue

def stationarity_test(timeseries, pvalue=0.05, verbose=1):
  adf_result = adf_test(timeseries, pvalue=pvalue, truefalse=True)
  kpss_result = kpss_test(timeseries, pvalue=pvalue, truefalse=True)

  if verbose > 0:
    print('Stationarity (ADF test): ', adf_result)
    print('Stationarity (KPSS test):', kpss_result)

  return adf_result and kpss_result

def remove_residual_emd(signal, n=1):
  imf_opts = {'sd_thresh': 0.05}
  imfs = emd.sift.sift(signal,imf_opts=imf_opts)
  if n > imfs.shape[1]:
    n = imfs.shape[1]
    
  return signal - imfs[:,-n:].sum(axis=1)