#!/usr/bin/env python
from window import *

class Menu(Pane):
	"""
	Defines a menu where items call local methods.
	"""
	geometry = [EXPAND, EXPAND]
	# Default and selection colours.
	col = [-1, -1] # fg, bg
	sel = [-1,  "blue"]
	pin = [-1, "yellow"]
	items = [
	          [1, 'Hello','handle_hello'],      # [selected, text, function]
	          [0, 'world','handle_world'],
	          [0, 'fight','handle_fight'],
	          [0, 'items','handle_items'],
	          [0, 'magic','handle_magic'],
	          [0, 'flee','handle_flee'],
	]

	def update(self):
		for i, item in enumerate(self.items):
			if item[0] == 2:
				colours = palette(self.pin[0], self.pin[1])
			elif item[0]:
				colours = palette(self.sel[0], self.sel[1])
			else:
				colours = palette(self.col[0], self.col[1])
			if i == self.height:
				text = ' ' * (self.width / 2)
				text += 'V'
			else:
				text = ' ' + item[1]
				spaces = ' ' * (self.width - len(text)) 
				text += spaces
			self.change_content(i, text + '\n', ALIGN_LEFT, colours)

	def process_input(self, character):
		# Handle the return key
		if character == 10 or character == 13:
			for i, item in enumerate(self.items):
				if item[0]:	
					func = getattr(self, item[2].lower(), None)
					if func:
						func()

		# Pin items (spacebar by default)
		elif character == 32:
			for i, item in enumerate(self.items):
				if item[0]:
					if item[0] == 2:
						self.items[i][0] = 1
					else:
						self.items[i][0] = 2
					break

		# Handle navigating the menu
		elif character in [259, 258, 339, 338]:
			for i, item in enumerate(self.items):
				if item[0]:	
					if character == 259:             # up arrow
						if i == 0: break
						if item[0] != 2:
							item[0] = 0
						if self.items[i-1][0] != 2:
							self.items[i-1][0] = 1
						break
					if character == 258:             # down arrow
						if i+1 >= len(self.items): break
						if item[0] != 2:
							item[0] = 0 
						if self.items[i+1][0] != 2:
							self.items[i+1][0] = 1
						break
					if character == 339:             # page up
						if item[0] != 2:
							item[0] = 0
						if self.items[0][0] != 2:
							self.items[0][0] = 1
						break
					if character == 338:             # page down
						if item[0] != 2:
							item[0] = 0
						if self.items[-1][0] != 2:
							self.items[-1][0] = 1
						break
	


if __name__ == '__main__':
	menu = Menu("test menu")
	menu.items.extend([[0, 'Test.','nofunc'] for x in range(50)])
	window = Window()
	window.debug = 1
	window.add(menu)
	window.exit_keys.append(4)
	window.start()
