import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import string
import random
import re
import requests
import os
import textwrap

#MAKING THE RANDOM CIPHER

list1 = list(string.ascii_lowercase)		#creating string of 26 alphabets in alphabetical order
list2 = list(string.ascii_lowercase)
random.shuffle(list2)						#shuffling list 2
true_mapping = dict(zip(list1,list2))		#creating an original mapping dictionary using zip(key,values)

# print(true_mapping)

#CREATING THE LANGUAGE MODEL

#initialize markov matrix
M = np.ones(26,26)							#initialized as one to implement the concept of add-one-smoothing

#initialize count of each letter as a vector
pi = np.zeros(26)

#function to update markov matrix

def update_transition(ch1, ch2):
	i = ord(ch1)-97					#ord converts character to ascii value now 'a' = 97, 97-97=0, this means a has first row
	j = ord(ch2)-97

	M[i, j]+=1						#updates markov matrix whenever the group of words occur

#function to update count of individual vectors

def update_pi(ch1):
	i = ord(ch1)-97
	pi[i]+=1

#function to get log probability of word/token

def log_likelyhood_of_word(word)
	i = word[0]-97 
	t = np.log(pi[i])

	for ch in word[1:]:
		j = word[ch]-97
		t += np.log(M[i,j])
		i=j

	return t

#function to get log probability of a sentence occuring

def log_likelyhood_of_sentence(words):
	l = words.split(' ')
	total =0
	for x in l:
		total += log_likelyhood_of_word(x)

	return total

#CREATING THE MARKOV MODEL




