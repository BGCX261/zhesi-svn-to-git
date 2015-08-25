from google.appengine.api import users
from google.appengine.ext import webapp

from base_page import BaseHandler

class HomePageHandler(BaseHandler):
  def ProcessGet(self):
    self.Setup('home_page.html')
    self.Render()

