import getch

filepubs = open("pubs", "r")
filetokens = open("tokens", "a+")
pubs = filepubs.readlines()
d = {"0": "T_DELIMITER", "1": "T_AUTHOR", "2": "T_TITLE", "3": "T_JOURNAL", "4": "T_LOCATION", "5": "T_PUBLISHER", "6": "T_YEAR", "7": "T_VOLUME", "8": "T_PAGES", "9": "T_TJSEP"}
for pub in pubs:
	tokens = pub.split()
	labels = [None] * len(tokens)
	for i, token in enumerate(tokens):
		res = None
		while res == None:
			print(pub)
			print(token)
			print("""
				1 - author
				2 - title
				3 - journal
				4 - location
				5 - publisher
				6 - year
				7 - volume
				8 - pages
				9 - title-journal separator
				0 - delimiter""")
			try:
				res = getch.getch()
				labels[i] = d[res]
			except Exception as e:
				res = None
		print(res)
	print(labels)
	filetokens.write((" ").join([item for i in zip(tokens, labels) for item in i])+"\n")

		