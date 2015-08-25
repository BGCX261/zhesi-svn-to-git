import os
import urllib

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import messages
import models

class RedirectException(Exception):
  pass

class RenderCompleteException(Exception):
  pass

class NotImplementedException(Exception):
 pass

class BaseHandler(webapp.RequestHandler):
  def __init__(self):
    self.template_values = {}
    self.template_path = ''
    self.navigation_bar = []
    # user
    self.google_user = None
    self.user = None
    # post method and actions
    self.is_post = False
    self.post_action = ''

  def get(self):
    self.Run()

  def post(self):
    self.Run()

  def ProcessGet(self):
    raise NotImplementedException("Process Get not implemented")

  def ProcessPost(self):
    raise NotImplementedException("Process Post not implemented")

  def Run(self):
    try:
      if self.request.method == 'GET':
        self.is_post = False
        self.post_action = ''
        self.ProcessGet()
      elif self.request.method == 'POST':
        self.is_post = True
        self.post_action = self.request.get('post_action')
        self.ProcessPost()
      else:
        raise NotImpelementedException(
            "Unsupported request method %s" % self.request.method)
    except RedirectException:
      pass
    except RenderCompleteException:
      pass

  def RedirectAndRaise(self, uri):
    self.redirect(uri)
    raise RedirectException("Redirect to %s" % uri)

  # TODO: this function sometimes does not work
  def RedirectLogin(self):
    self.RedirectAndRaise(users.create_login_url(self.request.uri))

  def Setup(self, pagename, require_login=False, require_registered=False):
    # Check if user is logged in
    self.google_user = users.get_current_user()

    if self.google_user:
      results = models.User().all().filter('google_user =', self.google_user)
      if results.count() > 0:
        self.user = results[0]
    elif require_login:
      self.RedirectLogin()

    if require_registered:
      # If user is not logged in, redirect to login page
      if not self.google_user:
        self.RedirectLogin()
      # Check if user is registered
      if not self.user:
        # continue_url = urllib.quote(self.request.uri)
        self.RedirectAndRaise("/createuser")

    self.PreCheckOrRedirect()
    self.template_path = os.path.join(os.path.dirname(__file__), 
                                      'templates/%s' % pagename)
    self.SetupBaseTempalteValues(pagename)

  def Render(self):
    self.response.out.write(template.render(self.template_path, self.template_values))

  def JsonReturn(self, values):
    pairs = []
    for key in values.keys():
      pairs.append("'%s':'%s'" % (key, values[key]))
    message = "{%s}" % ','.join(pairs)
    self.response.out.write(message)
    raise RenderCompleteException('Complete page rendering in JsonReturn')

  # A handy function to return a json error message
  def JsonErrorReturn(self, message):
    values = {}
    values['status'] = 'error'
    values['message'] = message
    self.JsonReturn(values)

  # A handy function to return a json OK message
  def JsonSuccessReturn(self, message):
    values = {}
    values['status'] = 'OK'
    values['message'] = message
    self.JsonReturn(values)

  def SetupBaseTempalteValues(self, pagename):
    # msg.Init must be executed before any msg functions can be called.
    messages.Init(self.request.get('hl'))
    # Add template msgs
    for key, value in messages.GetMsgs().items():
      self.template_values[key] = value
    # Add base page vars
    if self.google_user:
      url = users.create_logout_url(self.request.uri)
      url_linktext = messages.Get('Logout')
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = messages.Get('Login')
    self.template_values['login_url'] = url
    self.template_values['login_url_text'] = url_linktext
    self.template_values['is_admin'] = users.is_current_user_admin()
    self.template_values['google_user'] = self.google_user
    self.template_values['user'] = self.user
    if self.user:
      self.template_values['user_name'] = self.user.nickname
    # setup navigation bar: replace the second value with the corresponding
    # messages with current locale
    self.SetupNavigationBar()
    navigations = []
    for (link, name) in self.navigation_bar:
      navigations.append((link, messages.GetMsgs()[name]))
    self.template_values['navigations'] = navigations
    self.template_values['pagename'] = messages.GetMsgs()[pagename]

  # Override this function to setup navigation bars
  def SetupNavigationBar(self):
    self.navigation_bar = []
    self.navigation_bar.append(("/", "home_page.html"))

  # Preform prechecking and redirect if failed.
  def PreCheckOrRedirect(self):
    pass

  # Return None if the param value is empty or the entity does not exist.
  def GetEntityByKeyName(self, key_name):
    entity_key = self.request.get(key_name)
    if entity_key == '':
      return None
    try:
      entity = db.get(entity_key)
      return entity
    except db.Error:
      return None

  def GetEntityOrShowError(self, key_name, message='Object not found.'):
    entity = self.GetEntityByKeyName(key_name)
    if entity == None:
      self.RedirectToErrorPage(message)
    return entity

  def GetFieldOrRedirect(self, field, uri="/"):
    value = self.request.get(field)
    if not value:
      self.RedirectAndRaise(uri)
    return value

  def Debug(self, value):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(value)
    raise RenderCompleteException('Debug page.')

  def RedirectToErrorPage(self, message):
    self.Debug(message)
