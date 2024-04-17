
from random import * 
from math import *
import sys 
import threading

class vecteur:
    def __init__(self,solution,score) -> None:
        self.solution = solution
        self.score = score
    def get_solution(self):
        return self.solution
    def set_solution(self,solution):
        self.solution = solution
    def get_score(self):
        return self.score
    def set_score(self,score):
        self.score=score
    
class Client: 
    def __init__(self, ingredients_aimes, ingredients_detestes):
        self.ingredient_aimes = ingredients_aimes
        self.nb_aimes = len(ingredients_aimes)
        self.ingredient_detestes = ingredients_detestes
        self.nb_detestes = len(ingredients_detestes)
    def exist(self,aliment,i):
        if aliment in self.ingredient_aimes:
            self.ingredient_aimes.remove(aliment)
            self.ingredient_aimes.add(i)
        if aliment in self.ingredient_detestes:
            self.ingredient_detestes.remove(aliment)
            self.ingredient_detestes.add(i)
        
    def showIngredient(self):
        print(self.ingredient_aimes,self.ingredient_detestes)
    def est_satisfait(self,solution):
        for ingredient_deteste in self.ingredient_detestes:
            if ingredient_deteste in solution:
                return False
        if self.ingredient_aimes.issubset(solution):
            return True
        return False
