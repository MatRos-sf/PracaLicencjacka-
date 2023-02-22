import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.ar_model import AR

#funkcja wyliczająca współczynniki autoregresji 
def AR_function(train):
    t=np.array(train)
    model=AR(t)
    model_fit=model.fit()
    coef=model_fit.params
    return coef

# funkcja licząca wartosc bezwglegna w serii 
def srednia(y):    
    tab=list()
    d=len(y[0])
    for i in range(d):
        s=0
        for j in range(len(y)):
            z=np.abs(y[j][i])
            s=s+z
        tab.append(s/len(y))        
    return tab


# wpisywanie do pliku z tablicy 2 wymiarowej 
def do_pliku_2(name,tab):
    plik=open(name+'.txt', 'w')
    for i in range(len(tab)):
        for j in range(len(tab[i])):
           s=tab[i][j]
           plik.write(' %12s'%(s)+'%2s'%('$'))
           #plik.write(s+' \n')
        plik.write(' \n')
    plik.close()

#wpisywanie do pliku z tablica jednowymiarowa 
def do_pliku_1(name,tab):
    plik=open(name+'.txt', 'w')
    for i in range(len(tab)):
        s=tab[i]
        plik.write('%s'%(s)+',')
    plik.close()        

if __name__=='__main__':  

     
    # funkcja nonREM
    
    x=np.linspace(0,300,10000)
    y=np.sin(0.25*2*np.pi*x)+np.sin(0.10*2*np.pi*x)
    
    print("funkcja f= 1*y+0*szum ")
    plt.plot(y)
    plt.show()
    
    no=np.random.normal(1,0.1,10000)    #tworzenie szumu 
    
    A,B=0.01,1                          #zmienne do manipulowania proporcjami 
    
    X=[i for i in range(1,23)]
    
    y_1=(float(A)*y+float(B)*no)        #tworzenie funkcji fazy nonREM 
    
    #wyswietlanie pierwszych 200 pkt dla interwałow dla funkcji z lini 50 oraz dla fazy nonREM lina 62 
    
    plt.subplot(2,1,1)
    plt.plot(x[:200],y[:200])
    plt.savefig('interwaly_dla_funkcji_pierwotnej.jpg',dpi=50)
    plt.show()
    plt.subplot(2,1,1)
    plt.plot(x[:200],y_1[:200])
    plt.savefig('interwaly_dla_seri_nonREM.jpg', dpi=80)
    plt.show()
   
    # wyliczanie współczynników dla okien po 1000 pkt
    tab=list()
    for i in range(0,len(y_1),1000):
        k=1000      
        if i+k > len(y_1):
            k=len(y_1)-i                
        coef=AR_function(y_1[i:i+k])        
        tab.append(coef)
        plt.plot(coef)
        
    y_t=np.array(tab)
    plt.title("współczynniki z funkcji AR dla y_NREM")
    plt.savefig('coef_nonREM.jpg',dpi=80)
    plt.show()                              #wyswietlanie współczynników serii testowej dla fazy nonREM 
    
    #wyliczanie STD dla serii nonREM
    ST_N=np.std(y_t,axis=0)             
    
    #wpisanie do pliku STD oraz wszystkich wspołczynników 
    do_pliku_1('STD_nonREM',ST_N)
    do_pliku_2('coef_nonREM',tab)
     
    #wyliczanie wartosci bezwzglednej sredniej dla nonREM     
    srednia_1=np.array(srednia(tab))
    do_pliku_1('nonREM',srednia_1)          #aB
    
    tab.clear()
    tab=list()

    
    
    # funkcja REM
    
    y_2=(float(B)*y)+(float(A)*no)          # tworzenie funkcji dla fazy REM 

    #wyswietlanie pierwszych 200 pkt dla interwałow dla  fazy REM lina 106 
    
    plt.subplot(2,1,2)
    plt.plot(x[:200],y_2[:200])
    plt.savefig('interwaly_dla_seri_REM.jpg', dpi=72)
    plt.show()
       
    # wyliczanie współczynników AR dla okien po 1000 pkt
    for i in range(0,len(y_2),1000):
        k=1000            
        if i+k > len(y):
            k=len(y)-i
        coef=AR_function(y_2[i:i+k])
        os=[i for i in range(1,len(coef)+1)]
        plt.plot(os,coef)
        tab.append(coef)        
    y_t=np.array(tab)
    plt.title("współczynniki z funkcji AR dla y_REM")
    plt.savefig('coef_REM.jpg',dpi=80)
    plt.show()              #wyswietlanie współczynników serii testowej dla fazy REM 
    
    #wyliczanie STD dla serii REM
    ST_R=np.std(y_t,axis=0)
    
    #wpisanie do pliku STD oraz wszystkich wspołczynników 
    do_pliku_2('coef_REM',tab)
    do_pliku_1('STD_REM',ST_R)

    #wpisywanie do pliku sredniej z wspolczynnikow dla fazy REM 
    srednia_2=np.array(srednia(tab))
    do_pliku_1('REM',srednia_2)      #bA
    
    #wyswietlanie wzorcow fazy nonREM i REM 
    ZZ=np.array(tab)   
    plt.plot(X,srednia_1,label='nonREM')   
    plt.plot(X,srednia_2,label='REM')  
    plt.legend()
    plt.savefig('N_R.jpg',dpi=80)
    plt.show()
    
    print("Wszystkie wykresy, wspolczynniki oraz ich srednie znajdują sie w folderze model")
    