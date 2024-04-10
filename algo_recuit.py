import random as rd 
import sys 

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

# Initialisation.
N = 0
T0 = 1000000
tau = 1e4
beta = 1e-1
k = 0

# Liste des ingrédients et des clients.
ingredients = Ingredients()
clients = []

# On vérifie le nombre d'arguments passé en ligne de commance.
if len(sys.argv) != 2:
    raise TypeError("Le nombre d'arguments n'est pas valide.")
    sys.exit(1)

filename = sys.argv[1]

# On le fichier pour récupérer les informations.
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
        for j in range(len(ligne_1)):
            ingredients.add_ingredient(ligne_1[j])
            ingredients.ingredient_is_liked(ligne_1[j])

        # Ingrédients mal aimés.
        ligne_2 = fichier.readline().strip().split()
        nb_aliments_destes = int(ligne_2[0])
        ingredients_detestes = ligne_2[1:]

        for j in range(len(ligne_2)):
            ingredients.add_ingredient(ligne_2[j])

        # Crée un nouveau client avec les informations.
        client = Client(ingredients_aimes,ingredients_detestes)
        clients.append(client)

        # Print test.
        print("Client {i+1}:")
        print("Ingrédients aimés : ",ingredients_aimes)
        print("Ingredients mal aimés : ", ingredients_detestes)

# Calcul de la fonction d'évalution de la solution donnée.
def fonction_evaluation(solution):
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

solution = ["mushrooms", "tomatoes", "cheese", "peppers"]

print("la solution a une valeur = " + str(fonction_evaluation(solution)))