import types
import re

class MapObject(object):
    '''
    MapObject class contains an object for Map class.
    '''
    def __init__(self, controller, action, params=[]):
        self.controller = controller
        self.action = action
        self.params = params

    def __eq__(self, other):
        try:
            return self.controller == other.controller \
                and self.action == other.action \
                    and self.params == other.params
        except:
            return False
        
    def __ne__(self, other):
        return not self.__eq__(other)

class Map(object):
    '''
    Map class is storing paths in a dictionary tree
    '''
    def __init__(self):
        self.__map = {}

    def __getitem__(self, path):
        '''
        Method returns a MapObject for given path.
        '''
        if not path: raise KeyError('empty path')
        if not path.endswith('/'):
            path += '/'

        if self.__map.has_key(path):
            return self.__map[path]

        for patterns in self.__map.keys():
            if self.__match(patterns, path):
                params = self.__params(patterns, path)
                obj = self.__map[patterns]
                obj.params = params
                return obj
        return None

    def __match(self, pattern, path):
        patterns = pattern.split('/')
        groups = path.split('/')
        if len(patterns) != len(groups):
            return False
        for pattern,group in zip(patterns, groups):
            pg = re.match(r'^{0}$'.format(pattern), group)
            if not pg:
                return False
        return True

    def __params(self, pattern, group):
        patterns = pattern.split('/')
        groups = group.split('/')
        assert len(patterns) == len(groups)
        def str2int(val):
            '''
            Convert val to int or unicode.
            '''
            try:
                return int(val)
            except ValueError:
                return str(val)
        param_args = []
        param_kwargs = {}
        for pattern,group in zip(patterns, groups):
            pg = re.match(r'^{0}$'.format(pattern), group)
            assert pg
            if pg.groupdict():
                param_kwargs.update(pg.groupdict())
            elif pg.groups():
                param_args += pg.groups()
        param_kwargs = dict([(key, str2int(value)) for key,value in param_kwargs.items()])
        param_args = map(str2int, param_args)
        return param_kwargs or param_args


    def __setitem__(self, path, instance):
        '''
        Method sets callable object for given path.
        '''
        if not path: raise KeyError('empty path')
        if not path.endswith('/'):
            path += '/'
        self.__map[path] = instance
