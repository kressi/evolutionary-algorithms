
Process Flow Evolution
======================
Initialization
- Encoding

Evaluation
- Fitness

Reproduction
- Recombination
- Mutation

Convergence
- e.g. Fixed Number of Generations


Context Parameters
==================
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
===============
Phenotype: Individual, Creatur, Properties ∈ {l, u}^n , l, u: lower and upper bound of interval of n parameters
Genotype: {0,1}^l, (l: length of binary encoding)
