from webob import Response

class Render(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, name):
        return self.kwargs[name]

class Redirect(Exception):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, name):
        return self.kwargs[name]
    
    def __call__(self):
        response = Response()
        response.location = self.to
        response.status_int = 303
        return response