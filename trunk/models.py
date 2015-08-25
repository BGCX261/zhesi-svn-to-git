from google.appengine.ext import db
from google.appengine.api import users

class User(db.Model):
  # Google account user
  google_user = db.UserProperty()
  # Nick name is unique in this app
  nickname = db.StringProperty(multiline=False)
  # User types
  is_sys_admin = db.BooleanProperty()
  # Profile
  description = db.StringProperty(multiline=True)


class ProfileApplication(db.Model):
  # Google account user
  google_user = db.UserProperty()
  # Nick name to apply
  nickname = db.StringProperty(multiline=False)
