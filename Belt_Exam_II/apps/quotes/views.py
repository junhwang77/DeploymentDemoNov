from django.shortcuts import render, redirect, HttpResponse
from .models import Quotes
from . import models
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
    all_quotes = Quotes.usermanager.all().exclude(fav_id=request.session['logged_id'])
    fav_quotes = Quotes.usermanager.filter(fav_id=request.session['logged_id'])
    context={
        'all_quotes':all_quotes,
        'fav_quotes':fav_quotes,
    }
    return render(request, 'quotes/index.html', context)

def create(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        result = Quotes.usermanager.add_user_to_quote(request.POST['author'], request.POST['quote'], request.POST['logged_id'])
        if result[0]:
            try:
                request.session.pop('errors')
            except:
                pass
            return redirect(reverse('quotes:index'))
        else:
            request.session['errors'] = result[1]
        return redirect(reverse('quotes:index'))
    else:
        return redirect(reverse('quotes:index'))

def join(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        result =  Quotes.usermanager.join_quote_to_fav(request.POST['logged_id'], request.POST['id'])
        return redirect(reverse('quotes:index'))

def remove(request):
    if request.method == 'POST':
        request.session['logged_id']=request.POST['logged_id']
        r = Quotes.usermanager.get(id=request.POST['quote_id'])
        r.fav_id.remove(request.POST['logged_id'])
        return redirect(reverse('quotes:index'))

def show(request, id):
    request.session['logged_id']
    quotes = Quotes.usermanager.get(id=id)
    userq = Quotes.usermanager.filter(user_id=id).count()
    all_quotes = Quotes.usermanager.filter(user_id=id)
    context = {
        'alias':quotes.user_id.alias,
        'userq':userq,
        'all_quotes':all_quotes
    }
    return render(request, 'quotes/show.html', context)
