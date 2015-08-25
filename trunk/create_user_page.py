from google.appengine.api import users
from google.appengine.ext import webapp

from base_page import BaseHandler
from models import ProfileApplication
from models import User
from utils import CheckUserName

class CreateUserPageHandler(BaseHandler):
  def PreCheckOrRedirect(self):
    users = User.all().filter("google_user =", self.google_user)
    if users.count() > 0:
      self.RedirectAndRaise('/')

  def ProcessGet(self):
    self.Setup('create_user.html', require_login=True)

    applications = ProfileApplication.all().filter("google_user =",
                                                   self.google_user)
    if applications.count() > 0:
      self.template_values['allow_create_user'] = False
      self.template_values['existing_application'] = applications[0]
    else:
      self.template_values['allow_create_user'] = True
    
    self.Render()


  def ProcessPost(self):
    self.Setup('create_user.html', require_login=True)

    application = ProfileApplication()
    application.google_user = self.google_user
    application.nickname = self.request.get('nickname')
    # Check its validity and uniqueness
    if not CheckUserName(application.nickname):
      self.RedirectAndRaise('/')
    else:
      application.put()
    # done
    self.RedirectAndRaise('/createuser')

