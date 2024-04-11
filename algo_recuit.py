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

    def __init__(self,solution,ingredients) -> None:
        self.solution = solution
        self.solutionCourante = solution
        self.ingredients = ingredients
        self.nb_clients_sol_courante = self.evaluation_solution(solution)
        self.Imax = len(ingredients.ingredients)

        # Paramètres variants.
        self.T0 = self.Imax * 2
        self.T = self.T0
        self.Tmin = self.Imax
        self.tau = 1e4
        self.beta = 1e-4

    def generateNeighbor(self):
        seq = self.solutionCourante
        length = len(seq)
        start = 0
        end = length
        if (length >= 3):
            start = rd.randint(0, length - 2)  # Point de départ aléatoire
            end = rd.randint(start+1, length - 1)
        seq[start:end + 1] = reversed(seq[start:end + 1])
        return seq
    
    # Calcul de la fonction d'évalution de la solution donnée.
    def evaluation_solution(self, solution):
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
    
    def find_optimal_solution(self):
        i = 0
        while self.T > self.Tmin:
            solution_candidate = self.generateNeighbor()
            nb_clients_sol_candidate = self.evaluation_solution(solution_candidate)

            if self.nb_clients_sol_courante < nb_clients_sol_candidate:
                self.nb_clients_sol_courante = nb_clients_sol_candidate
                self.solutionCourante = solution_candidate
            else:
                dE = self.nb_clients_sol_courante - nb_clients_sol_candidate
                if self.beta < np.exp(-dE/self.T):
                    self.solutionCourante = solution_candidate
                    self.nb_clients_sol_courante = nb_clients_sol_candidate

            # Abaissement de la température suivant une loi exponentielle.
            self.T = self.T0 * np.exp(-i/self.tau)
            i+=1
        return self.solutionCourante
    
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

        # Print test.
        #print(f"Client {i+1}:")
        #print("Ingrédients aimés : ",ingredients_aimes)
        #print("Ingredients mal aimés : ", ingredients_detestes)

def taille_solution_initiale():
    p = np.linspace(1, 0, len(ingredients.ingredients), dtype=float)
    p = p / np.sum(p)
    return np.random.choice(range(1, len(ingredients.ingredients) + 1), p=p)

# Génération d'une solution initiale.
# On demande à l'objet de la classe Ingredients, de renvoyer les ingredients,
# les plus appréciés. 
# On demande un nombre 
solution_initiale = ingredients.get_meilleurs_ingredients(taille_solution_initiale())

# Algorithme du recuit simulé.
algo_recuit = RecuitSimule(solution_initiale,ingredients)
sol = algo_recuit.find_optimal_solution()
nb =0
while((algo_recuit.nb_clients_sol_courante < 5) and (nb < 1000)):
    sol = algo_recuit.find_optimal_solution()
    nb+=1

print("nb = ", nb)
print("solution = ",sol)
print("val sol =",algo_recuit.nb_clients_sol_courante)