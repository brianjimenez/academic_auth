# -*- coding: utf-8 -*-

if 0:
    from __init__ import *

import os
import datetime
import conf
import re


def index():
    """
    Landing page
    """
    return dict(num_entries=db(db.institutions.id).count())


def check_academic_email(email):
    if not email:
        return False
    else:
        try:
            email = email.lower()
            domain = email.split('@')[1]
            subdomains = domain.split('.')
            if subdomains[-1] == 'edu':
                return True
            else:
                if 'ac' in subdomains:
                    return True
                if len(subdomains) == 2:
                    num_domains = db(db.institutions.effective == domain).count()
                else:
                    to_check = []
                    for i in range(0, len(subdomains)):
                        to_check.append('.'.join(subdomains[i:]))
                    num_domains = db(db.institutions.effective.contains(to_check, all=False)).count()
                return num_domains > 0
        except:
            return False
        return False


@request.restful()
def api():
    response.view = 'generic.json'
    def GET(action, email_address):
        if not action == 'auth':
            raise HTTP(400)
        return dict(result=check_academic_email(email_address), email=email_address)

    return locals()

##################################################
##                  UTIL VIEWS
##################################################
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


##################################################
##                 ERROR VIEW
##################################################
def error():
    """
    Custom error view. Need to be mapped in routes.py
    """
    code = request.vars.code
    return dict(code=code)
