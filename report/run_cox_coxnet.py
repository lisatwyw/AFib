import sksurv 

from eval_metrics import brier_score, integrated_brier_score, concordance_index_censored, concordance_index_ipcw, cumulative_dynamic_auc            
from sksurv.linear_model import CoxnetSurvivalAnalysis, CoxPHSurvivalAnalysis        
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler        
from sklearn.model_selection import KFold, GridSearchCV

import lifelines 
import warnings
from sklearn.exceptions import ConvergenceWarning 
 

def get_structured( event_happened, time2event,s1,s2,s3,s4, s1b):
  yy_s = dict()    
  yy_s['trn'] = sksurv.util.Surv.from_arrays(  event_happened[s1].astype(bool), time2event[s1] )         
  yy_s['tst'] = sksurv.util.Surv.from_arrays(  event_happened[s2].astype(bool), time2event[s2] )         
  yy_s['ext'] = sksurv.util.Surv.from_arrays(  event_happened[s3].astype(bool), time2event[s3] )         
  yy_s['ext2'] = sksurv.util.Surv.from_arrays( event_happened[s4].astype(bool), time2event[s4] )          
  try:
      yy_s['val'] = sksurv.util.Surv.from_arrays( event_happened[s1b].astype(bool), time2event[s1b] )          
  except:
      pass    
  return yy_s

yy_s = get_structured( event_happened, time2event,s1,s2,s3,s4,s1b )

if metid=='coxnet':
  
  coxnet_pipe = make_pipeline(
  StandardScaler(),
  CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, max_iter=100) )

  st='coxnetsurvivalanalysis'        
  coxnet_pipe.fit(Xdata[t], yy_s[t])                                    
  cv = KFold( n_splits = 5, shuffle=True, random_state = SEED)                    
  est_alphas = coxnet_pipe.named_steps[st].alphas_

  gcv=GridSearchCV(  make_pipeline( StandardScaler(), CoxnetSurvivalAnalysis(alpha_min_ratio=.01, max_iter=200)), 
                    param_grid = {st+'__alphas': [ [v] for v in est_alphas], st+'__l1_ratio': [.88, .9, .92, .95]  }, 
                    cv=cv, error_score = .5, refit=True, n_jobs=2).fit( Xdata[t], yy_s[t] )      
  
elif metid=='cox':

  if FD>0:        
      alphas = [10, 100, 1000, 10000]; 
      #alphas = 10.**np.linspace(-4, 4, 25)
      I = [0, 6, 12, 18, 24] 
  else:
      I = np.arange( len(alphas) )

  coefficients = {}                        

  t='trn'            
  if 1:
      for ii,alpha in enumerate( alphas ):           
          cph = CoxPHSurvivalAnalysis( alpha,ties='efron' )
          cph.fit( Xdata[t], yy_s[t]) 
          k = round(alpha, 5)
          coefficients[k] = cph.coef_                                              
      print('\n\n\nDone',ii, 'alphas')       

  model = CoxPHSurvivalAnalysis( alpha=10, ties='efron' )
  model.fit( Xdata[t], yy_s[t]) 

  myutils.write2pkl( '%s_model' % prefix, {'model': model } )                         
  tester = myutils.readpkl( '%s_model.pkl' % prefix )                         

  coefficients = model.coef_
  C = pd.DataFrame( coefficients).rename_axis(index="feature", columns=["variable"]).set_index( pd.Series(variables) )

  def plot_coefficients(coefs, n_highlight):
      _, ax = plt.subplots(figsize=(9, 6))
      n_features = coefs.shape[0]
      alphas = coefs.columns
      for row in coefs.itertuples():
          ax.semilogx(alphas, row[1:], ".-", label=row.Index)

      alpha_min = alphas.min()
      top_coefs = coefs.loc[:, alpha_min].map(abs).sort_values().tail(n_highlight)
      for name in top_coefs.index:
          print( name )
          coef = coefs.loc[name, alpha_min]
          plt.text( alpha_min, coef, name + "   ",                        
              verticalalignment="center"
          )                
      ax.yaxis.set_label_position("right")
      ax.yaxis.tick_right()
      ax.grid(True)
      ax.set_xlabel("alpha")
      ax.set_ylabel("coefficient")

  plot_coefficients(C, n_highlight=len(C) )            
  plt.title( '%s\n\nEffects of alpha (in L2)'%prefix )        
  plt.tight_layout()                   
  plt.savefig( '%s_cphf.png' %( prefix ) )  
