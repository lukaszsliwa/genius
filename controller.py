'''
Created on 2010-02-01

@author: crh
'''
import types

from genius.request import Render, Redirect

class Controller(object):
    '''
    Controller
    '''
    
    def __init__(self, request):
        '''
        Constructor gets request argument.
        '''
        self.request = request
        self.controller = self.__class__.__name__[:-10].lower()

    def __call__(self, action, params):
        '''
        Method gets two arguments: action (string) and params (list or dict).
        Returns response object.
        '''
        self.action = action
        try:
            if params:
                if isinstance(params, types.DictType):
                    getattr(self, action)(**params)
                elif isinstance(params, types.ListType):
                    getattr(self, action)(*params)
            else:
                getattr(self, action)()
            self.render()
        except Render as render:
            return self.view.render(**render.kwargs)
        except Redirect as redirect:
            return redirect()
        return

    def render(self, **kwargs):
        '''
        Method raises an render exception. You can use fallowing arguments:
            * format:
                render(format='json')
            * controller, action:
                render(action='index')
                render(controller='hello', action='index')
            * dict:
                render(dict={'name': 'Lucas'})
            * code with status:
                render(status=404)
                render(status='404')

        By default 'controller' is current controller name, action is current
        action name, format='html'. Dict is self.__dict__.
            
        '''
        controller = kwargs.get('controller') or self.controller
        action = kwargs.get('action') or self.action
        format = kwargs.get('format') or 'html'
        dict = kwargs.get('dict') or self.__dict__
        status = kwargs.get('code') or 200
        raise Render(controller=controller, action=action, format=format, dict=dict, status=int(status))

    def redirect(self, *args, **kwargs):
        '''
        Method raises an redirect exception. You can use fallowing calls:
            redirect('/hello')
            redirect(to='/hello')
        '''
        to = args[0] if args else kwargs['to']
        raise Redirect(to=to)
