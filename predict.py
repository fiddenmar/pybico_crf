from sklearn.externals import joblib
import sklearn_crfsuite
import re
import sys, getopt
import argparse

from features import word2features, sent2features, sent2labels, sent2tokens

crf = joblib.load('model.pkl')

def predict_one(sentence):
	target = [sent2features(s) for s in [sentence.split()]]
	return crf.predict(target)

def predict(sentence_array):
	results=[]

	for sentence in sentence_array:
		result=predict_one(sentence)
		results.append(result)
	return results

if __name__ == "__main__":
	inp = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hs:", ["str="])
	except getopt.GetoptError:
		print("usage: python3 predict.py [-s <inputString>]")
		sys.exit(2)
	if len(opts) == 0:
		print("Enter the bible string")
		inp = input()
	else:
		for opt, arg in opts:
			if opt == '-h':
				print("usage: python3 predict.py [-s <inputString>]")
				sys.exit()
			elif opt in ("-s", "--str"):
				inp = arg
			else:
				print("usage: python3 predict.py [-s <inputString>]")
	pred = predict_one(inp)
	print(list(zip(inp.split(), *pred)))
