import sys
import xbmcgui, xbmcaddon
#import pyxbmct.addonwindow as pyxbmct
import dudehere.routines.addonwindow as pyxbmct

class Manager():
	def __init__(self, width=800, height=400, columns=4, rows=6):
		self._width = width
		self._height = height
		self._columns = columns
		self._rows = rows
		self._confirmation = False
		self._pages = []

	def set_title(self, title):
		self._title = title

	def set_object_event(self, index, event, obj, target=None):
		if event == 'focus':
			self.set_focus(index, obj)
		elif event == 'left':
			self.set_event(index, 'left', obj, target)
		elif event == 'right':
			self.set_event(index, 'right', obj, target)
		elif event == 'down':
			self.set_event(index, 'down', obj, target)
		elif event == 'up':
			self.set_event(index, 'up', obj, target)
		elif event == 'action':
			self.set_event(index, 'action', obj, target)
			
	def get_object(self, index, key):
		return self.get_page(index).get_object(key)

	def set_focus(self, index, obj):
		self.get_page(index).set_focus(obj)

	def set_event(self, index, event, obj, target):
		self.get_page(index).set_object_event(event, obj, target)
	
	def get_value(self, index, obj):
		return self.get_page(index).get_value(obj)
		
	def get_page(self, index):
		return self._pages[index]
	
	def add_page(self, page, index=False):
		if index:
			self._pages[index] = page
		else:
			index = len(self._pages)
			page.set_index(index)
			self._pages.append(page)
			
	def get_values(self):
		values = {}
		for index in range(0,len(self._pages)-1):
			values[index] = self.get_page(index).get_values()
		return values
	
	def add_confirmation(self, page):
		self._confirmation = page

	def show_confirmation(self):
		if self._confirmation:
			self.get_page(self._current_page).close()
			self._confirmation.doModal()

	def build(self, fanart=None):
		index=0
		count = len(self._pages)
		for index in range(0,count):
			page=self.get_page(index)
			if fanart is not None:
				page.__background = xbmcgui.ControlImage (0, 0, 1280, 720, fanart)
				page.addControl(page.__background)
				page.setFrame(page.title)

			if page._width is None: page._width = self._width
			if page._height is None: page._height = self._height
			if page._rows is None: page._rows = self._rows
			if page._columns is None: page._columns = self._columns

			page.setGeometry(page._width, page._height, page._rows, page._columns)
			page.draw()

				
			if index < count-1:
				pos_x = page._columns-1
				pos_y = page._rows-1
				try:
					page.create_button('next_button', page.overide_strings["next_button"])
				except:	
					page.create_button('next_button', 'Next >')
				page.add_object('next_button', pos_y, pos_x)
				try:
					page.set_object_event('action', 'next_button', page.overide_actions['next_button'])
				except:
					page.set_object_event('action', 'next_button', self.next_page)
			if index > 0 and index <= count:
				pos_x = 0
				pos_y = page._rows-1
				try:
					page.create_button('previous_button', page.overide_strings["previous_button"])
				except:	
					page.create_button('previous_button', '< Previous')
				page.add_object('previous_button', pos_y, pos_x)
				try:
					page.set_object_event('action', 'previous_button', page.overide_actions['previous_button'])
				except:
					page.set_object_event('action', 'previous_button', self.previous_page)

			self.add_page(page, index=index)
		if self._confirmation:
			if self._confirmation._width is None: self._confirmation._width = self._width
			if self._confirmation._height is None: self._confirmation._height = self._height
			if self._confirmation._rows is None: self._confirmation._rows = self._rows
			if self._confirmation._columns is None: self._confirmation._columns = 3
			pos_x = 1
			pos_y = self._confirmation._rows-1
			self._confirmation.setGeometry(self._confirmation._width, self._confirmation._height, self._confirmation._rows, self._confirmation._columns)
			self._confirmation.draw()
			try:
				self._confirmation.create_button('confirmation_close_button', page.overide_strings["confirmation_close_button"])
			except:	
				self._confirmation.create_button('confirmation_close_button', 'Close')
			self._confirmation.add_object('confirmation_close_button', pos_y, pos_x)
			try:
				self._confirmation.set_object_event('action', 'confirmation_close_button', page.overide_actions['confirmation_close_button'])
			except:
				self._confirmation.set_object_event('action', 'confirmation_close_button', self.close_all)
			self._confirmation.set_focus('confirmation_close_button')
		self._build=False

	def close_all(self):
		for index in range(0,len(self._pages)):
			try:
				self.get_page(index).close()
			except: pass
		try:
			self._confirmation.close()
		except: pass
		
	def show(self, index=0):
		self._current_page=index
		self.get_page(index).doModal()

	def next_page(self):
		index = self._current_page+1
		if index > len(self._pages): index = len(self._pages)-1
		self.get_page(self._current_page).close()
		self.show(index)

	def previous_page(self):
		index = self._current_page-1
		if index < 0: index = 0
		self.get_page(self._current_page).close()
		self.show(index)
