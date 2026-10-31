#CODICE PER IL CALCOLO AUTOMATICO DEGLI ERRORI DAGLI STRUMENTI DI LABORATORIO

#OSCILLOSCOPIO KEYSIGHT DSOX1102G
# Manuale: https://www.keysight.com/us/en/assets/7018-05520/data-sheets/5992-1965.pdf
# prime due funzioni per stimare la div dello strumento se non fornita direttamente
def _stima_div_verticale(valore):
    """Stima la scala verticale (V/div) ottimale (sequenza 1-2-5 su 8 divisioni)."""
    scale = [
        1e-3, 2e-3, 5e-3,
        10e-3, 20e-3, 50e-3,
        100e-3, 200e-3, 500e-3,
        1.0, 2.0, 5.0
    ]
    v = abs(valore)
    for s in scale:
        if v <= 6 * s:  # Segnale entro ~6 delle 8 divisioni verticali
            return s
    return scale[-1]
def _stima_div_orizzontale(periodo):
    """Stima la scala orizzontale (s/div) ottimale (sequenza 1-2-5 su 10 divisioni)."""
    t = abs(periodo)
    for exp in range(-9, 2):
        for b in (1, 2, 5):
            s = b * (10 ** exp)
            if t <= 5 * s:  # Un periodo entro metà schermo (5 su 10 divisioni)
                return s
    return 50.0
# funzione principale per il calcolo delle incertezze
def dsox1102g(misura, div, valore):
    v = abs(valore)
    if misura == "dp":
        # Se div non viene fornito (None o 0), stima la scala ottimale dal valore
        if div is None or div <= 0:
            div = _stima_div_verticale(v)
        # Guadagno verticale DC: 3% per >= 10 mV/div, 4% per < 10 mV/div
        gain_acc = 0.03 if div >= 10e-3 else 0.04
        # Incertezza cursori/lettura (Dual Cursor): 0.5% del fondo scala (8 * div)
        cursor_err = 0.005 * (8 * div)
        return gain_acc * v + cursor_err
    elif misura == "dt":
        if div is None or div <= 0:
            div = _stima_div_orizzontale(v)
        return 50e-6 * v + 0.0016 * (div * 10) + 200e-12
    else:
        periodo = 1.0 / v
        if div is None or div <= 0:
            div = _stima_div_orizzontale(periodo)
        # Propagazione errore su f = 1 / T -> sigma_f = sigma_T * f^2
        return dsox1102g("dt", div, periodo) * (v ** 2)


# MULTIMETRO FLUKE 45 
# funzione per ottenere in automatico la risoluzione a partire dal valore misurato
def alternata(valore):
    v = abs(valore)
    if v < 300e-3:
        return 10e-6
    elif v < 3:
        return 100e-6
    elif v < 30:
        return 1e-3
    elif v < 300:
        return 10e-3
    else:
        return 100e-3
#funzione effettiva per restituire i valori richiesti
def fluke45(misura, div=0, valore=0):
    v = abs(valore)
    if misura == "r":
        # Specifiche resistenza: ±(% lettura + digit)
        if v < 300:
            return v * 0.0005 + 2 * 0.01 + 0.02   # 0.05% + 2 digit + 0.02 ohm
        elif v < 3e3:
            return v * 0.0005 + 2 * 0.1           # 0.05% + 2 digit
        elif v < 30e3:
            return v * 0.0005 + 2 * 1             # 0.05% + 2 digit
        elif v < 300e3:
            return v * 0.0005 + 2 * 10            # 0.05% + 2 digit
        elif v < 3e6:
            return v * 0.0006 + 2 * 100           # 0.06% + 2 digit
        elif v < 30e6:
            return v * 0.0025 + 3 * 1000          # 0.25% + 3 digit
        else:
            return v * 0.02 + 2 * 100e3           # 2.0% + 2 digit (range 300 MOhm)
    elif misura == "vc":
        # Specifiche tensione DC: ±(0.025% lettura + 2 digit)
        return v * 0.00025 + 2 * alternata(v)
    elif misura == "va":
        # Qui 'div' rappresenta la frequenza del segnale in Hz (20 Hz - 100 kHz)
        risoluzione = alternata(v)
        if div <= 50:
            return v * 0.02 + 10 * risoluzione    # 2.0% + 10 digit (20 - 50 Hz)
        elif div <= 10e3:
            return v * 0.002 + 10 * risoluzione   # 0.2% + 10 digit (50 Hz - 10 kHz)
        elif div <= 20e3:
            return v * 0.005 + 10 * risoluzione   # 0.5% + 10 digit (10 - 20 kHz)
        elif div <= 50e3:
            return v * 0.02 + 20 * risoluzione    # 2.0% + 20 digit (20 - 50 kHz)
        else:
            return v * 0.05 + 50 * risoluzione    # 5.0% + 50 digit (50 - 100 kHz)
