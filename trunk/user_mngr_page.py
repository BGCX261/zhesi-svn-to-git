from google.appengine.api import users
from google.appengine.ext import webapp

from base_page import BaseHandler
from models import User
from models import ProfileApplication
from utils import CheckUserName

class UserMngrPageHandler(BaseHandler):
  def PreCheckOrRedirect(self):
    if not users.is_current_user_admin():
      self.RedirectAndRaise('/')

  def ProcessGet(self):
    self.Setup('user_mngr.html', require_login=True)

    self.template_values['profile_applications'] = ProfileApplication.all()
    self.template_values['all_users'] = User.all()
    
    self.Render()


  def ProcessPost(self):
    if self.post_action == 'Action.delete_application':
      self.HandleDeleteApplication()
    elif self.post_action == 'Action.approve_application':
      self.HandleApproveApplication()
    elif self.post_action == 'Action.delete_user':
      self.HandleDeleteUser()
    else:
      self.Debug('Unknown action: %s' % self.post_action)


  def HandleDeleteApplication(self):
    application = self.GetEntityOrShowError('appl_id')
    application.delete()
    self.Debug('Delete success')


  def HandleApproveApplication(self):
    application = self.GetEntityOrShowError('appl_id')
    # Step1: check it the username
    if not CheckUserName(application.nickname):
      self.Debug('invalid user name')
    # Step2: create a user and copy data from the application
    new_user = User()
    new_user.google_user = application.google_user
    new_user.nickname = application.nickname
    # Step3: fill other fields
    new_user.is_admin = False
    new_user.description = ''
    # Step4: delete the application and save the new user
    application.delete()
    new_user.put()
    self.Debug('Approve success')


  def HandleDeleteUser(self):
    user = self.GetEntityOrShowError('user_id')
    user.delete()
    self.Debug('Delete success')
