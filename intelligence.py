import numpy as np
from dataset_preprocessor import embeddings
from dbloader import db
import scipy
import random
from scipy.stats import gamma

ALPHA  = 0.05
BETA = 0.02
SHAPE = 2
SCALE = 1

def get_user_vector(uid):
	# db = pickledb.load("user_store.db", False)
	user_obj = db.get(uid, False)

	return np.asarray(user_obj["vector"])


def update_user_vector(uid, vector):
	# db = pickledb.load("user_store.db", True)
	user_obj = db.get(uid, False)
	user_obj["vector"] = vector.tolist()

	db[uid] = user_obj
	print("User vector updated: ", user_obj["vector"])


def update(userID, word, correct):
	user_vector = get_user_vector(userID)
	word_vector = embeddings[word]
	
	if correct:
		user_new = user_vector + ALPHA*word_vector
		word_new = word_vector + ALPHA*user_vector
	else:
		user_new = user_vector - BETA*word_vector
		word_new = word_vector - BETA*user_vector

	user_new = user_new / np.linalg.norm(user_new)
	word_new = word_new / np.linalg.norm(word_new)

	update_user_vector(userID, user_new)
	embeddings[word] =  word_new


def get_word(userID):
	print("In get_word:", userID)
	print(type(userID))
	user_vector = get_user_vector(userID)

	# finding cosine similarity of user vector and word vectors
	ranked_words = [ [word, np.dot(user_vector, word_vector)] for word, word_vector in embeddings.items()]

	# sort the words in increasing order of distance
	# ranked_words.sort(key = lambda x: x[1])
	dist_array = [x[1] for x in ranked_words]
	#print("dist_array:",dist_array[:10])
	length = len(dist_array)
	#print("length = ", length)
	g_values = [float(y) for y in np.random.gamma(SHAPE, SCALE, length)] #np.random.gamma(shape, scale, output_length)
	#print(g_values[:10])
	prob_values = [float(gamma.pdf(g, SHAPE, scale = SCALE)) for g in g_values] #gamma.pdf(input_x, shape, location, scale), location is for shifting so ignored
	'''prob_ranks = [float(gamma.pdf(x, 1, SHAPE, SCALE)) for x in dist_array]
	print("works3S")
	print(prob_ranks[:10])'''
	#print(prob_values[:10])
	i = 0
	for word in ranked_words:
		#print("word:", word)
		word.append(prob_values[i])
		#print("word is :", word)
		i = i+1
	#print("new ranked_words:",ranked_words[:10])
	ranked_words.sort(key = lambda x : x[2], reverse = True)
	#print("sorted new ranked_words:", ranked_words[:10], ranked_words[-1], ranked_words[0])
	return ranked_words[0][0]

	#w = random.choice(ranked_words)
	#print(w)
	#return w[0]
	# perform random sampling centered around a gamma distribution
	# return a word based on that


def novice_vector():
	return np.ones(8) / np.linalg.norm(np.ones(8))
