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
	i = ord(word[0])-97 
	t = np.log(pi[i])

	for ch in word[1:]:
		j = ord(ch)-97
		t += np.log(M[i,j])
		i=j

	return t

#function to get log probability of a sentence occuring

def get_sequence_prob(words):
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
	new_msg = new_msg.join(coded_msg)		#joins elements of a list to make it to a string

	return new_msg


original_message = "I then lounged down the street and found,
as I expected, that there was a mews in a lane which runs down
by one wall of the garden. I lent the ostlers a hand in rubbing
down their horses, and received in exchange twopence, a glass of
half-and-half, two fills of shag tobacco, and as much information
as I could desire about Miss Adler, to say nothing of half a dozen
other people in the neighbourhood in whom I was not in the least
interested, but whose biographies I was compelled to listen to.
"

encoded_msg = encode(original_message)




# def getKey(ch,d):									#mini function to get keys from values of a dictionary
# 	for key,value in d.items():
# 		if ch==value:
# 			return key


# def decode(msg,d):

# 	decoded_msg = []

# 	for ch in msg:

# 		decoded_character = ch
# 		if ch in d.values():
# 			decoded_character = getKey(ch,d)

# 		decoded_msg.append(decoded_character)

# 	final_msg = ""
# 	final_msg = final_msg.join(decoded_msg)

# 	return final_msg

def decode(msg, word_map):
  decoded_msg = []
  for ch in msg:
    decoded_ch = ch # could just be a space
    if ch in word_map:
      decoded_ch = word_map[ch]
    decoded_msg.append(decoded_ch)

  return ''.join(decoded_msg)

#MAKING THE EVOLUTIONARY ALGORITHM



# this is our initialization point
dna_pool = []
for _ in range(20):

  	dna = list(string.ascii_lowercase)				#make a list of lowercase alphabets
  	random.shuffle(dna)								#shuffle them and append them to dnapool list	
  	dna_pool.append(dna)

def evolve_offspring(dna_pool, n_children):

  # make n_children per offspring
  	offspring = []

  	for dna in dna_pool:
  		for _ in range(n_children):
  			copy = dna.copy()
  			j = np.random.randint(len(copy))		#chose a random index from the list
  			k = np.random.randint(len(copy))
  			tmp = copy[j]
  			copy[j] = copy[k]
  			copy[k] = tmp
  			offspring.append(copy)
      		
      		
      		
      		

      		
      											
      		

  	return offspring + dna_pool	

      							#join both lists together


    	
#working the algo

num_iters = 1000
scores = np.zeros(num_iters)
best_dna = None
best_map = None
best_score = float('-inf')

for i in range(num_iters):
  	if i > 0:
  		dna_pool = evolve_offspring(dna_pool, 3)		#if more than 1st iter, use function to get offsprings
   
    	

  
  	dna2score = {}			#initialize dictionary to calculate score for each dna

  	for dna in dna_pool:
  		current_map = {}			#makes a current map 
  		for k, v in zip(list1, dna):
  			current_map[k] = v

  		decoded_message = decode(encoded_msg, current_map)
  		score = get_sequence_prob(decoded_message)
  		dna2score[''.join(dna)] = score 			#since dictionary key has to be stored as a string
  		if score > best_score:
  			best_dna = dna
  			best_map = current_map
  			best_score = score
      		
  	scores[i] = np.mean(list(dna2score.values()))	#average score of DNA list for this generation
  	sorted_dna = sorted(dna2score.items(), key=lambda x: x[1], reverse=True)
  	dna_pool = [list(k) for k, v in sorted_dna[:5]]
      		
    	
decoded_mesg= decode(encoded_msg, best_map)
print(decoded_mesg)

    	
      	
    	
    	
      		

    	


    
    
  	