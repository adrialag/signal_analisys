#Codice per calcolare automaticamente gli errori strumentali in laboratorio

#OSCILLOSCOPIO
#manuale https://www.keysight.com/us/en/assets/7018-05520/data-sheets/5992-1965.pdf
def dsox1102g(misura, div, valore):#valore incertezza dipenderà dalla valore misurato e dalle divisioni
    if misura=="dp":
        if div>10E-3:
            return div*8*0.03
        else:
            return div*8*0.04
    elif misura=="dt":
        return 50E-6*valore+0.0016*div*10+200E-12
    elif misura=="f":
        return dsox1102g('dt', div, valore)*valore**2

#FLUKE 45
#aggiungere il manuale del fluke
#per via dei vari casi per la corrente alternata crea una funzione aggiuntiva
def alternata(valore):
    if valore < 300E-3:
        return 10E-6
    elif valore < 3:
        return 100E-6
    elif valore < 30:
        return 1E-3
    elif valore < 300:
        return 10E-3
    else:
        return 100E-3
def fluke45(misura, div, valore):
    #aggiungere convertitore valore -> div quando possiible almeno stima
    if misura =="r":
        if valore<300:
            return valore*0.05+0.02+2*0.01
        elif valore<3E3:
            return valore*0.05+2*0.1
        elif valore<30E3:
            return valore*0.05+2*1
        elif valore<300E3:
            return valore*0.05+2*10
        elif valore<3E6:
            return valore*0.06+2*100
        elif valore<30E6:
            return valore*0.25+3*1000
        else:
            return valore*0.02
    if misura=="vc":
        if valore < 300E-3:
            return valore*0.025+2*10E-6
        elif valore < 3:
            return valore*0.025+2*100E-6
        elif valore < 30:
            return valore*0.025+2*1E-3
        elif valore <300:
            return valore*0.025+2*10E-3
        else:
            return valore*0.025+2*100E-3
    if misura=="va": #in queste misure div indica la frequenza del segnale
        if div < 50:
            return valore*0.02+10*alternata(valore)
        elif div < 10E3:
            return valore*0.002+10*alternata(valore)
        elif div < 20E3:
            return valore*0.005+10*alternata(valore)
        elif div < 50E3:
            return valore*0.02+20*alternata(valore)
        elif div < 100E3:
            return valore*0.05+50*alternata(valore)

