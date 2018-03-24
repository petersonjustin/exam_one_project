from django.shortcuts import render, HttpResponse, redirect
# import models
from models import User
from ..second_app.models import Quote
# import regex for validation
import re
# import messages for error warnings
from django.contrib import messages
import bcrypt


######### define initial route ##########
def index(request, user_id="1"):
    print "In Index"
    if 'user_id' not in request.session:
        request.session['user_id'] = False
    if request.session['user_id'] == True:
        return redirect('/second')
    else:
        return render(request, 'landr_app/index.html')


######### register user processing ##########
def register(request):
    print "In Register route landr"
    response = User.objects.register_validator(request.POST)
    if not response['status']:
        print 'inside register errors if'
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags='register')
        return redirect('/')
    else:
        request.session['user_id'] = response['user_id']
        # change to new
        return redirect('/second')


######### login processing ##########
def login(request, user_id="1"):
    print "in Login Route"
    response = User.objects.login_validator(request.POST)
    print response
    if len(response['errors']):
        print 'inside login errors'
        for tag, error in response['errors'].iteritems():
            messages.error(request, error, extra_tags='login')
        return redirect('/')
    else:
        print 'In Login Success Validation'
        request.session['user_id'] = response['user_id']
        # change to new
        return redirect('/second')


######### success processing ##########
def success(request):
    print "Success route landr"
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'landr_app/success.html', context)


######### success processing ##########
def logout(request):
    print "Logout landr"
    request.session['user_id'] = False
    return redirect('/')


######### define  route ##########
def user(request, user_id):
    quotes = Quote.objects.all()
    login_id= request.session['user_id']
    print "user id ", user_id
    print 'login id', login_id
    print quotes
    context = {
        'login': User.objects.get(id=login_id),
        'user': User.objects.get(id=user_id),
        'quote_count': quotes.filter(creator_id=user_id).count(),
        'quote_list': quotes.filter(creator_id=user_id)
    }
    return render(request, 'landr_app/user.html', context)