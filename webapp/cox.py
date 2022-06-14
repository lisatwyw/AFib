from flask import Flask, render_template, request, redirect, url_for
import joblib
import pickle
import numpy as np
import numpy

from utils import StepFunction

app = Flask(__name__)

@app.route("/")

def root():
    return render_template("index.html")

@app.route("/response", methods=['POST'])

def make_prediction():

    cbh=joblib.load('stroke_normv1_cox_SW1.1_fa22_k8__0FD20_FS0_VS0.3_modeday_06-12.1_cbh.pkl')
    print( 'PKL loaded' )
    stroke=chf=hypertension=comp=nocomp=cvd=0.0

    if request.method == 'POST':
        age = int( request.form['age'] )        

        for v in request.form.getlist('history'):

            if 'hypertension' in v:
                hypertension=1.0
            elif 'chf' in v:
                chf=1.0
            elif 'nocomp' in v:
                nocomp=1.0
            elif 'comp' in v:
                comp=1.0
            elif 'stroke' in v:
                stroke=1.0
            elif 'cvd' in v:
                cvd=1.0

        print(request.form.getlist('history'))

        mus = cbh['mus']
        stds= cbh['stds']+1e-10

        try:
            msg0="Based on collected info: %d years old at time of incident AF diagnosis with riskFactors: {Diabetes with comp %d,Diabetes w/o complications %d,
            prev_stroke %d,CVD %d,CHF %d, Hypertension %d}" %(age, comp, nocomp, stroke, cvd, chf, hypertension )
        except:
            msg0=''

        i=0
        age = (age - mus[i])/stds[i]; i+=1
        comp = (comp - mus[i])/stds[i]; i+=1
        nocomp = (nocomp - mus[i])/stds[i]; i+=1
        stroke = (stroke - mus[i])/stds[i]; i+=1
        cvd = (cvd - mus[i])/stds[i]; i+=1
        chf = (chf - mus[i])/stds[i]; i+=1
        hypertension = (hypertension - mus[i])/stds[i]; i+=1

        risk_score = np.exp( age*0.705+ comp*0.049 + nocomp*0.087 + stroke*0.167+ cvd*0.18 + chf*0.061 + hypertension*0.083 )

        cum_baseline_hazard_x = cbh['xx']
        cum_baseline_hazard_y = cbh['yy']
        baseline_survival_ = StepFunction(cum_baseline_hazard_x, np.exp(-cum_baseline_hazard_y) )
        surv_prb = StepFunction(x=baseline_survival_.x, y=np.power(baseline_survival_.y, risk_score ) )

    try:
        msg = 'Risk: %.2f' % risk_score
        
        msg1 = 'Chance of experiencing a stroke by year %d: %.1f%%' %(surv_prb.x[1*365]//365, 100-100*surv_prb.y[1*365] )
        msg2 = 'Chance of experiencing a stroke by year %d: %.1f%%' %(surv_prb.x[2*365]//365, 100-100*surv_prb.y[2*365] )
        msg3 = 'Chance of experiencing a stroke by year %d: %.1f%%' %(surv_prb.x[3*365]//365, 100-100*surv_prb.y[3*365] )
        msg5 = 'Chance of experiencing a stroke by year %d: %.1f%%' %(surv_prb.x[5*365]//365, 100-100*surv_prb.y[5*365] )
        msg8 = 'Chance of experiencing a stroke by year %d: %.1f%%' %(surv_prb.x[8*365]//365, 100-100*surv_prb.y[8*365] )
    except:
        msg = 'Cannot load server; please try again later...'; msg2=msg1=msg3=''

    heading='Results of estimation'

    return render_template("index.html", heading=heading, msg0=msg0, msg=msg, msg1=msg1, msg2=msg2, msg3=msg3, msg5=msg5, msg8=msg8 )


if __name__ == '__main__':
    app.run(debug=True)
