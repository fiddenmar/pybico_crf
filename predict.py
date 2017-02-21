from sklearn.externals import joblib
import sklearn_crfsuite
import re

from features import word2features, sent2features, sent2labels, sent2tokens

crf = joblib.load('model.pkl')

def predict(sentance):
	target = [sent2features(s) for s in [sentance.split()]]
	return crf.predict(target)

if __name__ == "__main__":
	inp = input("Input string: ")
	pred = predict(inp)
	print(list(zip(inp.split(), *pred)))