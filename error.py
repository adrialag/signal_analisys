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

#ALIMENTATORE IN CONTINUA

