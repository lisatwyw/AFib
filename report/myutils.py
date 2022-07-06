def write2pkl(file, dic) :
    from pickle import dump
    f=open( file + '.pkl', 'wb' )
    dump(dic,f)
    f.close() 
    
def readpkl( file ):
    from pickle import load
    file=open(file,'rb')
    dat = load(file )
    return dat
 

import numpy
from scipy.integrate import trapz
from sklearn.utils import check_consistent_length, check_array

from sksurv.exceptions import NoComparablePairException
from sksurv.nonparametric import CensoringDistributionEstimator, SurvivalFunctionEstimator
from sksurv.util import check_y_survival

def _check_estimate(estimate, test_time):
    estimate = check_array(estimate, ensure_2d=False)
    if estimate.ndim != 1:
        raise ValueError(
            'Expected 1D array, got {:d}D array instead:\narray={}.\n'.format(
                estimate.ndim, estimate))
    check_consistent_length(test_time, estimate)
    return estimate


def _check_inputs(event_indicator, event_time, estimate):
    check_consistent_length(event_indicator, event_time, estimate)
    event_indicator = check_array(event_indicator, ensure_2d=False)
    event_time = check_array(event_time, ensure_2d=False)
    estimate = _check_estimate(estimate, event_time)

    if not numpy.issubdtype(event_indicator.dtype, numpy.bool_):
        raise ValueError(
            'only boolean arrays are supported as class labels for survival analysis, got {0}'.format(
                event_indicator.dtype))

    if len(event_time) < 2:
        raise ValueError("Need a minimum of two samples")

    if not event_indicator.any():
        raise ValueError("All samples are censored")

    return event_indicator, event_time, estimate


def _check_times(test_time, times):
    times = check_array(numpy.atleast_1d(times), ensure_2d=False, dtype=test_time.dtype)
    times = numpy.unique(times)

    if times.max() >= test_time.max() or times.min() < test_time.min():
        raise ValueError(
            'all times must be within follow-up time of test data: [{}; {}['.format(
                test_time.min(), test_time.max()))

    return times

  
def cumulative_dynamic_auc(survival_train, survival_test, estimate, times, verbose= False, tied_tol=1e-8, ci=.95, debug=False ):
    
    test_event, test_time = check_y_survival(survival_test)
    estimate = _check_estimate(estimate, test_time)
    times = _check_times(test_time, times)

    # sort by risk score (descending)
    o = numpy.argsort(-estimate)
    test_time = test_time[o]
    test_event = test_event[o]
    estimate = estimate[o]
    survival_test = survival_test[o]

    cens = CensoringDistributionEstimator()
    cens.fit(survival_train)
    ipcw = cens.predict_ipcw(survival_test)      
    
    import scipy.stats as st
    
    if ci==.95:
        delta = (1-ci )/2
        upper = st.norm.ppf( .975 )
        lower = st.norm.ppf( .025 )
    else:
        delta = (1-ci)/2
        upper = st.norm.ppf( ci+delta)
        lower = st.norm.ppf( delta )
        
        if debug:
            print(ci, 'c.i.: ', delta , ci+delta )
    
    se_auc = []
    SENS = []
    FPR = []
    n_samples = test_time.shape[0]
    scores = numpy.empty(times.shape[0], dtype=float)
    for k, t in enumerate(times):
        is_case = (test_time <= t) & test_event
        is_control = test_time > t
        n_controls = is_control.sum()
        n_cases = is_case.sum()
        
        if verbose:
            print(n_controls, 'controls', n_cases, 'cases' )
        
        true_pos = []
        false_pos = []
        tp_value = 0.0
        fp_value = 0.0
        est_prev = numpy.infty

        for i in range(n_samples):
            est = estimate[i]
            if numpy.absolute(est - est_prev) > tied_tol:
                true_pos.append(tp_value)
                false_pos.append(fp_value)
                est_prev = est
            if is_case[i]:
                tp_value += ipcw[i]
            elif is_control[i]:
                fp_value += 1
        true_pos.append(tp_value)
        false_pos.append(fp_value)

        sens = numpy.array(true_pos) / ipcw[is_case].sum()
        fpr = numpy.array(false_pos) / n_controls
        auc = scores[k] = trapz(sens, fpr)
        
        
        FPR.append( fpr )
        SENS.append( sens )
        
        
        Q1 = (auc)/(2-auc )
        Q2 = 2*(auc**2)/(1+auc)
        
        n1 = n_cases + 1e-10
        n2 = n_controls + 1e-10       
        if 0:
            n1 = (n1 + n2) /2
            n2 = n1
        se = numpy.sqrt(  ( auc *(1-auc) + (n1 - 1)*(Q1 - auc**2) +  (n2 - 1)*(Q2 - auc**2) )/ n1/ n2 )
        se_auc.append( (auc+lower*se, auc, auc+ upper*se) )
        
    
    if times.shape[0] == 1:
        mean_auc = scores[0]
        if verbose:
            print( 'Single timepoint', scores )                
    else:
        surv = SurvivalFunctionEstimator()
        surv.fit(survival_test)
        s_times = surv.predict_proba(times)
        # compute integral of AUC over survival function
        d = -numpy.diff(numpy.concatenate(([1.0], s_times)))
        integral = (scores * d).sum()
        mean_auc = integral / (1.0 - s_times[-1])
        if verbose:        
            print( 'multiple timepoint', mean_auc )
    
    return scores, mean_auc, se_auc, SENS, FPR, ipcw 

  
