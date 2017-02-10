from __future__ import unicode_literals
from ..login_reg.models import Users
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def add_user_to_quote(self, author, quote, logged_id):
        errors = []
        if len(author) == 0:
            errors.append("Quoted By: is required")
        if len(quote) == 0:
            errors.append("Message is required")
        if len(errors) is not 0:
            return (False, errors)
        else:
            q = Quotes(author=author, quote=quote)
            q.save()
            print q.id
            quot = Quotes.usermanager.get(id=q.id)
            user = Users.usermanager.get(id=logged_id)
            quot.user_id = user
            quot.save()
            return (True, q)

    def join_quote_to_fav(self, logged_id, id):
        q = Quotes.usermanager.get(id=id)
        u = Users.usermanager.get(id=logged_id)
        q.fav_id.add(u)
        return (True, q)

class Quotes(models.Model):
    user_id = models.ForeignKey(Users, related_name='usertoquote', null=True)
    fav_id = models.ManyToManyField(Users, related_name='usertofav')
    author = models.CharField(max_length=45)
    quote = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    usermanager = UserManager()
