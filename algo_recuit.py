import random as rd 
import sys 
import numpy as np
import math

# Classe client avec les infos du client : 
# Les ingrédients qu'il aime, les ingrédients qu'il n'aime pas.
# Et respectivement, le nombre d'ingrédients de chaque.
class Client: 
    def __init__(self, ingredients_aimes, ingredients_detestes):
        self.ingredient_aimes = ingredients_aimes
        self.nb_aimes = len(ingredients_aimes)
        self.ingredient_detestes = ingredients_detestes
        self.nb_detestes = len(ingredients_detestes)

# Classe des ingrédients qui effectue des stats dessus.
class Ingredients:
    def __init__(self):
        self.ingredients = {}
        self.nom_ingr = []

    def add_ingredient(self, ingredient):
        if(not self.ingredients in self.ingredients.values()): 
            self.ingredients[ingredient] = 0
            self.nom_ingr.append(ingredient)

    # Incrémente le compteur de client qui aime cet ingrédient.
    def ingredient_is_liked(self, ingredient):
        self.ingredients[ingredient] += 1

    def get_meilleurs_ingredients(self, n):
        ordre_decroissant = sorted(self.ingredients.items(), key=lambda x: x[1], reverse=True)
        seq = [0] * len(self.ingredients) # instancie la séquence à 0 (bits)
        meilleurs_ingredients = [ingredient for ingredient, _ in ordre_decroissant[:n]]
        # Met l'indexe correspondant de la séquence de nb_ingredients bits à 1.
        # Les bits nuls veulent dire que l'on ne prend pas cet ingrédient.
        for ingredient in meilleurs_ingredients:
            index_ingredient = list(self.ingredients.keys()).index(ingredient)
            seq[index_ingredient] = 1
        return seq

class RecuitSimule:
    def __init__(self,solution,ingredients) -> None:
        self.solution = solution
        self.solutionCourante = solution
        self.ingredients = ingredients
        self.nb_clients_sol_courante = self.evaluation_solution(solution)
        self.Imax = len(ingredients.ingredients)

        # Paramètres variants.
        self.T = 0.2 * self.nb_clients_sol_courante
        self.tau = 1e4

    def genereVoisin(self):
        seq = self.solutionCourante
        length = len(seq)
        start = 0
        end = length
        if (length > 2):
            start = rd.randint(0, length - 2)  # Point de départ aléatoire
            end = rd.randint(start+1, length - 1)
        seq[start:end + 1] = reversed(seq[start:end + 1])
        return seq
    
    def traduireSequence(self,seq):
        tab = []
        for i in range(len(seq)):
            if (seq[i] == 1):
                tab.append(self.ingredients.nom_ingr[i])
        return tab
    
    # Calcul de la fonction d'évalution de la solution donnée.
    def evaluation_solution(self, seq):
        n = N # Initialise un petit n qui prend le nombre de clients.
        solution_traduite = self.traduireSequence(seq)   

        for client in clients:
            nbi = 0 # Nombre d'ingredients que le client aime, dans la solution.
            ok = True
            for ingredient in solution_traduite:
                if (ingredient in client.ingredient_aimes):
                    nbi +=1
                if (ingredient in client.ingredient_detestes): 
                    ok = False
            # On vérifie que le client a tous les ingredients qu'il aime et aucun qu'il n'aime pas.
            if (not(ok and (nbi == client.nb_aimes))):
                n-=1 # Sinon on retire le client.

        return n
    
    def getSolutionOptimale(self):
        i = 0
        while i < self.Imax:
            seq_candidate = self.genereVoisin()
            nb_clients_sol_candidate = self.evaluation_solution(seq_candidate)

            if self.nb_clients_sol_courante <= nb_clients_sol_candidate:
                self.nb_clients_sol_courante = nb_clients_sol_candidate
                self.solutionCourante = seq_candidate
            else:
                probaTiree = rd.random()
                dE = self.nb_clients_sol_courante - nb_clients_sol_candidate
                print("proba tirée =",probaTiree)
                print("dE",dE)
                print("exp(x) = ",np.exp(-dE/self.T))
                if probaTiree < np.exp(-dE/self.T):
                    self.solutionCourante = seq_candidate
                    self.nb_clients_sol_courante = nb_clients_sol_candidate

            # Abaissement de la température suivant une loi exponentielle.
            if (i % 5 == 0):
                self.T = self.T * 0.9
            i+=1
        return self.traduireSequence(self.solutionCourante)
    
    def is_accepted(Xca,Xco,temperature):
        proba = np.exp((Xca-Xco)/temperature)
        test = rd.uniform(0.0,1.0)
        return proba > test

N = 0 # Nombre de clients
Imax = 0 # Nombre d'ingredients

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
            ingredients.add_ingredient(ligne_1[j])
            ingredients.ingredient_is_liked(ligne_1[j])

        # Ingrédients mal aimés.
        ligne_2 = fichier.readline().strip().split()
        nb_aliments_destes = int(ligne_2[0])
        ingredients_detestes = ligne_2[1:]

        for j in range(1, len(ligne_2)):
            # On ignore le premier élément de la ligne.
            ingredients.add_ingredient(ligne_2[j])

        # Crée un nouveau client avec les informations.
        client = Client(ingredients_aimes,ingredients_detestes)
        clients.append(client)

def taille_solution_initiale():
    p = np.linspace(1, 0, len(ingredients.ingredients), dtype=float)
    p = p / np.sum(p)
    return np.random.choice(range(1, len(ingredients.ingredients) + 1), p=p)

# Génération d'une solution initiale.
# On demande à l'objet de la classe Ingredients, de renvoyer les ingredients,
# les plus appréciés. 
# Renvoie une séquence :
seq_initiale = ingredients.get_meilleurs_ingredients(taille_solution_initiale())

# Algorithme du recuit simulé.
algo_recuit = RecuitSimule(seq_initiale,ingredients)
sol = algo_recuit.getSolutionOptimale()

tab = []
ok = True
for elem in sol:
    if elem in tab:
        print("UN DOUBLON !!!! à l'ingrédient : ", elem)
        ok = False
        break
    else:
        tab.append(elem)

if (ok):
    with open("resultat.txt", 'w') as fichier:
        for element in sol:
            fichier.write(str(element) + '\n')
        fichier.write("La valeur de la solution = " + str(algo_recuit.nb_clients_sol_courante))

