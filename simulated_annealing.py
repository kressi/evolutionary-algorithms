"""
Simulated Annealing
===================

Best Result so far:

[21, 4, 10, 11, 15, 20, 19, 27, 32, 1, 12, 34, 26, 18, 29, 13, 6, 3, 16, 7, 17, 24, 9, 8, 30, 23, 14, 25, 31, 33, 2, 0, 22, 28, 5]
0        Biel
34       Neuchatel
83       Bern
116      Fribourg
253      Genf
317      Lausanne
348      Montreux
390      Martigny
422      Sion
502      Zermatt
626      Andermatt
726      Glarus
795      Zug
822      Schwyz
859      Luzern
951      Thun
981      Interlaken
1094     Brig
1222     Bellinzona
1240     Locarno
1306     Chiasso
1333     Lugano
1459     St. Moritz
1527     Davos
1585     Chur
1625     Vaduz
1691     St. Gallen
1731     Kreuzlingen
1776     Schaffhausen
1804     Winterthur
1829     Zürich
1912     Basel
1977     Aarau
1990     Olten
2028     Solothurn
2052     Biel

Distance:  2052

"""

from math import exp
from random import random, sample
from copy import copy

import simulated_annealing_data as data
from simulated_annealing_data import path_length as length
from simulated_annealing_data import path_print


BOLTZMANN = 1.3808 * 10 ** (-23)

def metropolis(E1, E0, T):
	"""Metropolis Verteilung
	"""
	return exp((E0 - E1) / (T * BOLTZMANN)) if E0 < E1 else 1

def two_opt(p1):

	p2 = copy(p1)
	
	# generate non-neighbouring permutation
	x = True
	while x:
		p = sample(range(len(p2)), 4)
		x = abs(p[0]-p[1]) == 1 or abs(p[2]-p[3]) == 1

	p2[p[0]], p2[p[1]] = p2[p[1]], p2[p[0]]
	p2[p[2]], p2[p[3]] = p2[p[3]], p2[p[2]]

	return p2


# initial solution
path = [i for i in range(len(data.CITIES))]
path_len     = length(path)
shortest     = path
shortest_len = path_len

# initial temperature
T = 3000

for _ in range(200):

	for _ in range(2000):
		
		path_new     = two_opt(path)
		path_new_len = length(path_new)

		if path_new_len < path_len \
		or metropolis(path_len, path_new_len, T) < random():

			path     = path_new
			path_len = path_new_len
			if path_len < shortest_len:
				shortest_len = path_len
				shortest     = path

	T = 0.8 * T

# show result
path_print(shortest)
print('\nDistance: ', shortest_len)

