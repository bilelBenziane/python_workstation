

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from updown.resources import app as updown
from updown_client.application import app as updown_client

application = DispatcherMiddleware(updown, {
    '/updown/client': updown_client
})
if __name__ == '__main__':
    run_simple('localhost', 5000, application,
               use_reloader=True, use_debugger=True, use_evalex=True)
			   
		