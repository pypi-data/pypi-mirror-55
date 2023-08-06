import http.server
import threading
import os


class NoLogHTTPHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass


class HTTPserver_mock():
    def __init__(self,
                 listen=('localhost', 8000),
                 filename='index.html',
                 html='<html><title>testtitle</title><body><h1>hello</h1></body></html>'):
        self.listen = listen
        self.filename = filename
        self.html = html

    def __call__(self, original_func):
        decorator_self = self

        def wrappee(*args, **kwargs):
            if os.path.isfile(decorator_self.filename):
                raise Exception('File already exist:', decorator_self.filename)

            with open(decorator_self.filename, 'w') as fp:
                fp.write(decorator_self.html)

            server = http.server.HTTPServer(decorator_self.listen, NoLogHTTPHandler)
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()

            original_func(*args, **kwargs)

            server.shutdown()
            os.remove(decorator_self.filename)

        return wrappee
