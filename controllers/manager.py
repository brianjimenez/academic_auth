# -*- coding: utf-8 -*-

if 0:
    from __init__ import *


@auth.requires_membership('manager')
def index():
    return dict()

@auth.requires_membership('manager')
def institutions():
    grid = SQLFORM.smartgrid(db.institutions, orderby=[~db.institutions.id])
    return dict(grid=grid)
