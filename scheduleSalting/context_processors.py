from .settings import PORTAL_URL

def schedule_proc(request):
	d = {'key.1': 'ok',
		 'key2': 'nice'}
	protocol = request.META['wsgi.url_scheme']

	return {'PORTAL_URL': 'http://' + request.get_host(),
			'PORTAL_URL2': protocol + '://' + request.get_host()}
