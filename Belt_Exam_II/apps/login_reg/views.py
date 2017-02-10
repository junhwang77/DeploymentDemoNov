from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from . import models
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if not 'errors' in request.session:
        request.session['errors'] = []
    try:
        request.session.pop('logged_id')
    except KeyError:
        pass
    return render (request, 'login_reg/index.html')

def login(request):
    if request.method == "POST":
        result = Users.usermanager.loginValid(request.POST['email'],request.POST['password'])
        if result[0]:
            request.session['alias'] = result[1].alias
            request.session['logged_id'] = result[1].id
            try:
                request.session.pop('errors')
            except KeyError:
                pass
            return redirect(reverse('quotes:index'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login_reg:index'))
    else:
        return redirect(reverse('login_reg:index'))

def create(request):
    if request.method == "POST":
        result = Users.usermanager.registerValid(request.POST['name'], request.POST['alias'],request.POST['email'], request.POST['password'], request.POST['conf_pw'], request.POST['b_date'])
        if result[0]:
            request.session['alias'] = result[1].alias
            request.session['logged_id'] = result[1].id
            try:
                request.session.pop('errors')
            except:
                pass
            return redirect(reverse('quotes:index'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login_reg:index'))
    else:
        return redirect(reverse('login_reg:index'))

def show(request, id):
    user = models.Users.usermanager.get(id=id)
    reviews = models.Users.usermanager.reviews(id)
    context = {
        'name':user.alias,
        'email':user.email,
        'reviews':reviews
    }
    return render(request, 'login_reg/show.html', context)


#def success(request):

    #return render (request, 'login_reg/success.html', {'alias': #request.session.get('alias')})
