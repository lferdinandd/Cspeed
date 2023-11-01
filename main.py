# calcul vitesse optimale de l'avion en fonction du nombre de cellules solaires le long de la corde
print("")
print("Bienvenue sur Cspeed ")
print("")
import csv 
import numpy as np 
import matplotlib.pyplot as plt


def air_rho(altitude = 0, temperatureSol = 290, pressionSol = 1020):
    return 1.3 
# ajouter variation en fonction de l'altitdue, température au sol et pression au sol 

def air_viscositeDynamique(temperature=290): 
    return 2.028*10**(-5)
# ajouter variation en fonction de la température 

def reynolds(vitesse, corde_longueur, air_rho=air_rho(), air_viscositeDynamique=air_viscositeDynamique()): 
    return air_rho*vitesse*corde_longueur/air_viscositeDynamique

def ouverture_xfoil_data(nom_profil='n63412-il'): 
    data = {}
    l = ['50000','100000','200000','500000','1000000']
    for i in l : 

        with open('xf-'+nom_profil+'/xf-'+nom_profil+'-'+i+'-n5.csv', 'r') as fichier_csv:
            for _ in range(10):
                next(fichier_csv)
            lecteur_csv = csv.DictReader(fichier_csv)   
            data[i+'-n5'] = []   
            for ligne in lecteur_csv:
                data[i+'-n5'].append(ligne)
  
        with open('xf-'+nom_profil+'/xf-'+nom_profil+'-'+i+'-n5.csv', 'r') as fichier_csv:
            for _ in range(10):
                next(fichier_csv)
            lecteur_csv = csv.DictReader(fichier_csv)   
            data[i] = []   
            for ligne in lecteur_csv:
                data[i].append(ligne)
        

    return data 
# -> Renvoie un dictionnaire indéxé par les nombres de Reynolds, contenant une liste des lignes du tableau. 
# Chaque ligne est un dictionnaire indexé par le titre des colonnes du fichier csv 

data = ouverture_xfoil_data()
corde_longueur = 0.3 
poidSurfacique = 40 #N/m2 
surfaceProjetee = 5*(12/100)*corde_longueur 

x,y = [],[]
for vitesse in [int(x)*air_viscositeDynamique()/(air_rho()*corde_longueur) for x in ['50000','100000','200000','500000','1000000']]: 
    Re = reynolds(vitesse, corde_longueur) 
    Re = str(min(['50000','100000','200000','500000','1000000'], key=lambda x: abs(int(x) - Re)))

    # Calcul Cl 
    Cl = poidSurfacique*2/((vitesse**2)*air_rho())

    # Calcul Alpha, Cd
    i     = min([i for i in range(len(data[Re]))], key=lambda point: abs(float(data[Re][point]['Cl'])-Cl))
    Cl    = data[Re][i]['Cl']
    alpha = data[Re][i]['Alpha']
    Cd    = data[Re][i]['Cd']
    poussee_moteur = (1/9.81) * (1/2) * air_rho() * (vitesse**2) * surfaceProjetee * float(Cd) * 1/(np.cos(float(alpha)*3.14/180))

    x.append(vitesse*3.6)
    y.append(poussee_moteur*1000)
    print("")
    print("Vitesse de l'avion        ",round(vitesse*3.6),"km/h")
    print("Nombre de Reynolds        ",float(Re))
    print('Cl                        ',round(float(Cl),3))
    print('Alpha                     ',round(float(Alpha),3))
    print('Cd                        ',round(float(Cd),3))
    print('Poussée moteur nécessaire ',round(poussee_moteur,3),"kg")

plt.plot(x,y,marker ='o')
plt.xlabel("Vitesse de l'avion en km/h")
plt.ylabel("Poussée du moteur nécessaire / nombre de rangée de panneaux solaires en g")
plt.show()
print("")
print("Fin du programme ") 
print("")  
    
    







