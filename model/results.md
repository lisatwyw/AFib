

## Results on SUPPORT

### Round 1
- 70% training set
- 9105 hospitalized patients
- maximum time2event: 5.5 

| Algm | Brier Score | C-index |
|--|--|--|
| Nnet-survival | n/a | 72.8 | 
| DeepSurv-150 | n/a | 73.8 |
| DeepSurv-117-78 | n/a | 73.90 |
| DeepSurv-156-78-117 | n/a | 73.90 |


### Round 2
- 70% training + validation set

| Algm | Settings|Brier Score | C-index |
|--|--|--|--|
| Nnet-survival | Zeros-BS64 | n/a | 72.7, 72.5 | 
| Nnet-survival | RandU-BS64 | n/a | 72.8, 72.7 | 
| MLP-surv |BN-DO0-BS64 | n/a | 74.9, 71.6 | 
| MLP-surv |BN-DO0.3-BS64 | n/a | 73.5, 73.1 | 
| MLP-surv |BN-DO0.3-BS256 | n/a | 72.5, 72.3 | 


### Round 3
- 70% training + validation set
- 19 intervals

| Algm | Settings| C-indices | DAUC |  Integated Brier Score  |
|--|--|--|--|--|
| MLP-surv | 200-50-19 | 0.72,0.72,0.71| .79 | 0.52 |
| MLP-surv | 200-100-50-19 |  0.73,0.73,0.73 | 0.80 | 0.49 |
| MLP-surv | 400-200-100-50-19 | 0.73,0.73,0.72  | 0.80 | 0.49 |

| Algm | Settings| C-indices | DAUC |  Integated Brier Score  |
|--|--|--|--|--|
| MLP-surv | 400-200-19 | 0.73,0.72,0.72  | 0.79 | 0.47 |
| | 400_200_19_corr_BN1_selu_DO0.3_07 |  0.73,0.72,0.72| 0.78 | 0.45 | 
| | 100_75_50_25_19_corr_BN1_selu_DO0.3_07 |  0.74,0.73,0.73 | 0.79 | 0.55 | 
| | 117_78_39_19_corr_BN1_selu_DO0.3_07-15 |0.73,0.73,0.73 | 0.79 | 0.45 | 
| DeepSurv | 200-100-50 BentIdentity | 0.74,0.74,0.74 | 0.80 | 0.47 | 
| Nnet-survival | 1 layer | 0.73,0.72,0.71 | 0.79| 0.44 |
| Py-Cox | 4dims-BS256 | n/a | 0.76 | 0.41  | 
| | 2dims-BS64 | n/a | 0.77 | 0.40  | 
| | 2dims-BS32 | 0.75 | 0.40 |
| | 2dims- | 0.78 | 0.41 |
BentIdentity: ```x + (torch.sqrt(1.+ x*x)- 1.)/2```

```
nnetsurv_07-15

last:
trn 0.72,0.71,0.71, DAUC=0.79, IBS=0.45
val 0.70,0.70,0.69, DAUC=0.76, IBS=0.44
tst 0.73,0.72,0.71, DAUC=0.79, IBS=0.45
best:
trn 0.72,0.71,0.71, DAUC=0.79, IBS=0.44
val 0.70,0.70,0.69, DAUC=0.76, IBS=0.43
tst 0.73,0.72,0.71, DAUC=0.79, IBS=0.44

```

```
deepsurv_200_100_50__07-15

trn 0.75,0.75,0.75, DAUC=0.81, IBS=0.49
val 0.72,0.72,0.72, DAUC=0.78, IBS=0.48
tst 0.74,0.74,0.74, DAUC=0.80, IBS=0.47

```

```
200_50_19_nph_BN1_selu_DO0.3_07-15

last:
trn 0.73,0.72,0.72, DAUC=0.80, IBS=0.58
val 0.70,0.69,0.69, DAUC=0.76, IBS=0.58
tst 0.72,0.72,0.71, DAUC=0.79, IBS=0.55

best:
trn 0.73,0.72,0.72, DAUC=0.79, IBS=0.54
val 0.71,0.70,0.69, DAUC=0.77, IBS=0.55
tst 0.72,0.72,0.71, DAUC=0.79, IBS=0.52
```

```
200_100_50_19_nph_BN1_selu_DO0.3_07-15
trn 0.74,0.74,0.73, DAUC=0.80, IBS=0.51
val 0.72,0.72,0.71, DAUC=0.78, IBS=0.52
tst 0.73,0.73,0.73, DAUC=0.80, IBS=0.49
```

```
400_200_100_50_19_nph_BN1_selu_DO0.3_07-15
trn 0.74,0.74,0.74, DAUC=0.79, IBS=0.52
val 0.73,0.72,0.72, DAUC=0.78, IBS=0.53
tst 0.73,0.73,0.73, DAUC=0.79, IBS=0.50

trn 0.74,0.73,0.73, DAUC=0.80, IBS=0.51
val 0.72,0.71,0.71, DAUC=0.78, IBS=0.52
tst 0.73,0.73,0.72, DAUC=0.80, IBS=0.49
```
