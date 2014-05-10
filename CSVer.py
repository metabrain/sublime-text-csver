import sublime, sublime_plugin, csv

class CsverCommand(sublime_plugin.TextCommand):

	header = ''
	columns = []

	def run(self, edit):
		if not (self.view.window() is None \
				or self.view.file_name() is None \
				or self.view.file_name().endswith(".csv")):
			self.view.set_status('csver', '')
			return

		self.update_header()

	def update_header(self):
		first_line = self.get_line(0)
		rows = first_line.split(',')
		columns = []
		for row in rows:
			columns.append(row)

		col = self.get_selected_column()

		new_cols = list(columns)
		new_cols_seln = list()

		for i in range(0,len(columns)):
			if i in col:
				new_cols[i] = columns[i].upper()
				new_cols_seln.append(columns[i].upper())
			else:
				new_cols[i] = columns[i]

		selection = ','.join(new_cols)
		seln = ','.join(new_cols_seln)

		msg = "@%s -> %s " % (seln,selection)

		self.view.set_status('csver', msg)

	def get_selected_column(self):
		line = self.get_current_line()
		cols = line.split(',')

		if len(cols) == 0:
			return []

		def get_idx(col):
			idx = 0
			for i in range(0,len(cols)):
				idx = idx + len(cols[i]) + 1
				if col < idx:
					return i
			return 0 # In weird edge cases, such as endlines selections

		left_col = get_idx(self.view.rowcol(self.view.sel()[0].begin())[1])
		right_col = get_idx(self.view.rowcol(self.view.sel()[0].end())[1])

		#print "return range(left_col=%s,right_col=%s)" % (left_col,right_col)

		return range(left_col,right_col+1) #plus 1 for inclusive

	def get_current_line(self):
		view_selection = self.view.sel()
		if not view_selection:
			return None

		point = view_selection[0].end()
		return self.get_line(point)

	def get_line(self, point):
		return self.view.substr(self.view.line(point)).strip()

	def clear_statusbar(view):
		view.erase_status('csver')


class CsverEventListener(sublime_plugin.EventListener):

	def on_load(self, view):
		view.run_command('csver', None)

	def on_selection_modified(self, view):
		view.run_command('csver', None)

	def on_activated(self, view):
		view.run_command('csver', None)

	def on_modified(self, view):
		view.run_command('csver', None)