class algorithme_genetique:
    def __init__(self,SolutionInitial = []) -> None:
        self.solution = []
        self.client = []
        self.nbclient = 0
        self.ingredients = {}
        self.taille_population = 100
        self.nb_generation = 100
        self.nbTour = 5
        self.generation = []
        self.nb_croisement = 200
        self.chance_mutation = 0.05
        self.solutionFinal = SolutionInitial
        self.scoreFinal = 0
    def get_score_final(self):
        return self.scoreFinal
    def get_solution_final(self):
        return self.solutionFinal
    def init(self,fichier):
        with open(fichier,'r') as fichier: 
            # Nombre de clients.
            N = int(fichier.readline())
           
            # Parcours des lignes deux par deux.
            for i in range((N)):
               
                ligne_aime = fichier.readline().strip().split()
                aliments_aime = set()
                
                for j in range(int(ligne_aime[0])):
                    aliments_aime.add(ligne_aime[j+1])
                    self.ingredients[ligne_aime[j+1]]=0
                
                ligne_deteste = fichier.readline().strip().split()
                aliments_deteste = set()
                
                for j in range(int(ligne_deteste[0])):
                    aliments_deteste.add(ligne_deteste[j+1])
                    self.ingredients[ligne_deteste[j+1]]=0
                
                client = Client(aliments_aime,aliments_deteste)    
                self.client.append(client)
            self.traduire_aliment_client()
            self.taille_population = 150
            self.nbSolutionInitial = 1000000 if len(self.ingredients) > 13 else pow(2,len(self.ingredients))
            self.nbClient = N
            self.generate_solution(self.nbSolutionInitial)
            self.solution = sorted(self.solution, key=lambda x: x.get_score(),reverse=True)[:250]
   
    def generate_solution(self,taille_population):
        neededDigits = len(self.ingredients)
        unique_lists = set()
        while len(unique_lists) < self.nbSolutionInitial:
            new_list = [choice([0, 1]) for _ in range(neededDigits)]
            new_tuple = tuple(new_list)
            if new_tuple not in unique_lists:
                unique_lists.add(new_tuple)
                vecteur = self.calculer_score(new_list)
                self.solution.append(vecteur)
    def calculer_score(self,solutions):
        score = self.nbClient
        ingredients = set()
        i=0
        #on considère que les aliments sur la pizza
        for ingredient in solutions:
            if ingredient == 1:
                ingredients.add(i)
            i+=1
       
        for client in self.client:
            if not client.est_satisfait(ingredients):
                score -= 1
        
        return vecteur(solutions,score)     
    def traduire_aliment_client(self):
        i = 0
        for key in self.ingredients.keys():
            for client in self.client:
               client.exist(key,i) 
            i+=1
    def traduire_solution(self):
        i = 0
        ingredient_list = []
        
        for ingredients in self.ingredients.keys():
            if self.solutionFinal[i] == 1:
                ingredient_list.append(ingredients)
            i+=1
        return ingredient_list
    def tournamentSelection(self):
        populationSelection = [] # Création de notre variable de sortie
        for i in range(self.taille_population):
            populationRandom = [] # Création de notre liste de sélection aléatoire
            for j in range(self.nbTour):
                populationRandom.append(self.solution[randrange(len(self.solution))]) # On choisit aléatoirement des 
    # individus de la génération
            
            populationRandom = sorted(populationRandom, key=lambda x: x.get_score(),reverse=True) # Trier en fonction de la valeur du fitness
            populationSelection.append(populationRandom[0]) # Ajouter à notre variable de sortie l'individu ayant le 
    # meilleur fitness
    
        populationSelection = sorted(populationSelection, key=lambda x: x.get_score(),reverse=True) # Trier en fonction du fitness
        a = populationSelection[:] # Faire une copie de la variable de sortie
        self.generation=a
    def getMeileurSolution():
        return self.solution[:50]
    def croisement(self):
        enfants = []
        for i in range(self.nb_croisement):
            parent1 = self.generation[randrange(len(self.generation))].get_solution()
            parent2 = self.generation[randrange(len(self.generation))].get_solution()

            longueur_tab1 = len(parent1)
            longueur_tab2 = len(parent2)
    
            premiere_moitie_tab1 = parent1[:longueur_tab1 // 2]
            deuxieme_moitie_tab1 = parent1[longueur_tab1 // 2:]
            premiere_moitie_tab2 = parent2[:longueur_tab2//2]
            deuxieme_moitie_tab2 = parent2[longueur_tab2 // 2:]
            

            enfant1 = premiere_moitie_tab1 + deuxieme_moitie_tab2
            enfants.append(self.calculer_score(enfant1))
            enfant2 = premiere_moitie_tab2 + deuxieme_moitie_tab1
            enfants.append(self.calculer_score(enfant2))
          
        self.generation.extend(enfants)
        self.mutation()
        self.generation = populationSelection = sorted(self.generation, key=lambda x: x.get_score(),reverse=True)
    def mutation(self):
        for solution in self.generation:
            proba = random()
            if proba > self.chance_mutation:
                sequence = solution.get_solution()
                point_mutation = randrange(len(sequence))
                sequence[point_mutation] = 1-sequence[point_mutation]
                vecteur = self.calculer_score(sequence)
                solution.set_solution(sequence)
                solution.set_score(vecteur.get_score())
    def get_optimal_solution(self):
        
        if len(sys.argv) != 2:
            raise TypeError("Le nombre d'arguments n'est pas valide.")
            sys.exit(1)
        
        filename = sys.argv[1]
        #génération de la première population
        print("debut de l'algorithme génétique")
        self.init(filename)
        print("premiere génération créée")
        i=0
        while i<self.nb_generation:
            print(i,"ème génération")
            self.tournamentSelection()
            enfants = self.croisement()
          
            self.solution = self.generation
            i+=1

        self.solution = sorted(self.solution, key=lambda x: x.get_score(),reverse=True)    
        self.solutionFinal = self.solution[0].get_solution()
        self.scoreFinal = self.solution[0].get_score()
        print("score:",self.get_score_final())
        print("solution:",self.traduire_solution())
algo = algorithme_genetique()
algo.get_optimal_solution()
while algo.get_score_final() < 1500:
    algo = algorithme_genetique(algo.getMeileurSolution())
    algo.get_optimal_solution()

with open("resultats/genetique/elabore/resultat.txt", 'w') as fichier:
    ingredient = algo.traduire_solution()
    fichier.write(str(len(ingredient)))
    fichier.write(" ")
    for element in ingredient:
        fichier.write(element + " ")
"""
algo = []
thread = []
for i in range(6):
    algo.append(algorithme_genetique())
    thread.append(threading.Thread(target=algo[i].get_optimal_solution))
for t in thread:
    print("thread",i,"lancé")
    t.start()   
for t in thread:
    t.join()
    print("fini")
bestSolution =  sorted(algo, key=lambda x: x.get_score_final(),reverse=True)
print(bestSolution[0].get_score_final(),bestSolution[0].traduire_solution())

with open("resultats/genetique/difficile/resultat.txt", 'w') as fichier:
    ingredient = bestSolution[0].traduire_solution()
    fichier.write(str(len(ingredient)))
    fichier.write(" ")
    for element in ingredient:
        fichier.write(element + " ")
        """
