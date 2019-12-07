#Routines.window
# -*- coding: utf-8 -*-

'''
	Copyright (C) 2015 DudeHere

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
import sys, math
import xbmcgui, xbmcaddon

from dudehere.routines import *
from dudehere.routines.vfs import VFSClass
import dudehere.routines.addonwindow as pyxbmct
ACTION_ENTER = 13 
ACTION_SELECT_ITEM = 7
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_SHOW_INFO = 11
ACTION_CONTEXT_MENU = 117
TEXTURES = VFSClass().join(xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path'), 'resources/textures/')

'''
	The window wrapper extends the work by Roman_V_M script.module.pyxbmct.
	See http://forum.kodi.tv/showthread.php?tid=174859 for details.
	Documentation can be found at http://romanvm.github.io/PyXBMCt/docs/
	
	The purpose of this module is mainly to provide a interface for adding
	a window control that can be loaded through the manager class for creating
	multi-window forms.
	
	Additionally there are some helper functions for setting and getting stored values.
	There a couple of extra controls created by extending those currently provided.
	Nothing new here.	

'''

class Window(pyxbmct.AddonDialogWindow):
	def __init__(self, title='', width=None, height=None, columns=None, rows=None, shade=False, quiet=False, show_frame=True, skin_path=''):
		super(Window,self).__init__(title, show_frame=show_frame)
		self.quiet = quiet
		self.title = title
		self.shade = shade
		self.show_frame = show_frame
		self.__index = None
		self.__draw = False
		self.overide_strings = {}
		self.overide_actions = {}
		self._width = width
		self._height = height
		self._columns = columns
		self._rows = rows
		self.__objects = {}
		if skin_path:
			self._skin_path = skin_path
		else:
			self._skin_path = TEXTURES

		
		if None not in [width, height, rows, columns]:
			self.setGeometry(width, height, rows, columns)

	def setAnimation(self, control): control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),('WindowClose', 'effect=fade start=100 end=0 time=250',)])
	
	def get_index(self): return self.__index

	def set_index(self, index): self.__index=index

	def draw(self):
		''' Function draw
			initialize built-in functions
			this automatically called.
		'''
		if self.shade:
			self.create_image('shading', VFSClass().join(self._skin_path, 'default/AddonWindow/shading.png'), aspectRatio=1)
			self.add_object('shading', 0, 0, columnspan=self._columns, rowspan=self._rows, pad_y=0)
		self.set_info_controls()
		self.set_active_controls()
		self.set_navigation()
		self.connect(pyxbmct.ACTION_NAV_BACK, self._cancel)
		self.connect(pyxbmct.KEY_BACKSPACE, self._cancel)
		self.connect(pyxbmct.ACTION_PREVIOUS_MENU, self._cancel)
		self.__draw=True		
	
	def show(self):
		if self.__draw is False:
			self.draw()
		self.doModal()
	
	def hide(self): self.close()
	
	def reload(self):
		self.hide()
		self.__draw = False
		self.show()
		
		
	def set_info_controls(self):
		''' Function set_info_controls
			used to define static window controls
			this should be overwritten or the window will be blank.
		'''
		pass	

	def set_active_controls(self):
		''' Function set_active_controls
			used to define dynamic window controls
			this will be executed after set_info_controls
			this should be overwritten or the window will be blank.
		'''
		pass
	
	def set_navigation(self):
		''' Function set_navigation
			used to define navigation events
			this will be executed after set_info_controls
			this should be overwritten or there will be no navigation events
		'''
		pass
	
	def _cancel(self):
		if not self.quiet:
			dialog = xbmcgui.Dialog()
			if dialog.yesno("Exit " + self.title, "Are you sure?", "") : self.close()
		else: self.close()
	
	def set_focus(self, target):
		''' Function set_focus
			used to set the inital focus on a specific object by target name
			
			Example:
				self.set_focus('button_name')
		'''
		self.setFocus(self.__get_object(target))
		
	def set_object_event(self, event, obj, target=None):
		if event == 'focus':
			self.set_focus(obj)
		elif event == 'left':
			self.__get_object(obj).controlLeft(self.__get_object(target))
		elif event == 'right':
			self.__get_object(obj).controlRight(self.__get_object(target))
		elif event == 'down':
			self.__get_object(obj).controlDown(self.__get_object(target))
		elif event == 'up':
			self.__get_object(obj).controlUp(self.__get_object(target))
		elif event == 'action':
			self.connect(self.__get_object(obj), target)
		elif event == 'context':	
			self.connectEventList([ACTION_MOUSE_RIGHT_CLICK, ACTION_CONTEXT_MENU],target)
			
	def __put_object(self, name, obj):
		self.__objects[name] = obj
	
	def __get_object(self, key):
		return self.__objects[key]
	
	def put_object(self, name, obj):
		self.__objects[name] = obj
	
	def get_object(self, key):
		return self.__objects[key]
	
	def create_label(self, text, **kwargs):
		''' Function create_label
			used to create a text label
			the label needs to be added to the window via self.add_label
			
			Parameters:
			text: string or unicode - text string.
			font: string - font used for label text. (e.g. 'font13')
			textColor: hexstring - color of enabled label's label. (e.g. '0xFFFFFFFF')
			disabledColor: hexstring - color of disabled label's label. (e.g. '0xFFFF3300')
			alignment: integer - alignment of label - *Note, see xbfont.h
			hasPath: bool - True=stores a path / False=no path.
			angle: integer - angle of control. (+ rotates CCW, - rotates CW)
			
			Example:
				label = self.create_label('The text is blah blah blah', font='font14')
		'''
		return pyxbmct.Label(text, **kwargs)
		
	def add_label(self, label, row, column, **kwargs):
		''' Function add_label
			Place a label within the window grid layout.
			
			Paramaters:
			label: label object created with self.create_label
			row: x coordinate
			column: y coordinate
			rowspan: expand by n rows
			columnspan: expand by n columns
			pad_x: horizontal padding
			pad_y: vertical padding
			size and aspect adjustments. Negative values can be used
			to make a control overlap with grid cells next to it, if necessary.
			Raises AddonWindowError if a grid has not yet been set.
			Example:
				self.add_label(label_object, 1,1, rowspan=2)
		'''
		self.placeControl(label, row, column, **kwargs)
	
	def create_textbox(self, name, **kwargs):
		self.__put_object(name, pyxbmct.TextBox(**kwargs))
		self.__get_object(name)._type = 'textbox'
		self.__get_object(name)._name = name
	
	def create_input(self, name, **kwargs):
		self.__put_object(name, pyxbmct.Edit('', **kwargs))
		self.__get_object(name)._type = 'input'
		self.__get_object(name)._name = name

	def create_button(self, name, text, **kwargs):
		self.__put_object(name, pyxbmct.Button(text, **kwargs))
		self.__get_object(name)._type = 'button'
		self.__get_object(name)._name = name
	
	def create_checkbox(self, name, text, **kwargs):
		self.__put_object(name, pyxbmct.RadioButton(text, **kwargs))
		self.__get_object(name)._type = 'checkbox'
		self.__get_object(name)._name = name
	
	def create_image(self, name, path, **kwargs):
		self.__put_object(name, pyxbmct.Image(path, **kwargs))
		self.__get_object(name)._type = 'image'
		self.__get_object(name)._name = name
	
	def create_progress_bar(self, name, **kwargs):
		self.__put_object(name, pyxbmct.Label(''))
		self.__get_object(name)._type = 'progress_bar'
		self.__get_object(name)._name = name	
		self.__get_object(name)._label = xbmcgui.ControlLabel (0, 0, 100, 20, '', alignment=0, font='font12')
		self.__get_object(name)._percent = xbmcgui.ControlLabel (0, 0, 100, 20, '', alignment=2, font='font10')
		
	def draw_progress_bar(self, name):
		pos_x, pos_y = self.__get_object(name).getPosition()
		self.addControl(self.__get_object(name)._label)
		self.addControl(self.__get_object(name)._percent)
		width =  int(self.__get_object(name).getWidth())
		self.__get_object(name)._label.setWidth(width)
		self.__get_object(name)._label.setPosition(pos_x + 20, pos_y-20)
		self.__get_object(name)._percent.setWidth(width)
		self.__get_object(name)._percent.setPosition(pos_x, pos_y+20)
		self.__get_object(name)._highlight_images = []
		bg = xbmcgui.ControlImage(pos_x, pos_y, 15, 24, self._skin_path + '/OSDProgressBackLeft.png', aspectRatio=0)
		self.addControl(bg)
		self.__get_object(name)._highlight_images.append(xbmcgui.ControlImage(pos_x, pos_y, 15, 24, self._skin_path + '/OSDProgressMidLeft.png', aspectRatio=0))
		self.addControl(self.__get_object(name)._highlight_images[0])
		self.__get_object(name)._highlight_images[0].setVisible(False)
		bg = xbmcgui.ControlImage(pos_x + width - 15, pos_y, 15, 24, self._skin_path + '/OSDProgressBackRight.png', aspectRatio=0)
		self.addControl(bg)
		segments = int(math.floor(((width - 30) / 10)))
		self.__get_object(name)._progress = []
		
		for n in xrange(segments):
			n += 1
			offset_x = n * 10
			bg = xbmcgui.ControlImage(pos_x + 5 + offset_x, pos_y, 10, 24, self._skin_path + '/OSDProgressBack.png', aspectRatio=1)
			self.addControl(bg)
			
			self.__get_object(name)._highlight_images.append(xbmcgui.ControlImage(pos_x + 5 + offset_x, pos_y, 10, 24, self._skin_path + '/OSDProgressMid.png', aspectRatio=1))
			self.addControl(self.__get_object(name)._highlight_images[n])
			self.__get_object(name)._highlight_images[n].setVisible(False)
			
		rest =  (width - offset_x - 30)
		self.__get_object(name)._rest_w = rest
		bg = xbmcgui.ControlImage(pos_x + 15 + offset_x, pos_y, rest, 24, self._skin_path + '/OSDProgressBack.png', aspectRatio=1)
		self.addControl(bg)
		self.__get_object(name)._highlight_images.append( xbmcgui.ControlImage(pos_x + 15 + offset_x, pos_y, rest, 24, self._skin_path + '/OSDProgressMid.png', aspectRatio=1))
		n += 1
		self.addControl(self.__get_object(name)._highlight_images[n])
		self.__get_object(name)._highlight_images[n].setVisible(False)
		n += 1
		self.__get_object(name)._highlight_images.append( xbmcgui.ControlImage(pos_x + width - 15, pos_y, 15, 24, self._skin_path + '/OSDProgressMidRight.png', aspectRatio=0))
		self.addControl(self.__get_object(name)._highlight_images[n])
		self.__get_object(name)._highlight_images[n].setVisible(False)
		self.__get_object(name)._segments = n

	def update_progress_bar(self, name, percent, label=''):
		segments = self.__get_object(name)._segments
		for n in xrange(segments+1):
			self.__get_object(name)._highlight_images[n].setVisible(False)
		width =  int(self.__get_object(name).getWidth())
		progress = percent * width
		segment_h = int(math.floor(percent * segments))
		if percent >= 1: segment_h += 1
		for n in xrange(segment_h): self.__get_object(name)._highlight_images[n].setVisible(True)
		self.__get_object(name)._label.setLabel(label)					
		self.__get_object(name)._percent.setLabel("%s %s" % (percent * 100, '%'))	
				
			
			
		
				
	def create_list(self, name, **kwargs):
		if not hasattr(self, "space"):
			space=1
		if not hasattr(self, "itemHeight"):
			itemHeight=50
		if not hasattr(self, "imageWidth"):
			imageWidth=20	
		self.__put_object(name, pyxbmct.List(_space=space, _itemHeight=itemHeight, _imageWidth=imageWidth))
		self.__get_object(name)._type = 'list'
		self.__get_object(name)._name = name
	
	def add_list_items(self, name, items, default=None, selectable=True, allow_multiple=False, allow_toggle=True, call_back=None, selection_image=None):
		if selection_image is None:
			self.__get_object(name).__selection_image = self._skin_path + 'checked.png'
		else:
			self.__get_object(name).__selection_image = selection_image
			
		self.__get_object(name).reset()
		self.__get_object(name).addItems(items)
		for index in xrange(self.__get_object(name).size()):
			self.__get_object(name).getListItem(index).setProperty('index', str(index))
		if default is not None:
			if isinstance(default, list):
				for index in default: self.set_selected(name, index)
			else:
				self.set_selected(name, default)

		def list_update():
			if selectable:
				obj = self.getFocus()
				selected_index = int(obj.getSelectedItem().getProperty('index'))
				if allow_multiple is False:
					for index in xrange(obj.size()):
						if index!=selected_index or allow_toggle is False:
							obj.getListItem(index).setIconImage("")
							obj.getListItem(index).setLabel2("unchecked")
	
				list_item = obj.getSelectedItem()
				if list_item.getLabel2() == "checked":
					list_item.setIconImage("")
					list_item.setLabel2("unchecked")
				else:
					list_item.setIconImage(self.__get_object(name).__selection_image)
					list_item.setLabel2("checked")
			
			if call_back:
				call_back()	
				
		self.connect(self.__get_object(name), list_update)
		
	
	def add_object(self, name, row, column, height=None, width=None, **kwargs):
		if None in [height, width]:
			self.placeControl(self.__get_object(name), row, column, **kwargs)
		else:
			self.placeControl(self.__get_object(name), row, column, height, width, **kwargs)
		if self.__get_object(name)._type == 'progress_bar': self.draw_progress_bar(name)	
			
			
	def get_values(self):
		values = {}
		for key in self.__objects.keys():
			values[key] = self.get_value(key)
		return values
	
	def get_value(self, key, return_text=False, return_index=False):
		if self.__get_object(key)._type in ['input', 'textbox']:
			return self.__get_object(key).getText()
		elif self.__get_object(key)._type == 'checkbox':
			return self.__get_object(key).isSelected()==1
		elif self.__get_object(key)._type == 'list':
			if return_text:
				values = []
				for index in xrange(self.__get_object(key).size()):
					if self.__get_object(key).getListItem(index).getLabel2()=='checked':
						values.append(self.__get_object(key).getListItem(index).getLabel())
			elif return_index:
				values = []
				for index in xrange(self.__get_object(key).size()):
					if self.__get_object(key).getListItem(index).getLabel2()=='checked':
						values.append(index)			
			else:
				values = [self.__get_object(key).getListItem(index).getLabel2()=='checked' for index in xrange(self.__get_object(key).size())]
			return values
	
	def set_value(self, key, value):
		if self.__get_object(key)._type in ['input', 'textbox']:
			self.__get_object(key).setText(value)
		elif self.__get_object(key)._type == 'checkbox':
			self.__get_object(key).setSelected(value)
		elif self.__get_object(key)._type == 'list':
			pass
		
	def set_selected(self, key, index):
		if self.__get_object(key)._type == 'list':
			self.__get_object(key).getListItem(index).select(True)
			#text = self.__get_object(key).getListItem(index).getLabel()
			self.__get_object(key).getListItem(index).setLabel2('checked')
			self.__get_object(key).getListItem(index).setIconImage(self.__get_object(key).__selection_image)
		else:
			pass
	def set_unselected(self, key, index):
		if self.__get_object(key)._type == 'list':
			self.__get_object(key).getListItem(index).select(True)
			#text = self.__get_object(key).getListItem(index).getLabel()
			self.__get_object(key).getListItem(index).setLabel2('unchecked')
			self.__get_object(key).getListItem(index).setIconImage('')
		else:
			pass
			
