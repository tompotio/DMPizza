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

    def add_ingredient(self, ingredient):
        if(not self.ingredients in self.ingredients.values()): 
            self.ingredients[ingredient] = 0

    # Incrémente le compteur de client qui aime cet ingrédient.
    def ingredient_is_liked(self, ingredient):
        self.ingredients[ingredient] += 1

    def get_meilleurs_ingredients(self, n):
        ordre_decroissant = sorted(self.ingredients.items(), key=lambda x: x[1], reverse=True)
        return [ingredient for ingredient, _ in ordre_decroissant[:n]]
    
class RecuitSimule:
    def __init__(self,solution,temperature,ingredients) -> None:
        self.solution = solution
        self.temperature = temperature
        self.ingredients = ingredients

    def generateNeighbors(seq):
        length = len(seq)
        start = rd.randint(0, length - 2)  # Point de départ aléatoire
        end = rd.randint(start+1, length - 1)
        seq[start:end + 1] = reversed(seq[start:end + 1])
        return seq
    
    def find_optimal_solution():
        while T > Tmin:
            solution_candidate = mouvement()
            nb_clients_sol_candidate = evaluation_solution(solution_candidate)

            if nb_clients_sol_courante < nb_clients_sol_candidate:
                nb_clients_sol_courante = nb_clients_sol_candidate
            else: 
                dE = nb_clients_sol_courante - nb_clients_sol_candidate
                

            # Décroissement de la température suivant une loi exponentielle.
            T = T0 * np.exp(-t/tau)
    
    def is_accepted(Xca,Xco,temperature):
        proba = exp((Xca-Xco)/temperature)
        test = rd.uniform(0.0,1.0)
        return proba>test

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

        # Print test.
        #print(f"Client {i+1}:")
        #print("Ingrédients aimés : ",ingredients_aimes)
        #print("Ingredients mal aimés : ", ingredients_detestes)

Imax = len(ingredients.ingredients)

# Calcul de la fonction d'évalution de la solution donnée.
def evaluation_solution(solution):
    n = N # Initialise un petit n qui prend le nombre de clients.

    for client in clients:
        nbi = 0 # Nombre d'ingredients que le client aime, dans la solution.
        ok = True
        for ingredient in solution:
            if (ingredient in client.ingredient_aimes):
                nbi +=1
            if (ingredient in client.ingredient_detestes): 
                ok = False 
        # On vérifie que le client a tous les ingredients qu'il aime et aucun qu'il n'aime pas.
        if (not(ok and (nbi == client.nb_aimes))):
            n-=1 # Sinon on retire le client.

    return n

def taille_solution_initiale():
    p = np.linspace(1, 0, Imax, dtype=float)
    p = p / np.sum(p)
    return np.random.choice(range(1, Imax + 1), p=p)

def exp(delta, T):
    return math.exp(-delta/T)

def mouvement():
    return

# Génération d'une solution initiale.
# On demande à l'objet de la classe Ingredients, de renvoyer les ingredients,
# les plus appréciés. 
# On demande un nombre 
solution_initiale = ingredients.get_meilleurs_ingredients(taille_solution_initiale())
solution_courante = solution_initiale
nb_clients_sol_courante = evaluation_solution(solution_courante)

print(solution_initiale)

# Paramètres variants.
T0 = Imax * 2
T = T0
Tmin = 1e-1
tau = 1e4
beta = 1e-4
t = 0

# Algorithme du recuit simulé.
algo_recuit = RecuitSimule()









