from django.shortcuts import render, HttpResponse, redirect
from . import models
from models import Books, Reviews
from django.core.urlresolvers import reverse
from django.db.models import Count


def index(request):
    books = models.Books.bookmanager.all()
    reviews = models.Reviews.bookmanager.all().order_by('-id')[:3]
    try:
        request.session.pop('errors')
    except:
        pass
    context = {
        'books':books,
        'reviews':reviews
    }
    return render(request, 'books/index.html', context)

def add(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
    books = models.Books.bookmanager.all()
    context = {
        'books':books
    }
    return render(request, 'books/add.html', context)

def addreview(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        result = Reviews.bookmanager.add_book_and_review(request.POST['title'], request.POST['author'], request.POST['review'], request.POST['rating'], request.POST['logged_id'], request.POST['location'], request.POST['book_id'])
        if result[0]:
            try:
                request.session.pop('errors')
            except:
                pass
            book = models.Books.bookmanager.get(title=request.POST['title'])
            request.session['book_id']=book.id
            return redirect(reverse('books:show', kwargs={'id':book.id}))
        else:
            request.session['errors'] = result[1]
    if 'show' == request.POST['location']:
        book = models.Books.bookmanager.get(title=request.POST['title'])
        request.session['book_id']=book.id
        return redirect(reverse('books:show', kwargs={'id':book.id}))
    else:
        return redirect(reverse('books:add'))


def show(request, id):
    request.session['int_id']=int(request.session['logged_id'])
    book = models.Books.bookmanager.get(id=id)
    reviews = models.Reviews.bookmanager.filter(book_id=id)
    context = {
        'reviews':reviews,
        'title':book.title,
        'author':book.author,
        'id':book.id,
    }
    return render(request, 'books/show.html', context)

def user(request, id):
    user = models.Reviews.bookmanager.user(id)
    books = models.Reviews.bookmanager.filter(user_id=id)
    bks = models.Reviews.bookmanager.filter(user_id=id).count()
    context = {
        'user':user,
        'books':books,
        'bks':bks
    }
    return render(request, 'books/user.html', context)

def delete(request, id):
    request.session['logged_id']=request.POST['logged_id']
    r = models.Reviews.bookmanager.get(id=id)
    r.delete()
    try:
        request.session.pop('errors')
    except:
        pass
    return redirect(reverse('books:show', kwargs={'id':request.POST['book_id']}))

def remove(request, id):
    request.session['logged_id']=request.POST['logged_id']
    r = models.Reviews.bookmanager.filter(book_id=id)
    r.delete()
    b = models.Books.bookmanager.get(id=id)
    b.delete()
    return redirect(reverse('books:index'))
#def show(request):
    #return render(request, 'books/show.html')
# Create your views here.
