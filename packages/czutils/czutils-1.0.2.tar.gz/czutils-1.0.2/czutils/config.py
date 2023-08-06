# _*_ encoding=utf-8 _*_
#!/usr/bin/env python3

import configparser
from czutils.decorators import singleton

@singleton
class Config():
    def __init__( self, config_file ):
        self.config_file = config_file
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)

    def get_config( self, section, key, type='str' ):
        if type == 'int':
            return self.parser.getint(section, key)
        elif type == 'float':
            return self.parser.getfloat(section, key)
        else:
            return self.parser.get(section, key)