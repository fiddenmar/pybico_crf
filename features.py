import regex as re

rem_pun_re = re.compile(r'\p{P}+')

def remove_punctuation(s):
	return rem_pun_re.sub('', s)

def word2features(sent, i):
	is_tuple = False
	if isinstance(sent[i], tuple):
		is_tuple = True
	if is_tuple:
		word = sent[i][0]
	else:
		word = sent[i]
	wwnp = remove_punctuation(word)

	features = {
		'word.islower()': int(wwnp.islower()),
		'word.isupper()': int(wwnp.isupper()),
		'word.istitle()': int(wwnp.istitle()),
		'word.isdigit()': int(wwnp.isdigit()),
		'word.isalpha()': int(wwnp.isalpha()),
		'word.endswithdot()': int(word.endswith('.')),
		'word.tjsep()': int(word == '//'),
		'word.isNum()': int('№' in word),
	}
	if i > 0:
		if is_tuple:
			word = sent[i-1][0]
		else:
			word = sent[i-1]
		wwnp = remove_punctuation(word)
		features.update({
			'-1:word.islower()': int(wwnp.islower()),
			'-1:word.isupper()': int(wwnp.isupper()),
			'-1:word.istitle()': int(wwnp.istitle()),
			'-1:word.isdigit()': int(wwnp.isdigit()),
			'-1:word.isalpha()': int(wwnp.isalpha()),
			'-1:word.endswithdot()': int(word.endswith('.')),
			'-1:word.tjsep()': int(word == '//'),
			'-1:word.isNum()': int('№' in word),
			'BOS': 0,
		})
	else:
		features['BOS'] = 1

	if i < len(sent)-1:
		if is_tuple:
			word = sent[i+1][0]
		else:
			word = sent[i+1]
		wwnp = remove_punctuation(word)
		features.update({
			'+1:word.islower()': int(wwnp.islower()),
			'+1:word.isupper()': int(wwnp.isupper()),
			'+1:word.istitle()': int(wwnp.istitle()),
			'+1:word.isdigit()': int(wwnp.isdigit()),
			'+1:word.isalpha()': int(wwnp.isalpha()),
			'+1:word.endswithdot()': int(word.endswith('.')),
			'+1:word.tjsep()': int(word == '//'),
			'+1:word.isNum()': int('№' in word),
			'EOS': 0,
		})
	else:
		features['EOS'] = 1

	return features

def sent2features(sent):
	return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
	return [label for token, label in sent]

def sent2tokens(sent):
	return [token for token, label in sent]