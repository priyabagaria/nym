import requests

base_url = "http://words.bighugelabs.com/api/2/4c675b5dcbfdffb4d444d3b17fd954d4/"
alternate_base_url = "http://words.bighugelabs.com/api/2/666cadf7eb13cd95cc9f6bfe3024e027/"

def get_related(word):
	if not word:
		return False

	prepared_url = base_url + word + "/json"
	print(prepared_url)
	response = requests.get(prepared_url)

	synonyms = []
	antonyms = []

	response_content = response.json()

	for hi_i in response_content:
		synonyms.extend(response_content[hi_i].get("syn", []))
		synonyms.extend(response_content[hi_i].get("sim", []))
		antonyms.extend(response_content[hi_i].get("ant", []))

	return synonyms, antonyms

# print(get_synonyms("white"))
# print(get_synonyms("slow"))
