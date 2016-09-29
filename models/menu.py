# -*- coding: utf-8 -*-

if 0:
    from __init__ import *

response.title = ' '.join(
    word.capitalize() for word in request.application.split('_'))

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Protein Interactions and Docking Group'
response.meta.description = 'A REST API for academic authentication'
response.meta.keywords = 'academic auth'
response.meta.generator = 'Barcelona Supercomputing Center'

## your http://google.com/analytics id
response.google_analytics_id = 'UA-58599215-1'

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

if auth.is_logged_in():
    response.menu.append((T('Manager'), False, URL('manager', 'index')))
