import types
from genius.map import Map, MapObject

class Router(object):
    '''
    Router class
    '''

    names = {
        'index': ('', 'get'),
        'new': ('new', 'get'),
        'show': (r'(.+)', 'get'),
        'edit': (r'(.+)/edit', 'get'),
        'create': ('', 'post'),
        'update': (r'(.+)', 'post'),
        'delete': (r'(.+)/delete', 'post')
    }

    def __init__(self):
        self.__get_maptree = Map()
        self.__post_maptree = Map()
        self.routes = []

    def add(self, *args, **kwargs):
        '''
        Method adds controller to router and makes a methods map
        with required request type.
        By default you can use:
            add('hello', HelloController)
        to add new routing for HelloController with prefix 'hello'.
        Method create fallowing urls:
            GET  /hello/             index
            GET  /hello/new/         new
            POST /hello/             create
            GET  /hello/(.+)/        show
            POST /hello/(.+)/        update
            GET  /hello/(.+)/edit/   edit
            POST /hello/(.+)/delete/ delete

        Of course, we can add own method to routing with argument 'methods':
            add('hello', HelloController, methods={'my': 'get'})
        then you can see:
            GET  /hello/my          my

        If need a param in path, use regular expressions:
            add('hello', HelloController, names={'my': '([a-z]+)/my'}, methods={'my': 'get'})

            GET  /hello/([a-z]+)/my     my

        Your method 'my' should be as fallow:
            def my(self, param):
                ...

        If you use (?P<name>.+) regular expression, then method should be as fallow:
            def my(self, name):
                ...

        You can use 'only' argument to select methods which should be available:
            add('hello', HelloController, only=['index'])

        Use 'names' to change the name of method. It's usefull when you use
        english method names but your url should be for example in polish:
            add('witajcie', HelloController, names={'index': 'wszyscy'}, only=['index'])

            GET /witajcie/wszyscy   index

        '''
        assert len(args) == 2, 'it should be two arguments: route name and class'
        assert isinstance(args[0], types.StringType), 'first argument should be a string'
        assert isinstance(args[1], types.TypeType), 'secound argument should be a class'
        
        name, klass = args
        klass_names = dict(self.names)
        klass_names = self.__set_methods(klass_names, **kwargs)
        klass_names = self.__set_names(klass_names, **kwargs)
        klass_names = self.__set_only(klass_names, **kwargs)
        klass_names = self.__set_hides(klass_names, **kwargs)

        self.__add_to_maps(name, klass, klass_names)

    def __set_methods(self, route_names, **kwargs):
        '''
        Method set request type for methods in 'methods'
        '''
        _route_names = dict(route_names)
        try:
            methods = kwargs['methods']
            for name, request_type in methods.items():
                if _route_names.has_key(name):
                    _route_names[name] = (_route_names[name][0], request_type)
                else:
                    _route_names[name] = (name, request_type)
            return _route_names
        except KeyError:
            return _route_names

    def __set_names(self, route_names, **kwargs):
        '''
        Method set new names of all methods in 'names'
        '''
        _route_names = dict(route_names)
        try:
            new_names = kwargs['names']
            for method_name, new_name in new_names.items():
                _route_names[method_name] = (new_name.strip('/'), _route_names[method_name][1])
            return _route_names
        except KeyError:
            return _route_names

    def __set_only(self, route_names, **kwargs):
        '''
        Method set as available all methods in 'only'
        '''
        try:
            only = kwargs['only']
            _route_names = {}
            for method_name in only:
                if route_names.has_key(method_name):
                    _route_names[method_name] = route_names[method_name]
            return _route_names
        except KeyError:
            return dict(route_names)

    def __set_hides(self, route_names, **kwargs):
        '''
        Method hides all methods in 'hide'.
        '''
        try:
            hides = kwargs['hide']
            _route_names = dict(route_names)
            for method_name in hides:
                if _route_names.has_key(method_name):
                    del _route_names[method_name]
            return _route_names
        except KeyError:
            return dict(route_names)

    def __add_to_maps(self, name, klass, klass_names):
        '''
        For all paths like (class, method_name, request_type, path)
        add to routes and {get|post}_maptree.
        '''
        for controller, action, method, path in self.__paths(name, klass, klass_names):
            self.connect(path, controller=controller, action=action, method=method)

    def __paths(self, name, klass, klass_names):
        '''
        Methods is a generator for all paths in routes.
        '''
        name = name.strip('/')
        for method_name,url in klass_names.items():
            path = '/{0}'.format(url[0]) if not name \
                else '/{0}/{1}'.format(name, url[0])
            if not path[-1] == '/':
                path += '/'
            yield klass, method_name, url[1].upper(), path

    def __getitem__(self, path_info):
        '''
        Method returns callable object for current request and path
        path_info argument should contains two strings:
                request_type path
        i.e:
                GET /hello/new
                POST /hello
        '''
        request_type, path = path_info.strip(' ').split(' ')

        if request_type.upper() == 'GET':
            return self.__get_maptree[path]
        return self.__post_maptree[path]

    def root(self, klass, **kwargs):
        '''
        Alias for adding root class.
        '''
        self.add('', klass, **kwargs)

    def resource(self, *args, **kwargs):
        '''
        Alias for add method.
        '''
        self.add(*args, **kwargs)

    def connect(self, path, **kwargs):
        '''
        Method adds a raw pattern to routes and connects with controller
        and action.
        Argument:
            * path is a path pattern
            * controller is a reference to class
            * action is a string of function name in the controller
            * method is a request type: 'get' or 'post'
        '''
        assert isinstance(path, types.StringType), 'pattern should be a string'
        assert kwargs.has_key('controller'), 'controller argument is required'
        assert isinstance(kwargs['controller'], types.TypeType), 'controller is not a Controller'
        assert kwargs.has_key('action'), 'action argument is required'
        assert isinstance(kwargs['action'], types.StringType), 'action argument is required'
        
        if kwargs.has_key('method'):
            assert isinstance(kwargs['method'], types.StringType), 'method should be a string'
            method = kwargs['method']
        else:
            method = ''
            
        controller = kwargs['controller']
        action = kwargs['action']

        if method:
            # if method is GET then add to get_maptree
            if method.upper() == 'GET':
                self.routes.append((controller, action, 'GET', path))
                self.__get_maptree[path] = MapObject(controller=controller, action=action)
            # if method is POST then add to post_maptree
            if method.upper() == 'POST':
                self.routes.append((controller, action, 'POST', path))
                self.__post_maptree[path] = MapObject(controller=controller, action=action)
        else:
            # if method is not GET and not POST then add to get_maptree and post_maptree ;)
            self.connect(path, controller=controller, action=action, method='GET')
            self.connect(path, controller=controller, action=action, method='POST')

    def __str__(self):
        output = ''
        width = max([len(a.__name__) + len(b) for a,b,c,d in self.routes]) + 2
        for klass, method_name, request_type, path in self.routes:
            output += '{0}{1}{2}\n'.format(
                '{0} {1}'.format(klass.__name__, method_name).ljust(width),
                request_type.ljust(5),
                path)
        return str(output)
        