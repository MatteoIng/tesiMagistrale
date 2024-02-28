import json
import os
import sys

import numpy as np
from matplotlib import pyplot as plt


def visualizza_reward_mosse():
    dati = ''
    #with open(pathCompleto, "r") as file:
    with open("/home/matteo/Documenti/tesi/reward_mosse.txt", "r") as file:
        dati = file.read()
    dati_dict = json.loads(dati)
    
    print(dati_dict)

    a = dati_dict['attaccante']
    b = dati_dict['difensore']



    # insieme di 2 e 3
    app = dati_dict['attaccante']
    bpp = dati_dict['difensore']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []

    # reward per ogni partita
    """ for i in range(len(app)) :
        yA.append(app[i][1])
        yB.append(bpp[i][1])
    #print('YA:',yA)
    #print('YB:',yB)
    plt.figure()
    plt.title('ADDESTRAMENTO/EVALUATE')
    plt.ylabel('reward')
    plt.xlabel('t')
    #plt.xlabel('numero mosse per partita')
    plt.plot(np.arange(len(yA)),yA)
    plt.plot(np.arange(len(yB)),yB)
    
    plt.legend(['attaccante','difensore']) """


    # reward per epoca
    app = dati_dict['attaccante']
    bpp = dati_dict['difensore']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []
    tempo = []

    aPPEND = 0
    bPPEND = 0
    sommaTempo = 0

    count = 0
    for i in range(len(app)):
        aPPEND += app[i][1]
        bPPEND += bpp[i][1]
        sommaTempo = bpp[i][2]

        count +=1
        if count == 10:
            count = 0
            #print(i)
            #print(c/10)
            yA.append(aPPEND/10)
            yB.append(bPPEND/10)
            tempo.append(sommaTempo)
            aPPEND = 0
            bPPEND = 0
            
    plt.figure()
    plt.title('reward per epoca')
    plt.ylabel('reward')
    plt.xlabel('epoche')
    
    plt.plot(np.arange(len(yB)),yB)
    xl = 300
    rb = [-1.4 for i in range(xl)]
    plt.plot(np.arange(xl),rb)
    plt.ylim(-3.5,0)
    plt.xlim(0,300)
    plt.legend(['difensore','reward ottimo difensore'])
    
    
    """ # manteniamo per sicurezza
    plt.figure()
    xl=600
    rb = [-1.4 for i in range(xl)]
    plt.plot(tempo,yB)
    plt.plot([i for i in range(xl)],rb)
    plt.xlabel('secondi')
    plt.ylabel('reward')
    plt.ylim(-3.5,0)
    plt.xlim(0,600)
    #plt.xticks(tempo,tempo)
    print(tempo) """

    # Crea il grafico
    fig, ax = plt.subplots()

    # Plotta i dati
    ax.plot(tempo,yB)
    ax.set_xlabel('secondi')
   
    ax2 = ax.twiny()
    ax2.plot(tempo,yB)
    ax2.set_xticks([0,tempo[int(len(tempo)/4)],tempo[int(len(tempo)/2)],tempo[int(3*(len(tempo))/4)],tempo[-1]],[0,int(len(yB)/4),int(len(yB)/2),int(3*(len(yB)/4)),len(yB)])
    ax2.set_xlabel('epoche')

    
    plt.show()


    # il numero di mosse fatte nel tempo, per partita
    """ y = []
    for i in a :
        y.append(i[0])
    plt.figure()
    plt.title('MOSSE ATT+DIF fatte per ogni partita')
    plt.ylabel('n mosse')
    plt.xlabel('partite')
    plt.plot(np.arange(len(y)),y) """




    # reward rispetto al numero di mosse fatte dall'attaccante
    """ x = []
    y = []
    a.sort()
    for i in a :
        x.append(i[0])
        y.append(i[1])
    #print(len(x))
    #print(len(y))
    plt.figure()
    plt.title('REWARD attaccante rispetto il N.MOSSE')
    plt.ylabel('reward attaccante')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y) """

    # Grafico 3
    # reward rispetto al numero di mosse fatte dal difensore
    """ x = []
    y = []
    b.sort()
    for i in b :
        x.append(i[0])
        y.append(i[1])
    #print(len(x))
    #print(len(y))
    plt.figure()
    plt.title('')
    plt.title('REWARD difensore rispetto il N.MOSSE')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y) """

    plt.show()


visualizza_reward_mosse()
