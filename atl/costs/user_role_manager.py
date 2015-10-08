# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab
from django.db import models
from django.contrib.auth.models import User, Group
from atl.costs.models import *


def getUserProjectList(User):
    user = User.get()
    userprojectrole = user.userroleproject_set.all()[0]
    projectlist = [x.code for x in  userprojectrole.project.all()]
    return projectlist

def getUserProjectRole(User):
    user = User.get()
    userprojectrole = user.userroleproject_set.all()[0]
    return userprojectrole.role.role