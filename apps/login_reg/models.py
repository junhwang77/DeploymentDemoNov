from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def loginValid(self, email, password):
        errors =[]
        try:
            user = Users.usermanager.get(email=email)
            password = password.encode()
            hashed_pw = user.pw_hash.encode()
            if hashed_pw == bcrypt.hashpw(password, hashed_pw):
                return(True, user)

        except ObjectDoesNotExist:
            errors.append("Incorrect Email/Password")
        return (False, errors)

    def registerValid(self, name, alias, email, password, pass_conf):
        errors = []
        if len(email) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid Email")
        elif len(name) < 2:
            errors.append("Name is required")
        elif len(alias) < 2:
            errors.append("Alias is required")
        elif len(password) < 8:
            errors.append("Password is required")
        elif password != pass_conf:
            errors.append("Passwords do not match")
        elif Users.usermanager.filter(email=email):
            errors.append("Email already being used")
        if len(errors) is not 0:
            return (False, errors)
        else:
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            e = Users.usermanager.create(email=email, name=name, alias=alias, pw_hash=pw_hash)
            e.save()
            return (True, e)


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100, null=False)
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    usermanager = UserManager()
