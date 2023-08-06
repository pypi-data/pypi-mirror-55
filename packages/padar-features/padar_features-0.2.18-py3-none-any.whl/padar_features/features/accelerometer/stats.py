"""

Computing features of descriptive statistics

Author: Qu Tang

Date: Jul 10, 2018

"""
import numpy as np
from ...libs.data_formatting import validator
from ...libs.data_formatting import formatter
from scipy import stats as sp_stats


def mean(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(np.nanmean(X, axis=0))
    result = formatter.add_name(result, mean.__name__)
    return result


def std(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(np.nanstd(X, axis=0))
    result = formatter.add_name(result, std.__name__)
    return result


def positive_amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(np.nanmax(X, axis=0))
    result = formatter.add_name(result, positive_amplitude.__name__)
    return result


def negative_amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(np.nanmin(X, axis=0))
    result = formatter.add_name(result, negative_amplitude.__name__)
    return result


def amplitude_range(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(positive_amplitude(
        X).values - negative_amplitude(X).values)
    result = formatter.add_name(result, amplitude_range.__name__)
    return result


def amplitude(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(np.nanmax(np.abs(X), axis=0))
    result = formatter.add_name(result, amplitude.__name__)
    return result


def skew(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(sp_stats.skew(np.X, axis=0))
    result = formatter.add_name(result, skew.__name__)
    return result


def kurtosis(X):
    _check_input(X)
    X = formatter.as_float64(X)
    result = formatter.vec2rowarr(sp_stats.kurtosis(np.X, axis=0))
    result = formatter.add_name(result, kurtosis.__name__)
    return result


def correlation(X):
    _check_input(X)
    X = formatter.as_float64(X)
    corr_mat = np.corrcoef(X, rowvar=False)
    inds = np.tril_indices(n=3, k=-1, m=3)
    result = corr_mat[inds[:]]
    result = formatter.vec2rowarr(result)
    result = formatter.add_name(result, correlation.__name__)
    return result


def mean_distance(X):
    '''
    Compute mean distance, the mean of the absolute difference between value
     and mean. Also known as 1st order central moment.

     TODO: Questionable?
    '''
    _check_input(X)
    X = formatter.as_float64(X)
    result = mean(np.abs(X - np.repeat(mean(X), X.shape[0], axis=0)), axis=0)
    result = formatter.add_name(result, mean_distance.__name__)
    return result


def _check_input(X):
    if not validator.is_xyz_inertial(X) and not validator.is_vm_inertial(X):
        raise ValueError(
            'Input numpy array must be a 3 axis sensor or in vector magnitude')
