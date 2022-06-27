# AFib

Site under construction!!!

## Introduction

Demos that can be tried using any (free) Google Colab:
- [Demos to the *risk estimation models*](stroke_bleed_death_estimations.ipynb) 
- [Demos to the *NNsurv architecture*](afib_predict_death_risks_nnsurv.ipynb) 

## Simplified

The simplified **death risk estimation model** can be [tested here](afib_predict_death.ipynb); it uses 14 variables:
- Current age
- Male sex?
- Has COPD
- Has cardiovascular disease
- Has congestive heart failure
- Has cancer
- Has metastatic caricnoma
- Has dementia
- Hospitalized before due to life management difficulties (injuries at care home)
- Hospitalized before due to disorders of fluid electrolyte, volume depletion
- Hospitalization due to brain injuries
- Age when diagnosed with cancer prior to AF Dx
- Age of last sepsis prior to AF Dx
- Diuretic loop: # of days prescribed with diuretic loop prior to AF Dx
