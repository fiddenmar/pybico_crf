from sklearn.externals import joblib
import sklearn_crfsuite
import regex as re
import sys, getopt
import argparse
import itertools
import operator

from publication import Publication
from source import Source
from author import Author
from misc import Misc
from dbwrapper import DBWrapper

from saver import Saver
# from doc2text import doc2text
from features import word2features, sent2features, sent2labels, sent2tokens

crf = joblib.load('model.pkl')

def group_publication(zipped_list):
	accumulator = []
	it = itertools.groupby(zipped_list, operator.itemgetter(0))
	for key, subiter in it:
		if key not in ["T_TJSEP", "T_DELIMITER"]:
			accumulator.append((key, " ".join([item[1] for item in subiter])))
	accumulator.reverse()
	return dict((k, v) for k, v in accumulator)

def compose_publication(zipped_publication):
	grouped_publication = group_publication(zipped_publication)
	authors = Author.parse_authors(grouped_publication.get("T_AUTHOR"))
	source = Source(grouped_publication.get("T_JOURNAL"))
	misc = Misc(grouped_publication.get("T_LOCATION"), grouped_publication.get("T_PUBLISHER"), grouped_publication.get("T_YEAR"), grouped_publication.get("T_VOLUME"), grouped_publication.get("T_PAGES"))
	return Publication(grouped_publication.get("T_TITLE"), authors, source, misc)

def validate(predict):
	must_be_elements = ["T_AUTHOR", "T_TITLE", "T_JOURNAL"]
	if set(must_be_elements).issubset(predict):
		return True
	return False

def predict_one(sentence):
	target = [ sent2features(s) for s in [sentence.split()] ]
	return crf.predict(target)

def predict(sentence_array):
	results=[]

	for sentence in sentence_array:
		result = predict_one(sentence)
		results.append(*result)
	return results

if __name__ == '__main__':
	input_string = ''
	user = ''
	password = ''
	input_list = []
	input_mode = ''
	input_process = False
	load_process = False
	export_process = False
	export_file_name = ''
	usage_string = 'usage: python3 pybico_crf.py  [-h][-i <input_mode> -s <input_source>][[-l]|[-x <export_name>] -u <user_name> -p <user_password>]'
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hi:u:p:ls:x:')
	except getopt.GetoptError:
		print(usage_string)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(usage_string)
			sys.exit()
		elif opt == '-i':
			input_mode = arg
			input_process = True
		elif opt == '-u':
			user = arg
		elif opt == '-p':
			password = arg
		elif opt == '-l':
			load_process = True
		elif opt == '-s':
			input_string = arg
		elif opt == '-x':
			export_process = True
			export_file_name = arg
		else:
			print(usage_string)
			sys.exit(2)

	if input_process:
		if input_mode == 'input':
			print('Enter the bibliography string:')
			input_string = input()
			input_list = [input_string]
		elif input_mode == 'text':
			if input_string:
				f = open(input_string)
				content = f.read()
				lines = content.split('\n')
				# lines = [ re.sub( r"(?P<high>\p{Lu})(?P<low>((\p{Lu}*) ?)*)(?P<same> (\p{Lu}\p{Ll}*) \p{Lu}\. ?\p{Lu}\.)?", lambda m: m.group("high").capitalize()+m.group("low").lower()+m.group("same"), line) for line in lines ]
				# lines = [ re.sub(r"([\p{L}])//([\p{L}])", lambda m: m.group(1)+" // "+m.group(2), line) for line in lines ]
				# print(lines)
				input_list = [ line.strip() for line in lines ]
			else:
				print('The source (-s) option should be specified for proper input (-i)')
				print(usage_string)
				sys.exit(2)
		elif input_mode == 'string':
			input_list = [input_string]
		elif input_mode == 'doc':
			input_list = doc2text(input_string).split('\n')
			input_list = [ inp.lstrip('0123456789.- ') for inp in input_list ]
		else:
			print('Possible input (-i) option values: input, text, string, doc')
			print(usage_string)
			sys.exit(2)

	if load_process:
		if user != '' and password != '':
			pass
		else:
			print('The user (-u) and the password (-p) options should be specified for proper loading (-l)')

	pred = predict(input_list)
	results = []
	for predict, input_string in zip(pred, input_list):
		# if validate(predict):
			result = list(zip(predict, input_string.split()))
			results.append(result)
		# else:
			# print('Invalid string:')
			# print(input_string)
	# if load_process or export_process:
	# 	db = DBWrapper(user, password)
	# 	if load_process:
	# 		publications = [ compose_publication(result) for result in results ]
	# 		db.add(publications)
	# 	if export_process:
	# 		data = db.get()
	# 		exporter = Saver()
	# 		exporter.save(data, "xlsx", export_file_name)
	# else:
	# for result in results:
	# 	print(group_publication(result))
	data = [ compose_publication(result) for result in results ]
	exporter = Saver()
	exporter.save(data, "xlsx", export_file_name)
