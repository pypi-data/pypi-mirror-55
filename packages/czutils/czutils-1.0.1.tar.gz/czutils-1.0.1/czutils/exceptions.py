# -*— encoding=utf-8 -*-
#!/usr/bin/env python3

class LoadFileException(Exception):
	def __init__(self, file, err_msg):
		self._file = file
		self.err_msg = err_msg
		err = 'load file ' + file + ' ' + err_msg
		Exception.__init__(self, err)



