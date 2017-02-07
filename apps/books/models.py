from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import Users

class BookManager(models.Manager):
    def add_book_and_review(self, title, author, review, rating, logged_id, location, book_id):
        errors = []
        if len(title) == 0:
            errors.append("Title is required")
        elif len(author) < 2:
            errors.append("First name is required")
        elif location=='add':
            if Books.bookmanager.filter(title=title):
                errors.append("The book title is already registered")
        elif Reviews.bookmanager.filter(user_id=logged_id).filter(book_id=book_id):
            errors.append("You have already posted a review for this book")
        if len(errors) is not 0:
            return (False, errors)
        else:
            if location=='show':
                b = Books.bookmanager.get(title=title)
            elif location=='add':
                b = Books(title=title, author=author)
                b.save()
            r = Reviews(review=review, rating=rating)
            r.save()
            bk = Books.bookmanager.get(id=b.id)
            re = Reviews.bookmanager.get(id=r.id)
            user = Users.usermanager.get(id=int(logged_id))
            re.book_id = bk
            re.user_id = user
            re.save()
            return (True, re)

    def user(self, id):
        user = Users.usermanager.get(id=id)
        return(user)

class ReviewManager(models.Manager):
    def review(self, id):
        review = Reviews.reviewmanager.get(id=id)

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    bookmanager = BookManager()

class Reviews(models.Model):
    user_id = models.ForeignKey(Users, related_name='usertoreview', null=True)
    book_id = models.ForeignKey(Books, null=True)
    review = models.TextField(max_length=1000)
    rating = models.CharField(max_length=45, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    bookmanager = BookManager()
    reviewmanager = ReviewManager()
