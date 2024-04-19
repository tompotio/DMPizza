import sys
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
    def est_satisfait(self,solution):
        for ingredient_deteste in self.ingredient_detestes:
            if ingredient_deteste in solution:
                return False
        if self.ingredient_aimes.issubset(solution):
            return True
        return False
class enumeration:
    def __init__(self) -> None:
        self.solution = []
        self.client = []
        self.nbclient = 0
        self.ingredients = {}
        self.scoreMax = 0
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
            self.nbClient = N
            self.generate_solution()
            self.solution = sorted(self.solution, key=lambda x: x.get_score(),reverse=True)[:250]
            print("meilleurs solution", self.solution[0].get_solution(),self.solution[0].get_score())
            
            self.scoreMax = self.solution[0].get_score()
   
    def generate_solution(self):
        neededDigits = len(self.ingredients)
        unique_lists = set()
        formatstr = "0:0" +str(neededDigits)+"b"
        string ='{' + formatstr + '}' 
        for i in range(pow(2,len(self.ingredients))):
            recette = [int(i) for i in list(string.format(i))]
            vecteur = self.calculer_score(recette)
            print(vecteur.get_solution(),vecteur.get_score())
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
enumerationSolution = enumeration()
enumerationSolution.init(sys.argv[1])