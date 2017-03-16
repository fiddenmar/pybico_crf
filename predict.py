from sklearn.externals import joblib
import sklearn_crfsuite
import re

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
	inp = input("Input string: ")
	pred = predict_one(inp)
	print(list(zip(inp.split(), *pred)))