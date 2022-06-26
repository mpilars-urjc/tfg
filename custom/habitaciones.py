def getBed(var):
    if var == "1":
        value = "90x190"
    elif var == "2":
        value = "105x190"
    elif var == "3":
        value = "135x190"
    elif var == "4":
        value = "150x190"
    elif var == "5":
        value = "2(90x190)"
    return value

def getBanos(banos, aseos):
    if aseos == 0:
        value = str(banos) + " baño(s)"
    else:
        value = str(banos) + " baño(s) y " + str(aseos) + " aseo(s)"
    return(value)

def getUso(var):
    if var == "IND":
        value = "individual"
    else:
        value = "doble"
    return value

def getTipo(var):
    if var == "INT":
        value = "interior"
    else:
        value = "exterior"
    return value

def yesNo(var):
    if var == True:
        value = "si"
    else:
        value = "no"
    return value   