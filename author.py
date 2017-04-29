class Author:

	def __init__(self, name=None):
		self.name = name

	@staticmethod
	def parse_authors(string):
		authors = string.split(', ')
		result = []
		for author in authors:
			result.append(Author(author.strip().replace(". ", ".")))
		return result