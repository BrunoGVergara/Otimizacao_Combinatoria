# INF-05010 Otimização Combinatória

# Bruno Grohs Vergara 00324256
# Erick Larratéa Knoblich 00324422

from Functions import *
import random, os

# ----------------------------------------------------------------------------------------------------

os.system('cls')
random.seed(-5508469125140711083)

for i in range(1, 11):

  P, PN, S, SN, D, H = ReadFile(i)
  n, pivot, crossoverRate, mutationRate, objectives = 50, 0, 0.9, 0.775, []
  population = GenerateStartingPopulation(P, S, D, H, n, PN)
  bestSolution = BestSolution(population, P)
  bestObjective = CalculateObjetive(bestSolution, P)
  print(f"File #{i}:\n")

  while pivot < 50:

    newPopulation = []

    while len(newPopulation) < len(population):

      chromossome1, chromossome2 = Selection(P, population)

      if random.random() < crossoverRate:

        offspring = Crossover(chromossome1, chromossome2)

      else:

        offspring = chromossome1 if CalculateObjetive(chromossome1, P) <= CalculateObjetive(chromossome2, P) else chromossome2

      if random.random() < mutationRate:

        offspring = Mutation(offspring)

      if ValidateSolution(P, S, D, H, offspring):

        newPopulation.append(offspring)

    newPopulationBestObjective = CalculateObjetive(BestSolution(newPopulation, P), P)

    if newPopulationBestObjective < bestObjective:

      bestObjective = newPopulationBestObjective
      print(bestObjective)

    else:

      pivot += 1

    population = newPopulation
    
  objectives.append(bestObjective)
  print()