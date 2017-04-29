class Misc:

	def __init__(self, location=None, publisher=None, year=None, volume=None, pages=None):
		self.location = location if location else ""
		self.publisher = publisher if publisher else ""
		self.year = year if year else ""
		self.volume = volume if volume else ""
		self.pages = pages if pages else ""

	def to_string(self):
		str = ""
		fields = [self.location, self.publisher, self.year, self.volume, self.pages]
		for field in fields:
			if field != "":
				str += " - " + field
		return str