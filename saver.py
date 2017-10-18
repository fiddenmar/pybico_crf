import xlsxwriter

class Saver:

	def __init__(self):
		pass

	def save(self, data, save_format = None, filename = None):
		self.save_format = save_format if save_format else "xlsx"
		self.filename = filename if filename else "result."+self.save_format
		self.save_publications(data)

	def save_publications(self, data):
		offset = 3
		wb = xlsxwriter.Workbook(self.filename)
		ws = wb.add_worksheet()
		center = wb.add_format()
		center.set_text_wrap()
		center.set_align("center")
		center.set_align("vcenter")
		left = wb.add_format()
		left.set_text_wrap()
		left.set_align("left")
		left.set_align("top")

		miet = wb.add_format()
		miet.set_underline()
		aspir = wb.add_format()
		aspir.set_underline()
		aspir.set_bold()
		student = wb.add_format()
		student.set_underline()
		student.set_italic()
		styles = {"miet": miet, "aspir": aspir, "student": student}

		ws.write(0, 0, "№ раздела", center)
		ws.write(0, 1, "Автор (ФИО сотрудника МИЭТ, студента, аспиранта", center)
		ws.write(0, 2, "Название статьи, книги, монографии, уч. пособия и др.", center)
		ws.write(0, 3, "Наименование журнала или конференции", center)
		ws.write(0, 4, "Город, издательство, год, номер, том, страницы", center)
		ws.write(0, 5, "Статус\nWeb of Science\nScopus\nРИНЦ\nВАК", center)
		ws.write(0, 6, "Импакт-фактор", center)
		ws.merge_range('H1:I1', "Количество авторов", center)
		ws.write(1, 7, "Всего", center)
		ws.write(1, 8, "В т.ч. сотрудников МИЭТ", center)

		ws.set_row(0, 80)
		ws.set_row(1, 40)
		ws.set_column(0, 0, 10)
		ws.set_column(1, 1, 20)
		ws.set_column(2, 2, 40)
		ws.set_column(3, 3, 25)
		ws.set_column(4, 4, 25)
		ws.set_column(5, 5, 10)
		ws.set_column(6, 6, 10)
		ws.set_column(7, 7, 10)
		ws.set_column(8, 8, 15)

		for i in range(1, 10):
			ws.write(2, i-1, str(i), center)

		for i, item in enumerate(data):
			pos = i+offset
			# ws.write(pos, 0, str(item.source.status), center)
			ws.write(pos, 1, " ".join(str(x) for x in item.author))
			# ws.write_rich_string(pos, 1, *get_author_names(item.author, styles, left))
			ws.write(pos, 2, item.title, left)
			ws.write(pos, 3, item.source.title, left)
			ws.write(pos, 4, str(item.misc), left)
			# ws.write(pos, 5, str(item.source.status), center)
			# ws.write(pos, 6, str(get_impact_factor(item.source)), center)
			ws.write(pos, 7, str(len(item.author)), center)
			# ws.write(pos, 8, str(get_author_miet(item.authors)), center)
			height = 4
			if len(item.author) > height:
				height = len(item.author)
			ws.set_row(pos, 20*height)

		wb.close()

	def save_data(self, data):
		offset = 3
		wb = xlsxwriter.Workbook(self.filename)
		ws = wb.add_worksheet()
		center = wb.add_format()
		center.set_text_wrap()
		center.set_align("center")
		center.set_align("vcenter")
		left = wb.add_format()
		left.set_text_wrap()
		left.set_align("left")
		left.set_align("top")

		miet = wb.add_format()
		miet.set_underline()
		aspir = wb.add_format()
		aspir.set_underline()
		aspir.set_bold()
		student = wb.add_format()
		student.set_underline()
		student.set_italic()
		styles = {"miet": miet, "aspir": aspir, "student": student}

		ws.write(0, 0, "№ раздела", center)
		ws.write(0, 1, "Автор (ФИО сотрудника МИЭТ, студента, аспиранта", center)
		ws.write(0, 2, "Название статьи, книги, монографии, уч. пособия и др.", center)
		ws.write(0, 3, "Наименование журнала или конференции", center)
		ws.write(0, 4, "Город, издательство, год, номер, том, страницы", center)
		ws.write(0, 5, "Статус\nWeb of Science\nScopus\nРИНЦ\nВАК", center)
		ws.write(0, 6, "Импакт-фактор", center)
		ws.merge_range('H1:I1', "Количество авторов", center)
		ws.write(1, 7, "Всего", center)
		ws.write(1, 8, "В т.ч. сотрудников МИЭТ", center)

		ws.set_row(0, 80)
		ws.set_row(1, 40)
		ws.set_column(0, 0, 10)
		ws.set_column(1, 1, 20)
		ws.set_column(2, 2, 40)
		ws.set_column(3, 3, 25)
		ws.set_column(4, 4, 25)
		ws.set_column(5, 5, 10)
		ws.set_column(6, 6, 10)
		ws.set_column(7, 7, 10)
		ws.set_column(8, 8, 15)

		for i in range(1, 10):
			ws.write(2, i-1, str(i), center)

		for i, item in enumerate(data):
			pos = i+offset
			ws.write(pos, 0, str(item["source"]["type"]), center)
			ws.write_rich_string(pos, 1, *get_author_names(item["author"], styles, left))
			ws.write(pos, 2, item["article"], left)
			ws.write(pos, 3, item["source"]["name"], left)
			ws.write(pos, 4, item["misc"], left)
			ws.write(pos, 5, str("\n".join(get_status(item["source"]))), center)
			ws.write(pos, 6, str(get_impact_factor(item["source"])), center)
			ws.write(pos, 7, str(len(item["authors"])), center)
			ws.write(pos, 8, str(get_author_miet(item["authors"])), center)
			height = 4
			if len(item["authors"]) > height:
				height = len(item["authors"])
			ws.set_row(pos, 20*height)

		wb.close()

def get_author_names(authors, styles, cell_format):
	names = []
	for i, author in enumerate(authors):
		if (not not author["miet"]):
			if (author["position"] == "аспирант"):
				names.append(styles["aspir"])
			elif (author["position"] == "студент"):
				names.append(styles["student"])
			else:
				names.append(styles["miet"])
		if i == len(authors)-1:
			names.append(author["name"])
		else:
			names.append(author["name"]+"\n")
	names.append(cell_format)
	return tuple(names)

def get_author_miet(authors):
	miet = 0
	for author in authors:
		miet += not not author["miet"]
	return miet

def get_impact_factor(source):
	impact_list = [source["scopus"], source["wos"], source["hac"], source["rsci"]]
	impact = max(impact_list)
	if impact == 0:
		impact = -1
	if impact == -1:
		return ""
	return impact

def get_status(source):
	status = []
	impact_list = [source["scopus"], source["wos"], source["hac"], source["rsci"]]
	status_list = ["Scopus", "Web of Science", "ВАК", "РИНЦ"]
	for i, impact in enumerate(impact_list):
		if impact != 0:
			output = status_list[i]
			if impact != -1:
				output = output+"="+impact
			status.append(output)
	return status