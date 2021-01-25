# -*- coding: utf-8 -*-
"""
Znajdują się tu funkcje zapisujące :
    -tablice do pliku 
    -wykresy 
    - funkcja która wyliczca odpowiednie cykle snu (rozdział 2.3)
"""
import matplotlib.pyplot as plt

def Ilosc_faz_snu(who,tab):
    nrem=0
    rem=0
    for i in range(len(tab)):
        if tab[i][0]>tab[i][1]:
            nrem=nrem+1
        else:
            rem=rem+1
    #plik=open(location+'ilosc_faz.txt','w')
    return [who,nrem,rem]
"""
def Ilosc_faz_zapis(tab,location):
    plik=open(location+'ilosc_faz.txt','w')
    for i in range(len(tab)):
        plik.write(tab[i][0]+'\tNREM: '+str(tab[i][1])+'\tREM: '+str(tab[i][2])+'\n')
    plik.close()
"""

# funkcja fazy snu patrz rozdział 2.3
def Fazy_snu(who,tab):
    tab_r1=[]
    tab_r2=[]
    fazy=[]
    #obliczanie różnic 
    for i in range(len(tab)):
        a=tab[i][0]
        b=tab[i][1]
        r=b-a
        tab_r1.append(r)
        tab_r2.append(a-b)
    maks_1=round(max(tab_r1),4)     #max_differ 
    
    #porównanie i przypasowanie odpowiedniej fazy snu 
    if who=='m':
        for i in tab_r1:
            if i<0:
                fazy.append('N ')
            elif i>maks_1 -0.15:
                fazy.append('R ')
            else:
                fazy.append('n ')
    else:
        for i in tab_r1:
            if i<0:
                fazy.append('N ')
            elif i>maks_1 -0.1:
                fazy.append('R ')
            else:
                fazy.append('n ')
        
    return [who,''.join(fazy)]        

def Fazy_zapis(tab,location):
    plik=open(location+'fazy.txt','w')
    for i in range(len(tab)):
        plik.write(tab[i][0]+'\t\t\t '+str(tab[i][1])+'\n')
    plik.close()

def Ploty_zapisy(kto,plec,dane):    

    plt.plot(dane)
    plt.xlabel('n')
    plt.ylabel('RR [ms]')
    plt.savefig('./wyniki/'+plec+'/plot_RR/'+kto+'.jpg',dpi=80)
    plt.show()