'''
Created on 2010-02-01

@author: crh
'''

import genius.helper
import jinja2
from webob import Response
import types

class View(object):

    def __init__(self, *args, **kwargs):
        assert kwargs.has_key('views_path')
        if kwargs.has_key('helpers'):
            assert isinstance(kwargs['helpers'], genius.helper.Helper)
        self.views_path = kwargs['views_path']
        self.engine = Jinja2(*args, **kwargs)

    def render(self, controller, action, format, status, dict):
        '''
        Method gets fallowing arguments: controller, action, format, code, dict
        '''
        template = '{0}/{1}.{2}'.format(controller, action, format)
        content = self.engine.render(template=template, dict=dict)
        response = Response()
        response.status_int = status
        response.unicode_body = content
        return response

class TemplateEngine(object):
    '''
    TemplateEngine's class should be implemented by all available template engines.
    '''
    def __init__(self, *args, **kwargs):
        raise NotimplementedError

    def render(self, *args, **kwargs):
        raise NotImplementedError

class Jinja2(TemplateEngine):
    '''
    Jinja2TemplateEngine
    '''
    def __init__(self, *args, **kwargs):
        assert kwargs.has_key('views_path')
        assert isinstance(kwargs['views_path'], types.StringType)
        self.views_path = kwargs['views_path']
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(kwargs['views_path']),
            line_statement_prefix='%',
            variable_start_string="{{",
            variable_end_string="}}"
        )

        self.__load_default_helpers()
        
        if kwargs.has_key('helpers'):
            for name,func in kwargs['helpers'].items():
                print name, func
                self.environment.globals[name] = func

    def __load_default_helpers(self):
        import genius.helpers as helpers
        for name,func in helpers.__dict__.items():
            if isinstance(func, genius.helper.helper):
                self.environment.globals[name] = func

    def render(self, **kwargs):
        '''
        Method gets excatly two arguments: template, text and returns content.
        '''
        if kwargs.has_key('template') and kwargs.has_key('dict'):
            return self.__render_template(kwargs['template'], kwargs['dict'])
        elif kwargs.has_key('text'):
            return self.__render_text(kwargs['text'])

    def __render_text(self, text):
        return self.environment.from_string(text).render({})

    def __render_template(self, template, dict):
        return self.environment.get_template(template).render(dict)
        