from google.appengine.api import users
from google.appengine.ext import webapp

from models import User
from models import ProfileApplication

# Check its validity and uniqueness
def CheckUserName(name):
  return True
