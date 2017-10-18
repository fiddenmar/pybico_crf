from status import Status

class Source:

	def __init__(self, title=None, status=None):
		self.title = title if title else ""
		self.status = status if status else Status()
