import random as rd 
import sys 
import numpy as np
import os

# Quelques optimisations possibles : 
#   Créer une seule séquence dans le client, 0 = indifférent, 1 = aimé, 2 = pas aimé.

# Classe du client, pour appliquer la fonction d'évalution d'une solution donnée.
class Client: 
    def __init__(self,ingrAimes,ingrDetestes):
        self.ingrAimes = ingrAimes
        self.ingrDetestes = ingrDetestes
        self.seq_aimes = []
        self.seq_detestes = []

    def initialiserSequences(self,ingredients):
        n = len(ingredients.ingredients)
        self.seq_aimes = [0] * n
        self.seq_detestes = [0] * n 

        for ingredient in self.ingrAimes:
            index = list(ingredients.ingredients.keys()).index(ingredient)
            self.seq_aimes[index] = 1

        for ingredient in self.ingrDetestes:
            index = list(ingredients.ingredients.keys()).index(ingredient)
            self.seq_detestes[index] = 1

# Les ingrédients aimés par personne seront retirés de la liste des ingrédients,
# pour la génération de la solution optimale.
class Ingredients:
    def __init__(self):
        self.ingredients = {}

    def ajouterIngredient(self, ingredient):
        if(not(ingredient in self.ingredients.keys())): 
            self.ingredients[ingredient] = 0

    # Indique que l'ingrédient est aimé par une personne supplémentaire.
    def ingredientEstAime(self, ingredient):
        self.ingredients[ingredient] += 1
    
# Classe de l'algorithme, là où on résout le problème.
class RecuitSimule:
    def __init__(self, solutionInit, ingredients,clients,temp, tempMin, iStop):
        self.ingredients = ingredients
        self.clients = clients
        self.nbClients = len(clients)
        self.nbIngredients = len(ingredients.ingredients)

        self.T = temp
        self.Tmin = tempMin
        self.iStop = iStop

        self.solutionInit = solutionInit
        self.solCr = solutionInit #solution courante
        self.valCr = RecuitSimule.evalSolution(solutionInit)

    # Génère une séquence voisine.
    def genereVoisin(seq):
        i = rd.randint(0,len(seq) - 1)
        seq[i] = 1 - seq[i]
        return seq
    
    # Évalue la solution proposée.
    def evalSolution(seq):
        n = nbClients
        for client in clients:
            nbi = 0 # Nombre d'ingredients que le client aime, dans la solution.
            nbaimes = 0
            ok = True
            for i in range(len(seq)):
                val = seq[i]
                nbaimes += client.seq_aimes[i]
                if ((client.seq_aimes[i] == val) and (val == 1)):
                    nbi+=1
                if ((client.seq_detestes[i] == val) and (val == 1)):
                    ok = False
                    break
            # On vérifie que le client a tous les ingrédients qu'il aime et aucun qu'il n'aime pas.
            if ((not ok) or (nbi != nbaimes)):
                n-=1 # Sinon on retire le client.
        return n
    
    # Algorithme du recuit simulé qui calcule une solution "optimale".
    def solutionOptimale(self):
        i = 0
        while self.T >= self.Tmin and i < self.iStop:
            seqCand = RecuitSimule.genereVoisin(self.solCr)
            valCand = RecuitSimule.evalSolution(seqCand)
            if self.valCr <= valCand:
                self.valCr = valCand
                self.solCr = seqCand
            else:
                probaTiree = rd.random()
                dE = self.valCr - valCand
                if probaTiree < np.exp(-dE/self.T):
                    self.solCr = seqCand
                    self.valCr = valCand
            # Abaissement de la température suivant une loi exponentielle ou géométrique.
            self.T = self.T * 0.9
            i+=1
        return RecuitSimule.traduireSequence(self.ingredients,self.solCr)
    
    def traduireSequence(ingredients,seq):
        ingr = list(ingredients.ingredients.keys())
        tab = []
        for i in range(len(seq)):
            if (seq[i] == 1):
                tab.append(ingr[i])
        return tab
    
# -------------------------------- [Main] --------------------------------------
    
# Liste des ingrédients et des clients.
ingredients = Ingredients()
clients = []

# On vérifie le nombre d'arguments passé en ligne de commance.
if len(sys.argv) != 2:
    raise TypeError("Le nombre d'arguments n'est pas valide.")
    sys.exit(1)

