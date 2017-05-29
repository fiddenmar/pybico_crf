from sklearn.externals import joblib
import sklearn_crfsuite
import re
import sys, getopt
import argparse
import itertools
import operator

from publication import Publication
from source import Source
from author import Author
from misc import Misc
from dbwrapper import DBWrapper

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

def predict_one(sentence):
	target = [sent2features(s) for s in [sentence.split()]]
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
	usage_string = 'usage: python3 pybico_crf.py  [-h][-i <input_mode> -s <input_source>][-l -u <user_name> -p <user_password>]'
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hi:u:p:ls:')
	except getopt.GetoptError:
		print(usage_string)
		sys.exit(2)
	i_flag = 'input'
	u_flag = False
	p_flag = False
	l_flag = False
	s_flag = False
	for opt, arg in opts:
		if opt == '-h':
			print(usage_string)
			sys.exit()
		elif opt == '-i':
			i_flag = arg
		elif opt == '-u':
			user = arg
			u_flag = True
		elif opt == '-p':
			password = arg
			p_flag = True
		elif opt == '-l':
			l_flag = True
		elif opt == '-s':
			input_string = arg
			s_flag = True
		else:
			print(usage_string)
			sys.exit(2)
	if i_flag == 'input':
		input_string = input()
		input_list = [input_string]
	elif i_flag == 'text':
		if s_flag:
			f = open(input_string)
			content = f.read()
			lines = content.split('\n')
			input_list = [line.strip() for line in lines]
		else:
			print('The source (-s) option should be specified for proper input (-i)')
			print(usage_string)
			sys.exit(2)
	elif i_flag == 'string':
		input_list = [input_string]
	else:
		print('Possible input (-i) option values: input, text, string')
		print(usage_string)
		sys.exit(2)
	pred = predict(input_list)
	results = []
	for predict, input_string in zip(pred, input_list):
		result = list(zip(predict, input_string.split()))
		results.append(result)
	if l_flag:
		if u_flag and p_flag:
			publications = [ compose_publication(result) for result in results ]
			db = DBWrapper(user, password)
			db.add(publications)
		else:
			print('The user (-u) and the password (-p) options should be specified for proper loading (-l)')
	else:
		for result in results:
			print(group_publication(result))
