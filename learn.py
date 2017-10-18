from itertools import chain
import sklearn
import random
import scipy.stats
from sklearn.metrics import make_scorer, confusion_matrix
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from sklearn.externals import joblib
import re

from features import word2features, sent2features, sent2labels, sent2tokens

def cluster(data_global):
	groups = []
	for data in data_global:
		groups.append([data[0]])
		for x in data[1:]:
			if abs(x == groups[-1][-1]):
				groups[-1].append(x)
			else:
				groups.append([x])
	return groups

if __name__ == "__main__":
	file_with_tokens = open("tokens")
	token_lines = file_with_tokens.readlines()
	list_of_raw_tokens = [x.split() for x in token_lines]
	list_of_raw_tokens
	list_of_tuples_tokens = list(list(zip(t[::2], t[1::2])) for t in list_of_raw_tokens)
	token_length = len(list_of_tuples_tokens)
	data = list_of_tuples_tokens

	random.seed()
	random.shuffle(data)

	train = list_of_tuples_tokens[0:int(token_length*8/10)]
	test = list_of_tuples_tokens[int(token_length*8/10):]

	X_train = [sent2features(s) for s in train]
	y_train = [sent2labels(s) for s in train]

	X_test = [sent2features(s) for s in test]
	y_test = [sent2labels(s) for s in test]

	crf = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.01, max_iterations=100, all_possible_transitions=True)
	crf.fit(X_train, y_train)
	joblib.dump(crf, 'model.pkl') 

	labels = list(crf.classes_)
	sorted_labels = sorted(
		labels,
		key=lambda name: (name[1:], name[0])
	)

	y_pred = crf.predict(X_test)
	print(metrics.flat_classification_report(
		y_test, y_pred, labels=sorted_labels, digits=3
	))
	y_cl_test = y_test[:50]
	# print(y_cl_test)
	# print(cluster(y_cl_test))
	ds = ["T_DELIMITER", "T_AUTHOR", "T_TITLE", "T_JOURNAL", "T_LOCATION", "T_PUBLISHER", "T_YEAR", "T_VOLUME", "T_PAGES", "T_TJSEP"]
	tag_dict_test = {"T_DELIMITER": [], "T_AUTHOR": [], "T_TITLE": [], "T_JOURNAL": [], "T_LOCATION": [], "T_PUBLISHER": [], "T_YEAR": [], "T_VOLUME": [], "T_PAGES": [], "T_TJSEP": []}
	tag_dict_pred = {"T_DELIMITER": [], "T_AUTHOR": [], "T_TITLE": [], "T_JOURNAL": [], "T_LOCATION": [], "T_PUBLISHER": [], "T_YEAR": [], "T_VOLUME": [], "T_PAGES": [], "T_TJSEP": []}
	for d in ds:
		for seq in cluster(y_test):
			if seq[0] == d:
				tag_dict_test[d].append(seq)
		for seq in cluster(y_pred):
			if seq[0] == d:
				tag_dict_pred[d].append(seq)

	check_sum = 0;
	for d in ds:
		check = metrics.sequence_accuracy_score(
			tag_dict_test[d], tag_dict_pred[d]
		)
		check_sum += check
		print(d, "\t", check)

	print("Average: ", check_sum / len(ds))
