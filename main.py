from flask import Flask
from flask import request
from flask import session
from flask import render_template
from flask import jsonify

from dataset_preprocessor import embeddings

from dbloader import db

import hashlib
import os

import intelligence
import word_client
import random

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
	# return render templated homescreen
	return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		print(request.form)
		# method is post, validate userID and hash
		currID = request.form.get("uname", False)
		passwd = request.form.get("pwd", False)
		
		
		hashed = hashlib.sha256(passwd.encode("utf-8")).hexdigest()

		# db = pickledb.load("user_store.db", False)

		user_object = db.get(currID, False)

		if not user_object:
			# somehow redirect user back to login page with error message
			return 

		if user_object["password_hash"] == hashed:
			# User validated
			# direct to homepage

			session["userID"] = currID
			return render_template("question.html")
		
		return render_template("login.html") # TODO! Password mismatch not handled
	return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def newuser():
	# TODO! Check for existing users

	userID = request.form.get("uname", False)
	password = request.form.get("pwd", False)

	
	hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
	print(type(hashed))
	user_object = {"password_hash": hashed, "vector": intelligence.novice_vector().tolist(), "level": 0}

	db[userID] =  user_object

	session["userID"] = userID


	# redirect to homepage
	return render_template("question.html")


@app.route("/question", methods=["GET"])
def getword():
	currUserID = session.get("userID", False)

	if (not currUserID):
		# TODO!
		print('pass')
		pass
		# redirect to login page

	while True:
		try:
			chosen_word = intelligence.get_word(currUserID)

			candidate_synonyms, candidate_antonyms = word_client.get_related(chosen_word)
			
			shortlisted_synonyms = []
			
			for word in candidate_synonyms:
				if embeddings.get(word, []) != []:
					shortlisted_synonyms.append(word)

			shortlisted_antonyms = []

			for word in candidate_antonyms:
				if embeddings.get(word, []) != []:
					shortlisted_antonyms.append(word)

			print(shortlisted_synonyms, shortlisted_antonyms)

			response = {"question_word": chosen_word}

			candidate_words = []
			if len(shortlisted_antonyms) >= 1:
				
				candidate_words.append([random.choice(shortlisted_antonyms), True])
				response["question_text"] = "Choose the antonym"
				
				candidate_words.extend([[synonym, False] for synonym in shortlisted_synonyms[:3]])

				while len(candidate_words) != 4:
					candidate_words.append([random.choice(list(embeddings.keys())), False])

				response["wordses"] = candidate_words
				print("response ", response)
				return jsonify(response)
			
			elif len(shortlisted_synonyms) >= 1:
				
				candidate_words.append([random.choice(shortlisted_synonyms), True])
				response["question_text"] = "Choose the synonym"

				candidate_words.extend([[antonym, False] for antonym in shortlisted_antonyms[:3]])
				
				while len(candidate_words) != 4:
					candidate_words.append([random.choice(list(embeddings.keys())), False])
				random.shuffle(candidate_words)
				response["wordses"] = candidate_words
				print("response ", response)
				return jsonify(response)

			else:
				continue
		except Exception as e:
			print(e.__doc__)
			# return "error"
			return "errrror"
			continue
		else:
			# return jsonified response
			return response 
	# ensure there are atleast 3 of one of the two, if not, try another word / pick something random??

@app.route("/updateuser", methods=["POST"])
def updateuser():
	data = request.get_json()
	print("update user: ", data)
	#print(request.form.keys())
	#intelligence.update(data['userID'], data['word'], data['correct'])
	intelligence.update(data['userID'], data['word'], data['correct'])
	return "user vector updated"

if __name__ == "__main__":
	app.secret_key = os.urandom(16)
	app.run(host='0.0.0.0', port=5000, threaded=True)

