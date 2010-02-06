'''
This file contains default helpers. Helper should be decored by 'helper' decorator.
'''

from genius.helper import helper

@helper
def hello(name):
    return 'Hello {0}'.format(name)
