def mafonction(nom="ANNA", nom2= ""):
    print("Hello **********************")
    print("Salut **********************")
    print("Au revoir **********************")
    if nom== "ANNA":
        print("Condition une vraiiiiiiiiiiiiiiiiiiiiiiiii")
    else:
        print("Condition une faussssssssssse")

    if nom2=="ABOU":
        print("vraiiiiiic  condition 2")
    elif nom2=="DRAMANE":
        print("vraiiiiiiii pour elif")

    motos = ["CENT12", "CENT114", "HONDA", "YAMAHG"]


    for i in motos:
        print(f"HELLLLO  {i} ")


    i = 0
    while i < 1000:
        print("I plus petiti")
        i = i + 1





mafonction(nom2 = "SANOU")



def multi_by(x, y=10):
    return x*y

var = multi_by(1999999, 10000000000000000000)


print(var)



genre = "F"

variable = "ANA" if genre== "F" else "ABOU"

print(variable)