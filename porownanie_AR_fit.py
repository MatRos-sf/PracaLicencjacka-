# -*- coding: utf-8 -*-
"""
Porównanie funkcji AR oraz uproszczonego algorytmu metody fit() patrz dodaek C

"""

import numpy as np
from statsmodels.tsa.ar_model import AutoReg as AR


def AR_function(train):
    t=np.array(train)
    model=AR(t)
    model_fit=model.fit()
    coef = model_fit.params
    return coef

from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.tsatools import (lagmat, add_trend)
def uproszczony_fit(tab):
    tab=np.array(tab)           
    TAB=tab[:, None]
    l=round(12*(len(tab)/100.)**(1/4.))
    x=lagmat(TAB,maxlag=l,trim='both')
    X = add_trend(x, prepend=True, trend='c')
    Y=TAB[l:, :]
    o=OLS(Y,X).fit()
    return o.params
    
tab=[814, 431, 717, 489, 407, 693, 754, 724, 270, 557]
print(AR_function(tab))
print(uproszczony_fit(tab))

"""
funkcja "uproszczony_fit" jest tym samym co funkcja "AR_function" gdyż dla zrozumienia lini 14,16 wgłebiłem się 
w kod by sprawdzić w jaki sposob wyliczane są współczynniki 

"""