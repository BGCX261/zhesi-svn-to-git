import wsgiref.handlers

from google.appengine.ext import webapp

from home_page import HomePageHandler
from create_user_page import CreateUserPageHandler
from user_mngr_page import UserMngrPageHandler

def main():
  application = webapp.WSGIApplication(
      [('/',                 HomePageHandler),
       ('/createuser',       CreateUserPageHandler),
       ('/usermngr',         UserMngrPageHandler),
       ],
      debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
