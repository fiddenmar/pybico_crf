import pymysql.cursors

class DBWrapper:

	def __init__(self, user = None, password = None, url = "127.0.0.1"):
		self.user = user
		self.password = password
		self.url = url

	def add(self, data):
		connection = pymysql.connect(host=self.url,
									user=self.user,
									password=self.password,
									db='pybico_crf',
									charset='utf8',
									cursorclass=pymysql.cursors.DictCursor)
		try:
			for item in data:
				author_id = []
				source_id = 0
				publication_id = 0
				with connection.cursor() as cursor:
					cursor.execute('SET NAMES utf8;')
					cursor.execute('SET CHARACTER SET utf8;')
					cursor.execute('SET character_set_connection=utf8;')
					get_source_sql = "SELECT `id` FROM `source` WHERE `name`=%s"
					cursor.execute(get_source_sql, (item.source.title))
					result = cursor.fetchone()
					if result:
						source_id = result["id"]
					else:
						insert_source_sql = "INSERT INTO `source` (`name`) VALUES (%s)"
						cursor.execute(insert_source_sql, (item.source.title))
						connection.commit()
						cursor.execute(get_source_sql, (item.source.title))
						res = cursor.fetchone()
						source_id = res["id"]
				for a in item.author:
					author = a.name.strip()
					if author != "":
						with connection.cursor() as cursor:
							get_author_sql = "SELECT `id` FROM `author` WHERE `name`=%s"
							cursor.execute(get_author_sql, (author))
							result = cursor.fetchone()
							if result:
								author_id.append(result["id"])
							else:
								insert_author_sql = "INSERT INTO `author` (`name`) VALUES (%s)"
								cursor.execute(insert_author_sql, (author))
								connection.commit()
								cursor.execute(get_author_sql, (author))
								res = cursor.fetchone()
								author_id.append(res["id"])
				with connection.cursor() as cursor:
					get_publication_sql = "SELECT `id` FROM `publication` WHERE `title`=%s"
					cursor.execute(get_publication_sql, (item.title))
					result = cursor.fetchone()
					if result:
						publication_id = result["id"]
					else:
						insert_publication_sql = "INSERT INTO `publication` (`title`, `source_id`, `misc`) VALUES (%s, %s, %s)"
						cursor.execute(insert_publication_sql, (item.title, str(source_id), item.misc.to_string()))
						connection.commit()
						cursor.execute(get_publication_sql, (item.title))
						res = cursor.fetchone()
						publication_id = res["id"]
						for author in author_id:
							get_relation_sql = "SELECT * FROM `relation` WHERE `publication_id`=%s AND `author_id`=%s"
							cursor.execute(get_relation_sql, (str(publication_id), str(author)))
							result = cursor.fetchone()
							if not result:
								insert_relation_sql = "INSERT INTO `relation` (`publication_id`, `author_id`) VALUES (%s, %s)"
								cursor.execute(insert_relation_sql, (str(publication_id), str(author)))
								connection.commit()
		finally:
			connection.close()

	def get(self):
		data = []
		connection = pymysql.connect(host=self.url,
									user=self.user,
									password=self.password,
									db='pybico_crf',
									charset='utf8',
									cursorclass=pymysql.cursors.DictCursor)
		try:
			with connection.cursor() as cursor:
				get_publication_sql = "SELECT * FROM `publication` WHERE `registered`=%s"
				cursor.execute(get_publication_sql, (str(0)))
				result = cursor.fetchall()
				for pub in result:
					target_id = pub["id"]
					authors = []
					source = ""
					get_authors_sql = "SELECT `author_id` FROM `relation` WHERE `publication_id`=%s"
					cursor.execute(get_authors_sql, (str(target_id)))
					res = cursor.fetchall()
					for a in res:
						get_name_sql = "SELECT `name`, `position`, `miet` FROM `author` WHERE `id`=%s"
						cursor.execute(get_name_sql, (str(a["author_id"])))
						author = cursor.fetchone()
						authors.append({"name": author["name"], "position": author["position"], "miet": author["miet"]})
					get_source_sql = "SELECT `name`, `type`, `scopus`, `wos`, `hac`, `rsci` FROM `source` WHERE `id`=%s"
					cursor.execute(get_source_sql, (str(pub["source_id"])))
					src_res = cursor.fetchone()
					source = {"name": src_res["name"], "type": src_res["type"], "scopus": src_res["scopus"], "wos": src_res["wos"], "hac": src_res["hac"], "rsci": src_res["rsci"]}
					data.append({"authors": authors, "article": pub["title"], "source": source, "misc": pub["misc"]})
		finally:
			connection.close()
		return data