
import myutils

from sklearn.model_selection import train_test_split
import sksurv     
from sksurv.ensemble import RandomSurvivalForest

model = RandomSurvivalForest( n_estimators=1000, min_samples_split = .1, min_samples_leaf= .1, max_features="sqrt", n_jobs=-1,
                              random_state=SEED )                        

yy_s = U.get_structured( event_happened, time2event,s1,s2,s3,s4, s1b )                   

run_times=[]
run_times.append( tm.time() )

t='trn'
model.fit( Xdata[t], yy_s[t] )       # 5.32pm
run_times.append( tm.time() )      
train_time =  np.diff( run_times)/60 # 5.33pm                       
print('Took', train_time , 'minutes to train RSF-sk' )           


import eli5
from eli5.sklearn import PermutationImportance                 
perm = PermutationImportance( model, n_iter = 5, random_state=SEED ); SR=80; feat_times=[]; feat_times.append( tm.time() ); 
perm.fit( Xdata[t][::SR,:], yy_s[t][::SR] ); feat_times.append( tm.time() );feat_times =  np.diff( feat_times )/60  


qq = np.where( perm.feature_importances_ > 0)[0]
print( 'variables with feature importance > 0:',np.asarray(variables)[qq] )

plt.clf()        
f=perm.feature_importances_; 

q=np.argsort( -f )        
xx=np.arange( X.shape[1]); plt.bar( xx, f[q] )        

f=perm.feature_importances_; q=np.argsort( -f )        
V=[] 
for i in range(len(variables)):
    v = np.asarray(variables)[q][i] 
    V.append(v)      
    if i<np.int(len(variables)*.20):
        print( i, v )           
ff=f[q]
myutils.write2pkl( '%s_stats' % prefix, {'train_time':train_time,'feat_times':feat_times,'V':V,'importance':ff})     
