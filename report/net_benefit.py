# exec( open(rootdir + 'net_benefit.py').read() )

# modes:
plot_xgb=0



chosen={}
chosen['stroke']='ModifiedCHADS2'
chosen['death']='MPH-CCI'
chosen['bleed']='HAS-BLED'

if metid=='nnet' or (metid=='br3f'):
    comparison_names = ['Cox', 'xNN-survival', 'XGB', chosen[ev]]
else:
    if metid=='mlp':
        comparison_names = ['Cox', 'NNsurv', 'XGB', chosen[ev]]
    else:
        comparison_names = ['Cox', metid, 'XGB', chosen[ev]]

SR=1; WW=8; HH=4;
plt.close('all')

colors = ['', 'orange', 'green', 'grey', 'pink'] 
markers =['','.', 's', 'o', '+']        

if plot_xgb:
    BB=[1,2,3,4]
else:
    BB=[1,2,4]


for YR in [1,2,3]:
    plt.figure( figsize=(WW,HH), dpi=300 )        
    
    for aa in [1,2,3]:           
        ax=plt.subplot( 1,3, aa )             
        if aa==1:
            ii=2; t='tst'; ttt='Test Set'
        elif aa==2:
            ii=3; t='ext'; ttt='Validation Set A'
        else:
            ii=4; t='ext2'; ttt='Validation Set B'
    
        t1=time2event[sets[ii][::SR]] 
        e1=event_happened[sets[ii][::SR]]         
        
        for bbb in BB:                            

            if bbb==1:
                cox_y_pred=cph2.predict_survival_function( Xdata[t][:,fff] )
                                
                #times0=y_pred.index.values.astype('float64')
                #y_pred=y_pred.to_numpy().transpose()                                               
            
            allpos=[]
            nb=[]
            nb2=[]
            
            if ev=='death':
                th = np.arange(0.001,1,.05)
            else:
                th = np.arange(0.001,.1,.01)
            
            for i, pt in enumerate(th): 
                
                if bbb==1:  # trained in day, Cox model      
                    pred_surv = np.asarray( [[ fn(t) for t in [YR*365] ] for fn in cox_y_pred ]).squeeze()
                    risk = 1-pred_surv
                    
                elif bbb==11: #lifelines   
                    Factor=1                    
                    qq=np.where( times0 == YR )[0]                                         
                    pred_surv = np.array(y_pred[:,qq]).squeeze(); 
                    risk = 1- pred_surv
                    
                elif bbb==3:                        
                    ru =xgbmodel.predict( xgboost.DMatrix( Xdata['trn'], label= code_data( sets[0] ) ) )                       
                    u = xgbmodel.predict( xgboost.DMatrix( Xdata[t], label= code_data( sets[ii] ) ) )                                          
                    risk = ru.max() - u 
                    risk = risk/risk.max()
                elif bbb==4:
                    if ev=='bleed':                    
                        r=myutils.readpkl('R:/working/ltang/submission_figures/risk_scores/HASBLED_%s_scores_CI0.83.pkl.pkl'%setnames[ii] )
                    elif ev=='death':
                        r=myutils.readpkl('R:/working/ltang/submission_figures/risk_scores/MCHP-CCI_%s_scores_CI0.83.pkl.pkl'%setnames[ii] )
                    else:                    
                        r=myutils.readpkl('R:/working/ltang/submission_figures/risk_scores/ModifiedCHADS2_%s_scores_CI0.83.pkl.pkl'%setnames[ii] )                
                    try:
                        r=r['risk']
                    except:
                        r= r['risk_multidimension'][:,YR]                                                       
                    r= r.max() - r
                    risk = r/r.max()
                else:              
                    if mode=='day':
                        Factor=365
                    else:
                        Factor=1
                    if isNN:
                        ru = np.cumprod( YP[0][:, 0:np.nonzero(breaks>(Factor*YR))[0][0]] , 1 )[:,-1 ]              
                        u = np.cumprod( YP[ii][:, 0:np.nonzero(breaks>(Factor*YR))[0][0]] , 1 )[:,-1 ]              
                        risk = ru.max() -u 
                        risk = 1- u /u.max()       
                        
                        
                    elif metid=='coxnet':
                        risk = 1- cox_yreds[t][:,YR-1]
                        Factor=1
                    elif metid=='xgb':
                        if mode=='day':
                            Factor=365
                        else:
                            Factor=1
                        risk = YP[ii].max() - YP[ii]     
                        
                    elif 'rsf' in metid:
                        if mode=='day':
                            Factor=365
                        else:
                            Factor=1
                        risk = 1 - YP[ii][:,YR-1]                             
                        
                n = len(risk)        
                if t1.max()>10:
                    r1 = ((e1==1) & (t1<(YR*365)) ); 
                else:
                    r1 = ((e1==1) & (t1<(YR)) ); 
                    
                r0 = (r1==0)
                tp = np.sum( (risk >= pt ) & r1 )
                fp = np.sum( (risk >= pt ) & r0 )
                fn = np.sum( (risk < pt ) & r1 )
                tn = np.sum( (risk < pt ) & r0 )                                
                
                nb.append( (tp/n) - (fp/n)*( pt/(1-pt) ) )                        
                    
                risk2 = np.ones(len(r1))
                tp = np.sum( (risk2 >= pt ) & r1 )
                fp = np.sum( (risk2 >= pt ) & r0 )
                fn = np.sum( (risk2 < pt ) & r1 )
                tn = np.sum( (risk2 < pt ) & r0 )            
                allpos.append( (tp/n) - (fp/n)*( pt/(1-pt) ) )              
                
            if bbb==1:
                plt.plot( th, np.asarray( allpos), 'k--', label='Treat all', linewidth=2 )
                plt.plot( [0, 1], [0, 0], 'r--', label= 'Treat none', linewidth=1 )
                    
            
            plt.plot( th, np.asarray( nb ),  markers[bbb]+'-', markersize=1, color=colors[bbb], label=comparison_names[bbb-1] )
            #plt.plot( th, np.asarray( nb2 ), 'c', label='NNet Survival' )
            
            
            if (ev=='stroke') & (aa==1):            
                plt.legend( prop={'size': 6}, loc='best',handletextpad=.01)              
                plt.ylabel( 'Clinical net benefit')
                
            plt.xlabel('Threshold on risk')    
    
        ax.set_title(ttt);
                     
        ax.grid(which="major", alpha=.6)
        ax.grid(which="minor", alpha=.3)
        ax.tick_params( axis='y', labelsize=6)
        if ev=='stroke':
            plt.ylim( [-.05,.05])        
            plt.xlim( [0,.1])
        elif ev=='bleed':
            plt.ylim( [-.05,.05])
            plt.xlim( [0,.08])
        else: 
            plt.ylim( [-.1,.3])
            plt.xlim( [0,1])        
        plt.minorticks_on()                                     


    plt.suptitle( 'Decision curve analysis for %d-year %s risk prediction'% (YR, ev) )
    plt.tight_layout()
    
    if 0:    
      plt.savefig( prefix + '_net-ben_%dYR.png'% YR )    
      plt.savefig( prefix + '_net-ben_%dYR.tif'% YR, dpi=600, format='tiff',pil_kwargs={'compression':'tiff_lzw'}  )
      plt.savefig( prefix + '_net-ben_%dYR.pdf'% YR )
