import os
import cgi
import logging
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson as json
from google.appengine.api import urlfetch


KLOUT_API_KEY = ''

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

class HowMany(webapp.RequestHandler):
    def post(self):
		dan_url = "http://api.klout.com/1/users/show.json?key="+ KLOUT_API_KEY +"&users=dannomatic"
		your_url = "http://api.klout.com/1/users/show.json?key="+ KLOUT_API_KEY +"&users=" + cgi.escape(self.request.get('username'))

		dan = urlfetch.fetch(dan_url).content
		you = urlfetch.fetch(your_url).content
		
		dan = json.loads(dan)
		you = json.loads(you)
		
		try:
			dan_score = dan['users'][0]['score']['kscore']
			your_score = you['users'][0]['score']['kscore']
		
			num_dans = round(your_score / dan_score, 2)
		except KeyError:
			num_dans = 0
		
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps({'dans': num_dans}))


def main():
    application = webapp.WSGIApplication([('/', MainPage), ('/howmany', HowMany)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
