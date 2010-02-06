import types

class Helper(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Contructor makes dictionary with name as key and function reference
        as value of this key.
        '''
        self.__helpers = {}

    def load(self, helper):
        '''
        Method copies all helpers from parametered helper to current helper.
        '''
        assert isinstance(helper, Helper)
        for name, func in helper.items():
            self.__setitem__(name, func)

    def __setitem__(self, name, func):
        '''
        Method adds helper to dictionary.
        '''
        assert isinstance(name, types.StringType) \
            and isinstance(func, helper)
        self.__helpers[name] = func
    
    def __getitem__(self, name):
        assert isinstance(name, types.StringType)
        return self.__helpers[name]

    def items(self):
        for name, func in self.__helpers.items():
            yield name, func

class helper(object):
    '''
    Helper decorator. Just write as fallow:
        @helper
        def hello(name): print 'Hello {0}'.format(name)

    to create hello as a helper.
    '''
    def __init__(self, func):
        self.func = func
        self.func.helper = True

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)