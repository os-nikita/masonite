""" A StartResponseProvider Service Provider """
from masonite.provider import ServiceProvider


class StartResponseProvider(ServiceProvider):

    def register(self):
        pass

    def boot(self, Request, Response, Headers):
        if not Request.redirect_url:
            # Convert the data that is retrieved above to bytes
            # so the wsgi server can handle it.

            data = bytes(Response, 'utf-8')

            self.app.bind('StatusCode', "200 OK")
            Headers += [
                ("Content-Length", str(len(data)))
            ] + Request.get_cookies()
        else:
            self.app.bind('StatusCode', "302 OK")
            self.app.bind('Headers', [
                ('Location', Request.compile_route_to_url())
            ] + Request.get_cookies())

            Request.reset_redirections()

            self.app.bind('Response', 'redirecting ...')