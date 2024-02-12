import json
import os
import sys

import numpy as np
from matplotlib import pyplot as plt


def visualizza_reward_mosse():
    dati = ''
    #with open(pathCompleto, "r") as file:
    with open("/home/matteo/Documenti/GitHub/tesiMagistrale/fileGrafici/reward_mosse.txt", "r") as file:
        dati = file.read()
    dati_dict = json.loads(dati)
    
    #print(dati_dict)

    a = dati_dict['attaccante']
    b = dati_dict['difensore']



    # insieme di 2 e 3
    app = dati_dict['attaccante']
    bpp = dati_dict['difensore']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []

    for i in range(len(app)) :
        yA.append(app[i][1])
        yB.append(bpp[i][1])
    """ print('YA:',yA)
    print('YB:',yB) """
    plt.figure()
    plt.title('ADDESTRAMENTO/EVALUATE')
    plt.ylabel('reward')
    plt.xlabel('t')
    #plt.xlabel('numero mosse per partita')
    plt.plot(np.arange(len(yA)),yA)
    plt.plot(np.arange(len(yB)),yB)
    
    plt.legend(['attaccante','difensore'])


    # reward per epoca
    app = dati_dict['attaccante']
    bpp = dati_dict['difensore']
    """ print('APP:',app)
    print('BPP:',bpp) """

    yA = []
    yB = []

    aPPEND = 0
    bPPEND = 0
    count = 0
    for i in range(len(app)):
        aPPEND+=app[i][1]
        bPPEND+=bpp[i][1]
        count +=1
        if count == 10:
            count = 0
            #print(i)
            #print(c/10)
            yA.append(aPPEND/10)
            yB.append(bPPEND/10)
            aPPEND = 0
            bPPEND = 0
    """ print('YA:',yA)
    print('YB:',yB) """
    plt.figure()
    plt.title('reward per epoca')
    plt.ylabel('reward')
    plt.xlabel('epoche')
    ra = [1 for i in range(len(yA))]
    rb = [-0.1 for i in range(len(yA))]
    plt.plot(np.arange(len(yA)),ra)
    plt.plot(np.arange(len(yA)),rb)
    plt.plot(np.arange(len(yA)),yA)
    plt.plot(np.arange(len(yB)),yB)
    plt.legend(['attaccante','difensore'])



    # il numero di mosse fatte nel tempo, per partita
    y = []
    for i in a :
        y.append(i[0])
    plt.figure()
    plt.title('MOSSE ATT+DIF fatte per ogni partita')
    plt.ylabel('n mosse')
    plt.xlabel('partite')
    plt.plot(np.arange(len(y)),y)




    # reward rispetto al numero di mosse fatte dall'attaccante
    x = []
    y = []
    a.sort()
    for i in a :
        x.append(i[0])
        y.append(i[1])
    """ print(len(x))
    print(len(y)) """
    plt.figure()
    plt.title('REWARD attaccante rispetto il N.MOSSE')
    plt.ylabel('reward attaccante')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y)
    

    # Grafico 3
    # reward rispetto al numero di mosse fatte dal difensore
    x = []
    y = []
    b.sort()
    for i in b :
        x.append(i[0])
        y.append(i[1])
    """ print(len(x))
    print(len(y)) """
    plt.figure()
    plt.title('')
    plt.title('REWARD difensore rispetto il N.MOSSE')
    plt.xlabel('numero mosse per partita')
    plt.plot(x,y)

    plt.show()



