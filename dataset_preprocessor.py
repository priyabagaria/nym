from word_frequencies import log_frequency_index_full
from collections import Counter
import numpy as np

THRESHOLD = 3.5


def filter_words(word_freq_raw, threshold):
	word_freq_subset = {}
	for key, value in word_freq_raw.items():
		if key.isupper():
			continue
		if value < THRESHOLD:
			continue
		word_freq_subset[key] = value
	
	return word_freq_subset


def generate_encoding(word_list):

	nclasses = 64

	embeddings = dict()

	min_freq = min(word_list.values())
	max_freq = max(word_list.values())

	for k, v in word_list.items():
		this_class = int((nclasses-1) * (v - min_freq) / (max_freq - min_freq))
		embeddings[k] = np.asarray([int(c) for c in bin(this_class)[2:].rjust(8, "0")])
		embeddings[k] = embeddings[k] / np.linalg.norm(embeddings[k]) # rehashes like crazy, pls fix
	return embeddings


# word_freq_subset = filter_words(log_frequency_index_full, THRESHOLD)
embeddings = generate_encoding(filter_words(log_frequency_index_full, THRESHOLD))

# print(embeddings)
print(len(embeddings))