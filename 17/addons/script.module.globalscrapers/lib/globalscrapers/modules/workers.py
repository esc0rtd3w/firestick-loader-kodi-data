# -*- coding: UTF-8 -*-
#01010011 01001111 01001100 01001001 01000100 00100000 01010011 01001110 01000001 01001011 01000101 00100000


import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

