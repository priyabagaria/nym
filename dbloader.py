import atexit
import pickle

db = dict()

def load_user_files():
	userfile = open("user_data_store.db", 'rb')
	global db
	db = pickle.load(userfile)


def save_user_files():
	savefile = open("user_data_store.db", 'wb')
	pickle.dump(db, savefile)


load_user_files()
atexit.register(save_user_files)
