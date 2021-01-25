"""
Program:
    -wylicza współczynniki AR dla poszczegolnych pacjentów 
    -porównuje wzorce testowe z fazami
    - pokazuje cykl snu poszczegolnych pacjentow 
"""

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.ar_model import AR
import os
import do_zapisu as d_z

# funkcja importująca dane 
def tablica(kto):
    tab=[]    
    f="./patient/" + kto
    file = open(f+'.txt', 'r').read()    
    lines = file.split('\n')
    for line in lines:
        tab.append(line)
    return tab, kto[:8]

#funkcja wyliczająca współczynniki 
def AR_function(train):
    t=np.array(train)
    model=AR(t/1000)
    model_fit=model.fit()
    coef=model_fit.params
    return coef

#wzorce dla poszczególnych faz
def wzor(wybor):
    if wybor == 1:
        sin='REM.txt'
    else:
        sin='nonREM.txt'
        
    plik=open('./model/'+sin).read()
    lines=plik.split(',')
    tab=list()
    for line in lines:
        tab.append(line)
    
    return [float(tab[i])/2 for i in range(len(tab)-1)], sin[:2]

#funkcja porównująca fazy ze wzorcami 
def max_po_kolumnach(k,tab): #(jaka kolumna, tablica)
    a=tab[0][k]
    pozycja=0
    for i in range(1,len(tab)):
        if tab[i][k] > a:
            a=tab[i][k]
            pozycja=i
    return a, pozycja

if __name__=='__main__':
    tab_ilosc_faz=list()
    tab_fazy=list()
    tt=0
    
    #analiza kobiet 
    m='k19_12.00.cut_500'   #nazwa pliku kobiety. Pliki znajdują się w folderze patient
    w,who=tablica(m)
    z=list()
    z=[float(w[i]) for i in range(len(w)-1)]
    print("Tachograf znajduje sie w folderze ./wyniki/k/plot_RR")
    d_z.Ploty_zapisy(who,'k',z)

    tab=list()

    #########################################
    # tworzenie folderu dla danego pacjenta 
    if who[0] == 'm':
        path='./wyniki/m/'+who+'/'
    else:
        path='./wyniki/k/'+who+'/'
    try:
        os.makedirs(path)
    except:
        pass    
    #########################################
    # pętla, która dzieli serię na okna    
    for i in range(0,len(z),1000):
        k=1000        
        if i+k > len(z):    #pliki nie są równe dlatego u niektórych pacjentów ostatnie okno może być mniejsze 
            k=len(z)-i
        coef=AR_function(z[i:i+k])      #tworzenie współczynników   
        plt.plot(np.arange(1,6),coef[:5])
        tab.append(coef)
        
    y=np.array(tab)
    plt.xticks(np.arange(1,6))
    plt.title("wspolczynniki dla "+who[:3] )
    plt.savefig("./wyniki/k/"+who+"/coef_"+who+'.jpg',dpi=80)   
    print("Wykres z 5 pierwszymi współczynnikami znajduje się w: ./wyniki/k/ nazwa_pacjenta /")
    plt.show()
    
    #wpisywanie wspolczynnikow do pliku 
    plik=open(path+who+'_wyniki_AR.txt', 'w')
    for i in range(len(y)):
        for j in range(len(y[i])):
              s=str(y[i][j])
              plik.write(' %18s'%(s)+'%2s'%(' '))
        plik.write('\n')
    plik.close()
    print("Wszystkie współczynniki AR znajdują się w folderze: ./wyniki/k/ nazwa_pacjenta /")
    # zmiana tab na array
    
    tab_arr=np.array(tab)
    # porównanie wykresu i wzorców  które opisałem w rozdziale 2.2.1
    nazwy=['NREM','REM']
    for ii in range(2):
        kalka,sin=wzor(ii)
        kalka=np.array(kalka)*2
    #wyszukiwanie największej liczby , oraz jej pozycji w tablicy
        maks,pozycja=max_po_kolumnach(ii,tab_arr)           # wyszukiwanie najlepszego dopasowania dla wzorców 
        rozmiar_coef=len(kalka)
    #tworzenie wykresów porównawczych     
        plt.plot(np.arange(1,rozmiar_coef+1),tab_arr[pozycja])
        plt.plot(np.arange(1,rozmiar_coef+1),kalka)
        plt.xticks(np.arange(1,rozmiar_coef+1,2))
        plt.title(nazwy[ii]+' , '+who[:3])
        plt.legend([nazwy[ii],'test '+nazwy[ii]])
        plt.savefig(path+who+'_plot_'+sin+'.jpg')
        plt.show() 
    
    #tworzenie tablicy w której bedzie ilosć poszczegolnych faz 
    tab_ilosc_faz.append(d_z.Ilosc_faz_snu(who[:3],tab_arr))
    tab_fazy.append(d_z.Fazy_snu(who[:1],tab_arr))      #tworzenie wykresu z cyklami snu 
        
    wkw=tab_fazy[tt][1].split(' ')
    wkw=wkw[:-1]
    
    rwkw=[i for i in range(len(wkw))]
    plt.plot(np.arange(1,len(wkw)+1),wkw)
    plt.title(who)
    #plt.ylim('N','R')
    #plt.yticks(['R','n','N'])
    plt.xticks(np.arange(1,len(wkw)+1))
    plt.savefig('./wyniki/k/fazy_plot/'+who+'_plot.jpg',dpi=80)         
    plt.show()
    tt=tt+1
    
    #d_z.Ilosc_faz_zapis(tab_ilosc_faz,'./wyniki/k/')           
    d_z.Fazy_zapis(tab_fazy,'./wyniki/k/')
    
    print("Cykle snu znajdują się w folderze ./wyniki/k/fazy_plot/")
