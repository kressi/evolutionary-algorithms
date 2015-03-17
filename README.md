Evolution Algorithms
====================

Lecture: Comuptatianal Intelligence - ZHAW
Lecturer: Dr. Carsten Franke
Topic: i) Einkriterielle Evoulutionäre Algorithmen
          - Genetic Algorithm
          - Evolution Strategy
      ii) Mehrkriterielle Evolutionäre Algorithmen
          - Vector Evaluated Genetic Algorithm (VEGA)


Author: Michael Kressibucher


Problem solved with algorithms
------------------------------
Height of Cylinder h:   0 <= h <= 31
Diameter of Cylinder d: 0 <= d <= 31

Volume v:  pi*d^2*h/4 >= 300
Surface s: pi*d^2/2 + pi*d*h

-> By a genetic algorithm, diameter and height
   have to be determined, such that the surface
   of the cylinder is minimal.


Context Parameters
------------------
- Object Properties (Encoding of Problem): o_k
- Strategy Parameters (Mutation, Recombination, Selection): s_k
- Fitness: F(o_k)
- Size of Population at Time t: μ = |P_(t,μ)|
- Number of Descendants: λ
- Number of Parents at recombination: ρ
- Max Number of Generations an Individual lives: κ
- k: index of individual

Genetic Algorithm 
-----------------
(Chromosome Representation GA)
- Individuals a_k = (o_k, F(o_k))
- μ = λ
- κ = 1
- s_k constant


Binary Encoding
---------------
Phenotype: Individual, Creatur, Properties ∈ {l, u}^n , l, u: lower and upper bound of interval of n parameters
Genotype: {0,1}^l, (l: length of binary encoding)
