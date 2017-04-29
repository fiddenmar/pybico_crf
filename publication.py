from source import Source
from author import Author
from misc import Misc

class Publication:

	def __init__(self, title=None, author=None, source=None, misc=None):
		self.title = title if title else ""
		self.source = source if source else Source()
		self.misc = misc if misc else Misc()
		self.author = author if author else [Author()]