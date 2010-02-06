'''
Created on 2010-02-01

@author: crh
'''

class Dispatcher(object):

    def __init__(self, router):
        self.router = router

    def __call__(self, request):
        map_object = self.router['{0} {1}'.format(request.method, request.path_info)]
        if map_object:
            controller = map_object.controller(request)
            return controller(action=map_object.action, params=map_object.params)
        return