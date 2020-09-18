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
	new_msg = new_msg.join(coded_msg)		#joins elements of a list to make it to a string

	return new_msg

def getKey(ch,d):									#mini function to get keys from values of a dictionary
	for key,value in d.items():
		if ch==value:
			return key


def decode(msg,d):

	decoded_msg = []

	for ch in msg:

		decoded_character = ch
		if ch in d.values():
			decoded_character = getKey(ch,d)

		decoded_msg.append(decoded_character)

	final_msg = ""
	final_msg = final_msg.join(decoded_msg)

	return final_msg

#MAKING THE EVOLUTIONARY ALGORITHM






l1 = list(string.ascii_lowercase)
l2 = list(string.ascii_lowercase)




def evolutionary_decryption(msg,first_attempt=None):
	if first_attempt ==True:

		random_mapping_dictionaries_original = list()
		random_mapping_dictionaries_new = list()
		list_to_record_orignal_likelyhood = list()
		list_to_record_new_likelyhood = list()

		dictionary_to_hold_values = {}

		for i in range(20):
			random.shuffle(l2)
			temp_mappings = dict(zip(l1, l2))								#create random dictionary mappings
			random_mapping_dictionaries_original.append(temp_mappings)		#appends those dictionary objects to a list
		first_attempt = False

	for i in range(20):
		dictionary = random_mapping_dictionaries_original[i]				#take a dictionary out of the list
		
		xx = decode(msg,dictionary)											#decode the message using that dictionary
		tt = log_likelyhood_of_sentence(xx)
		list_to_record_orignal_likelyhood.append(tt)						#append the likelyhood value into the list tt
		dictionary_to_hold_values[str(i)] = tt 								#save the value in a dictioary dependednt on index i

	list_to_record_orignal_likelyhood.sort(reverse=True)					#sort the list in descending order

	for i in range(5):
		value = list_to_record_orignal_likelyhood[i]						#take top 5 of the sorted list and take the values as 'values' for dictionaries
		for keys, values in dictionary_to_hold_values.items():
			if value == values:
				a = int(keys)
				dictionary = random_mapping_dictionaries_original[a]		#now find the original dictionary from the random mapping original list
				random_mapping_dictionaries_new.append(dictionary)			#append it to a new list to create new set of dictionaries.


	for i in random_mapping_dictionaries_new:

		for num in range(3):												#repeat this loop thrice for 3 children per parent

			list_of_alphabets = list(string.ascii_lowercase)				#take list of lowercase alphabets
			zz = random.choice(list_of_alphabets)							#randomly select 2 of them
			mm = random.choice(list_of_alphabets)

			while(mm==zz):
				m = random.choice(list_of_alphabets)

			temporary = i[zz]												#swap random keys and values
			i[zz] = i[mm]
			i[mm] = temporary

			random_mapping_dictionaries_new.append(i)						#add this new dictionary to the list

	random_mapping_dictionaries_original = random_mapping_dictionaries_new.copy() #clones new list into the original one
	random_mapping_dictionaries_new.clear()
	list_to_record_new_likelyhood = list_to_record_orignal_likelyhood.copy()	#clones likelyhood list into a new list so that we can take it out and use it
	list_to_record_orignal_likelyhood.clear()
	final_values_dictionary = dictionary_to_hold_values.copy()					#holds values of the latest values in the dictionary
	dictionary_to_hold_values.clear()





def get_best_dictionary():
	dictionary_best = random_mapping_dictionaries_original[0]
	return dictionary_best


	
my_message = encode("Hello this is a trial dry run")
first_attempt = True

for numerical in range(20):
	evolutionary_decryption(my_message, first_attempt )
	first_attempt = False

decode(my_message, get_best_dictionary())














