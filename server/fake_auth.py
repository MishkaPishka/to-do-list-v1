#FAKE AUTH PAGE
import functools

from werkzeug import Request


def auth_decorator():
    def _auth_decorator(f):
        @functools.wraps(f)
        def __auth_decorator(*args, **kwargs):
            # just do here everything what you need
            print("AUTH DECORATOR - ARGS:{},KWARGS:{}".format(args,kwargs))
            result = f(*args, **kwargs)
            print("AUTH DECORATOR - result:{}".format(result))

            return result

        return __auth_decorator

    return _auth_decorator



def check_credentials():
    return True

class Middleware:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)
        print("IN MIDDLEWERE ")
        print('path: %s, url: %s' % (request.path, request.url))
        # just do here everything what you need
        return self.app(environ, start_response)

