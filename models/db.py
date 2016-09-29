# -*- coding: utf-8 -*-

if 0:
    from __init__ import *

from db_conf import connection_url

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL(connection_url,
         pool_size=1, check_reserved=['all'], lazy_tables=False,
         migrate_enabled=True, fake_migrate_all=False)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

from gluon.tools import Auth, Crud, Service, PluginManager
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True)

## configure auth policy
auth.settings.actions_disabled.append('register')
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

## Table definitions
db.define_table('institutions',
                Field('institution'),
                Field('sld'),
                Field('tld'),
                Field('effective'),
                format='%(institution)s - %(effective)s',
                singular='Institution', plural='Institutions')

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)
