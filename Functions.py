from Classes import *
import random, math

def ReadFile(pivot: int) -> ([Professor], int, [Student], int, float, int):

  content = open("file{}.csv".format(pivot), "r").readlines()
  PN, SN = content[0].split(",")
  PN, SN = int(PN), int(SN.strip())
  H, D = content[1].split(",")
  H, D = int(H), float(D.strip())
  P, S = [], []

  for i in range(2, 2 + PN):

    id, x, y, s = content[i].split(",")
    x, y, s = float(x), float(y), int(s.strip())
    P.append(Professor(x, y, s))

  for j in range(2 + PN, 2 + PN + SN):
    
    id, x, y, h = content[j].split(",")
    x, y, h = float(x), float(y), int(h.strip())
    S.append(Student(x, y, h, 0))

  return P, PN, S, SN, D, H

def CalculateObjetive(Xi: [int], professors: [Professor]) -> int:

  return sum(professors[i].s * Xi[i] for i in range(len(Xi)))

def BestSolution(population: [[int]], professors: [Professor]) -> [int]:

  objectiveA = CalculateObjetive(population[0], professors)
  bestChromossome = population[0]

  for chromossome in population[1:]:

    objectiveB = CalculateObjetive(chromossome, professors)

    if (objectiveB < objectiveA):

      objectiveA = objectiveB
      bestChromossome = chromossome

  return bestChromossome

def ValidateSolution(professors: [Professor], students: [Student], distance: float, hours: int, Xi: [int]) -> bool:

  i = 0

  for x in Xi:

    if x == 0:

      continue

    for student in students:

      if math.sqrt((professors[i].x - student.x) ** 2 + (professors[i].y - student.y) ** 2) <= distance:

        student.j = 1

    i += 1

  hoursSum = sum(j.h * j.j for j in students)

  for student in students:

    student.j = 0
  
  return True if hoursSum >= hours else False

def GenerateStartingPopulation(professors: [Professor], students: [Student], distance: float, hours: int, n: int, numberOfProfessors: int) -> [[int]]:  

  population, chromossome = [], []

  for i in range(n):  

    for j in range(numberOfProfessors):

      chromossome.append(random.randint(0, 1))
    
    if ValidateSolution(professors, students, distance, hours, chromossome):

      population.append(chromossome)

    else:

      i -= 1

    chromossome = []
  
  return population

def Selection(professors: [Professor], population: [[int]]) -> ([int], [int]):

  k = random.randint(2, round(0.25 * len(population)))
  tournament, chromossome1, chromossome2 = [], [], []

  for i in range(k):

    tournament.append(population[random.randint(0, len(population) - 1)])

  chromossome1, chromossome2 = tournament[0], tournament[1]

  if CalculateObjetive(chromossome2, professors) < CalculateObjetive(chromossome1, professors):

    chromossome1, chromossome2 = chromossome2, chromossome1

  for i in range(2, len(tournament)):

    if CalculateObjetive(tournament[i], professors) < CalculateObjetive(chromossome1, professors):

      chromossome1 = tournament[i]

    elif CalculateObjetive(tournament[i], professors) < CalculateObjetive(chromossome2, professors):

      chromossome2 = tournament[i]
  
  return chromossome1, chromossome2

def Mutation(Xi: [int]) -> [int]:

  K = []

  for i in range(random.randint(1, 0.01 * len(Xi))):

    K.append(random.randint(0, len(Xi) - 1))

  for k in K:

    Xi[k] = 1 if Xi[k] == 0 else 0

  return Xi

def Crossover(chromossome1: [int], chromossome2: [int]) -> [int]:

  pivot1 = random.randint(0, len(chromossome1) - 1)

  if pivot1 == 0:

    chromossome = chromossome1[0 : pivot1] + chromossome2[pivot1 :]

  else:

    chromossome = chromossome2[0 : pivot1] + chromossome1[pivot1 :]

  return chromossome