filename = sys.argv[1]

# On parcourt le fichier pour récupérer les informations.
with open(filename,'r') as fichier: 
    # Nombre de clients.
    N = int(fichier.readline())

    # Parcour des lignes deux par deux.
    for i in range(N):
        # Ingrédients aimés.
        ligne_1 = fichier.readline().strip().split()
        nb_ingredients_aimes = int(ligne_1[0])
        ingredients_aimes = ligne_1[1:]

        # Rajoute l'ingrédient dans la liste des ingrédients, et comme il est aimé par le client, on incrémente.
        for j in range(1, len(ligne_1)):
            # On ignore le premier élément de la ligne.
            ingredients.ajouterIngredient(ligne_1[j])
            ingredients.ingredientEstAime(ligne_1[j])

        # Ingrédients mal aimés.
        ligne_2 = fichier.readline().strip().split()
        nb_aliments_destes = int(ligne_2[0])
        ingredients_detestes = ligne_2[1:]

        for j in range(1, len(ligne_2)):
            # On ignore le premier élément de la ligne.
            ingredients.ajouterIngredient(ligne_2[j])

        # Crée un nouveau client avec les informations.
        client = Client(ingredients_aimes,ingredients_detestes)
        clients.append(client)

nbClients = len(clients)
nbIngr = len(ingredients.ingredients)

# Parcourt les clients pour générer des séquences de bits pour les ingrédients aimés et détestés.
for client in clients:
    client.initialiserSequences(ingredients)

def genererSolutionInitiale(n):
    return [rd.randint(0, 1) for _ in range(n)]

temp = 52
tempMin = 0.00000001
stopI = 10000000

fichierSave = "resultats/elabore"
fichierLoad = "init.txt"

# print("La solution initiale :")
# print(solinit)
# print(RecuitSimule.traduireSequence(ingredients,solinit))
# print(RecuitSimule.evalSolution(solinit))

# Code de la génération d'une solution initiale

seq_init = [0] * nbIngr

#seq_init = genererSolutionInitiale(nbIngr)
#itest = 0 
#itestMax = 50
#valeur = RecuitSimule.evalSolution(seq_init)
#meilleure_valeur = valeur
#while (valeur < 1500) and (itest < itestMax):
#    if(valeur > meilleure_valeur):
#        if os.path.exists(fichierLoad):
#            os.remove(fichierLoad)
#        seq_traduite = RecuitSimule.traduireSequence(ingredients, seq_init)
#        with open(fichierLoad, 'w') as fichier:
#            for element in seq_traduite[:-1]:
#                fichier.write(str(element) + '\n')
#        print("nouveau ! : ",valeur)
#        meilleure_valeur = valeur
#    seq_init = genererSolutionInitiale(nbIngr)
#    valeur = RecuitSimule.evalSolution(seq_init)
#    itest +=1
#print("Valeur de la solution trouvée = ",meilleure_valeur)

listofing = list(ingredients.ingredients.keys())

# Récupérer la solutionInitiale
with open(fichierLoad, 'r') as fichier:
    for line in fichier:
        ingredient = line.rstrip('\n')
        index = listofing.index(ingredient)
        seq_init[index] = 1

# Générer 100 variations aléatoires 
        
somme_dE = 0
seq_cr = seq_init
valCr = RecuitSimule.evalSolution(seq_cr)
nbVariations = 100
for i in range(nbVariations):
    candidat = RecuitSimule.genereVoisin(seq_cr)
    valCand = RecuitSimule.evalSolution(candidat)
    somme_dE += valCr - valCand
    seq_cr = candidat
print("La moyenne des variations est de ",somme_dE/nbVariations)

# Algorithme du recuit simulé.
#algo_recuit = RecuitSimule(
#   seq_init,
#   ingredients,
#   clients,
#   temp,
#   tempMin,
#   stopI
#)

#sol = algo_recuit.solutionOptimale()

#with open("resultats/elaboree/resultat.txt", 'w') as fichier:
#    for element in sol[:-1]:
#        fichier.write(str(element) + '\n')
#    fichier.write(str(sol[-1]))
#print("La valeur de la solution = " + str(algo_recuit.valCr))