# -*- coding: utf8 -*-

EN_MSGS_ = {
  # base.html
  "Login" : "Sign In",
  "Logout" : "Sign Out", 
  # home_page.html
  # page names
  "home_page.html" : "home page",
  "create_user.html" : "create user",
  "user_mngr.html" : "User Management",
  # others
}


ZH_CN_MSGS_ = {
  # base.html
  "Login" : "Sign In",
  "Logout" : "Sign Out", 
  # home_page.html
  # page names
  "home_page.html" : "home page",
  "create_user.html" : "create user",
  "user_mngr.html" : "User Management",
  # others
}

CURRENT_MSGS_ = None

def Init(hl):
  global CURRENT_MSGS_
  if hl == 'en':
    CURRENT_MSGS_ = EN_MSGS_
  elif hl == 'zh-CN':
    CURRENT_MSGS_ = ZH_CN_MSGS_
  else:
    CURRENT_MSGS_ = ZH_CN_MSGS_  # default Locale

def GetMsgs():
  return CURRENT_MSGS_

def Get(msg): 
  return CURRENT_MSGS_[msg]
