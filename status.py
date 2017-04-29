class Status:

	def __init__(self, status_dict = None):
		self.status_dict = status_dict if status_dict else {}

	def add(self, status_name, status_impact, replace = 1):
		if not replace:
			if self.status_dict[status_name]:
				pass
		self.status_dict[status_name] = status_impact

	def merge(self, status_dict, replace = 1):
		for key, val in status_dict:
			if not replace:
				if self.status_dict[key]:
					pass
			self.status_dict[key] = val