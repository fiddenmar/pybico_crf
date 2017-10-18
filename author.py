class Author:

	def __init__(self, name=None):
		self.name = name

	def __str__(self):
		return self.name

	@staticmethod
	def parse_authors(string):
		if string:
			authors = string.split(', ')
			result = []
			for author in authors:
				result.append(Author(author.strip().replace(". ", ".")))
			return result
		else:
			return [""]