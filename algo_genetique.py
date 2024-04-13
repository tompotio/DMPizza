
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
class Client: 
    def __init__(self, ingredients_aimes, ingredients_detestes):
        self.ingredient_aimes = ingredients_aimes
        self.nb_aimes = len(ingredients_aimes)
        self.ingredient_detestes = ingredients_detestes
        self.nb_detestes = len(ingredients_detestes)
    def exist(self,aliment,i):
        j = 0
        
        for ingredient in self.ingredient_aimes:
            if ingredient == aliment:
                self.ingredient_aimes[j]=i
            j+=1
        j=0
        for ingredient in self.ingredient_detestes:
            if ingredient == aliment:
                self.ingredient_detestes[j]=i
            j+=1   
    def tailleAime(self):
        return len(self.ingredient_aimes)
    def aime(self,i):
        if i in self.ingredient_aimes:
            return True
        else:
            return False
    def deteste(self,i):
        if i in self.ingredient_detestes:
            return True
        else:
            return False
class algorithme_genetique:
    def __init__(self) -> None:
        self.solution = []
        self.client = []
        self.nbclient = 0
        self.ingredients = {}
        self.taille_population = 0
        self.nb_generation = 50
        self.nbTour = 10
        self.generation = []
        self.nb_croisement = 10
        self.chance_mutation = 0.2
    def init(self,fichier):
        with open(fichier,'r') as fichier: 
            # Nombre de clients.
            N = int(fichier.readline())

            # Parcours des lignes deux par deux.
            for i in range((N//2)):
                ligne_aime = fichier.readline().strip().split()
                aliments_aime = []
                
                for j in range(int(ligne_aime[0])):
                    aliments_aime.append(ligne_aime[j+1])
                    self.ingredients[ligne_aime[j+1]]=0
                
                ligne_deteste = fichier.readline().strip().split()
                aliments_deteste = []
                
                for j in range(int(ligne_deteste[0])):
                    aliments_deteste.append(ligne_deteste[j+1])
                    self.ingredients[ligne_deteste[j+1]]=0
               
                client = Client(aliments_aime,aliments_deteste)    
                self.client.append(client)
            self.traduire_aliment_client()
            self.taille_population = 150
            self.nbSolutionInitial = min(10000,pow(2,len(self.ingredients)))
            self.nbClient = N
            self.generate_solution(self.nbSolutionInitial)
    def generate_sequence(self,neededDigits):
        sequence = []
        for i in range(neededDigits):
            sequence.append(randint(0, 1))
        return sequence
    def generate_solution(self,taille_population):
        neededDigits = len(self.ingredients)
        for i in range(taille_population):
            sequence =self.generate_sequence(neededDigits)
            vecteur = self.calculer_score(sequence)
            self.solution.append(vecteur)      
    def calculer_score(self,solutions):
        score = self.nbClient
        for client in self.client:
            i=0
            nb_aime=0
            deteste = False
            for ingredient in solutions:
                if client.deteste(i) and ingredient==1:
                    deteste = True
                    break
                if client.aime(i) and ingredient==1:
                    nb_aime+=1
                
            if nb_aime != client.tailleAime() or deteste:
                    i+=1
                    score-=1      
        return vecteur(solutions,score)     
    def traduire_aliment_client(self):
        i = 0
        for key in self.ingredients.keys():
            for client in self.client:
               client.exist(key,i) 
               i+=1
    def tournamentSelection(self):
        populationSelection = [] # Création de notre variable de sortie
        for i in range(self.taille_population):
            populationRandom = [] # Création de notre liste de sélection aléatoire
    
            for j in range(self.nbTour):
                populationRandom.append(self.solution[randrange(len(self.solution))]) # On choisit aléatoirement des 
    # individus de la génération
            
            populationRandom = sorted(populationRandom, key=lambda x: x.get_score()) # Trier en fonction de la valeur du fitness
            populationSelection.append(populationRandom[0]) # Ajouter à notre variable de sortie l'individu ayant le 
    # meilleur fitness
    
        populationSelection = sorted(populationSelection, key=lambda x: x.get_score()) # Trier en fonction du fitness
        a = populationSelection[:] # Faire une copie de la variable de sortie
        
        self.generation=a
    def croisement(self):
        enfants = []
        for i in range(self.nb_croisement+1):
            parent1 = self.generation[randrange(len(self.generation))].get_solution()
            parent2 = self.generation[randrange(len(self.generation))].get_solution()
            enfant1 = parent1[0:len(parent1)//2] + parent2[len(parent1)//2 + 1:len(parent2)-1]
            enfants.append(self.calculer_score(enfant1))
            enfant2 = parent2[0:len(parent2)//2] + parent1[len(parent2)//2 +1 : len(parent1)-1]
            enfants.append(self.calculer_score(enfant2))
        return enfants
    def mutation(self):
        for solution in self.generation:
            proba = random()
            if proba > self.chance_mutation:
                sequence = solution.get_solution()
                point_mutation = randrange(len(sequence))
                sequence[point_mutation] = 1-sequence[point_mutation]
                solution.set_solution(sequence)
    def get_optimal_solution(self):
        if len(sys.argv) != 2:
            raise TypeError("Le nombre d'arguments n'est pas valide.")
            sys.exit(1)
        filename = sys.argv[1]
        #génération de la première population
        self.init(filename)
       
        i=0
        while i<self.nb_generation:
            self.tournamentSelection()
            enfants = self.croisement()
            self.mutation()
            self.generation.extend(enfants)
            self.solution = self.generation
            i+=1
        self.solution = sorted(self.solution, key=lambda x: x.get_score())    
        print(self.solution[0].get_score(),self.solution[0].get_solution())
        
algo_genetique = algorithme_genetique()
algo_genetique.get_optimal_solution()
algo = []
thread = []
for i in range(6):
    algo.append(algo_genetique())
    thread.append(threading.Thread(target=algo[i].get_optimal_solution()))
for i in range(6):
    thread[i].start()