
from webob import Response, Request
from genius.dispatcher import Dispatcher

class Genius(object):

    def __init__(self, router):
        self.dispatcher = Dispatcher(router)
        
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.dispatcher(request)
        return response(environ, start_response)