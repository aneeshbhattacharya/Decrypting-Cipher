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
M = np.ones((26,26))							#initialized as one to implement the concept of add-one-smoothing

#initialize count of each letter as a vector
pi = np.zeros(26)

#function to update markov matrix

def update_transition(ch1, ch2):
	i = ord(ch1)-97					#ord converts character to ascii value now 'a' = 97, 97-97=0, this means a has first row
	j = ord(ch2)-97

	M[i,j]+=1						#updates markov matrix whenever the group of words occur

#function to update count of individual vectors

def update_pi(ch1):
	i = ord(ch1)-97
	pi[i]+=1

#function to get log probability of word/token



def log_likelyhood_of_word(word):
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

#Data Processing:


file_to_edit =  open('moby_dick.txt')


#List to replace all non-alpha characters/special characters
regex = re.compile('[^a-zA-Z]')

for line in file_to_edit:
	line = line.rstrip()		#this strips white space

	if line:					#this condition says that if line is not blank then work
		line = regex.sub(' ',line) #replace all non alpha characters with space

		tokens = line.lower().split()	#make a list of lines

		for token in tokens:

			ch0 = token[0]
			#update vector
			update_pi(ch0)

			for ch1 in token[1:]:				#update probabilities of other letters occuring when first has occured
				update_transition(ch0,ch1)
				ch0 = ch1

#converting the data of matrices into probabilities:
pi /= pi.sum()
M /= M.sum(axis=1, keepdims=True)	#each row of m should sum to 1, this means every number of the row should be divided by their respective column sums.


#function to encode the message

def encode(msg):					#takes msg as a string as a whole

	msg = msg.rstrip()
	msg = regex.sub(' ', msg)
	msg  = msg.lower()

	coded_msg = []			#start a list for the coded message to be appended
	for ch in msg:

		encoded_character = ch 		#This is because the character could just be a space

		if ch in true_mapping.keys():
			encoded_character = true_mapping[ch]
			
		coded_msg.append(encoded_character)

	new_msg =""
	new_msg = new_msg.join(coded_msg)

	return new_msg














