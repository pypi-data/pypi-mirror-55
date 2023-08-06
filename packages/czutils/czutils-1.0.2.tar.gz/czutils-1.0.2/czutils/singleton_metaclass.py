# --*- coding: utf-8 -*-
#!/bin/bash/python3

class SingletonMetaClass(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super(SingletonMetaClass, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(SingletonMetaClass, self).__call__(*args, **kwargs)
        return self._instance