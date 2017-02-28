from django.shortcuts import render, redirect, HttpResponse
from .models import User, Favorite, Quote
import bcrypt
from django.contrib import messages
def index(request):

    return render(request, 'main/index.html')

def success(request):
    ids=[]
    favs = Favorite.objects.filter(added_by = request.session['id'])
    for fav in favs:
        ids.append(fav.quote_id.id)
        print ids
    my_favorites = Favorite.objects.filter(added_by = request.session['id'])
    other_quotes = Quote.objects.exclude(id__in=ids)

    context ={
        'my_favorites': my_favorites,
        'other_quotes': other_quotes
    }
    return render(request, 'main/success.html', context)

def create(request):
    if User.objects.registration(request.POST):

        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    else:
        messages.error(request, "Registration Error")

    return redirect('/')

def login(request):
    if User.objects.login(request.POST):
        identify = User.objects.get(email=request.POST['email_login'])
        request.session['id'] = identify.id
        request.session['first_name'] = identify.first_name
        return redirect('/success')
    else:
        messages.error(request, "Login Error")
        return redirect('/')

def create_quote(request):
    if len(request.POST['author']) < 3 :
        messages.error(request, "Author Must Be Three Characters Long")
        return redirect('/success')

    if len(request.POST['quote_text']) < 10:
        messages.error(request, "Quote Must Be 10 Characters Long")
        return redirect('/success')
    else:
        Quote.objects.create(quote=request.POST['quote_text'], author=request.POST['author'], creator=User.objects.get(id = request.session['id']))
    return redirect('/success')

def user_page(request, id):
    username = Quote.objects.filter(creator = id).first()
    userinfo = Quote.objects.filter(creator = id)
    precount = Quote.objects.filter(creator = id)
    count = len(precount)
    context = {
        'count' : count,
        'userinfo': userinfo,
        'username': username
    }
    return render(request, 'main/user_page.html', context)

def add_favorite(request, id):
    Favorite.objects.create(quote_id = Quote.objects.get(id = id), added_by = User.objects.get(id=request.session['id']))
    return redirect('/success')

def del_favorites(request, id):
    Favorite.objects.get(id = id).delete()
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')
