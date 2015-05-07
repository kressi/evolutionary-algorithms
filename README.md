# Evolutionary Algorithms

**Lecture:** Comuptatianal Intelligence - ZHAW  
**Lecturer:** Dr. Carsten Franke  
**Topic:**  
- Einkriterielle Evoulutionäre Algorithmen  
  - Genetic Algorithm
  - Evolution Strategy
- Mehrkriterielle Evolutionäre Algorithmen
  - Vector Evaluated Genetic Algorithm (VEGA)

**Author:** Michael Kressibucher


## Problem solved with algorithms
Height of Cylinder h:   0 ≤ h ≤ 31  
Diameter of Cylinder d: 0 ≤ d ≤ 31  

Volume V: ![π * d² * h / 4 ≥ 300](http://mathurl.com/pqc4j8g.png)  
Surface S: ![π * d² / 2 + π * d *h](http://mathurl.com/mrsqgnw.png)  

By a genetic algorithm, diameter and height have to be determined, such that the surface of the cylinder is minimal.


## Context Parameters
- Object Properties (Encoding of Problem): ![o_k](http://mathurl.com/l2pxyl8.png)
- Strategy Parameters (Mutation, Recombination, Selection): ![s_k](http://mathurl.com/mrt835g.png)
- Fitness: ![F(o_k)](http://mathurl.com/p45qp4l.png)
- Size of Population at Time t: ![μ = |P_(t,μ)|](http://mathurl.com/m5f9k7x.png)
- Number of Descendants: λ
- Number of Parents at recombination: ρ
- Max Number of Generations an Individual lives: κ
- k: index of individual

## Genetic Algorithm
- Individuals ![a_k = (o_k, F(o_k))](http://mathurl.com/mxxd7aq.png)
- μ = λ
- κ = 1
- ![s_k](http://mathurl.com/mrt835g.png) constant

## Binary Encoding
**Phenotype:** Individual, Creatur, Properties ![∈ {l, u}^n](http://mathurl.com/mx3yovt.png) , l, u: lower and upper bound of interval of n parameters  
**Genotype:** ![{0,1}^l](http://mathurl.com/nzs2mrm.png), (l: length of binary encoding)
