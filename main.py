import os
import urllib2
from xml.dom import minidom
from collections import namedtuple
import urllib2
import json
from xml.dom import minidom

import webapp2
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
        autoescape = True)
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, content):
        self.response.headers['Content-Type'] = 'application/json; character=UTF-8'
        self.write(json.dumps(content))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'):  
            self.format = 'json'
        else: 
            self.format = 'html'


### WELCOME PAGE
class WelcomePage(Handler):
    def get(self):
        self.render("welcome.html")

    def post(self):
        inpt = self.request.get('submit')
        inpt2site = {'FizzBuzz':'/fizzbuzz', 'ShoppingList':'/shopping','Rot13Encription':'/rot13','Asciichan':'/asciichan','Blog':'/blog'}
        site = inpt2site[inpt]
        self.redirect(site)

class ResumeHandler(Handler):
	def get(self):
		self.render('cv.html')

app = webapp2.WSGIApplication([
    ('/', WelcomePage),
    ('/resume', ResumeHandler)
], debug=True)