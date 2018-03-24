from django.shortcuts import render, HttpResponse, redirect


from ..landr_app.models import User
from models import Quote
from django.contrib import messages

# Create your views here.
######### define initial route ##########
def index(request): # DONE!
    quotes = Quote.objects.all()
    user_id = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user_id,
        'quotes': quotes,
        'favorited_quotes': Quote.objects.filter(favorites=user_id),
        'non_favorited_quotes': Quote.objects.exclude(favorites=user_id)
    }
    return render(request, 'second_app/home.html', context)


def create_quote(request):# DONE!

    response = Quote.objects.quote_create(request.POST)
    # if len(response['errors']):
    #     print 'inside comment errors if'
    #     for tag, error in response['errors'].iteritems():
    #         messages.error(request, error, extra_tags='register')
    #     return redirect('/second')
    # else:
    # new_quote = Quote.objects.quote_create(request.POST)
        # change to new
    return redirect('/second')


def add_favorite(request):# DONE!
    print 'Inside Favorite a quote'
    new_favorite = Quote.objects.favorite_a_quote(request.POST)
    quote_key = Quote.objects.get(id=new_favorite['quote_id'])
    user_key = User.objects.get(id=new_favorite['user'])
    quote_key.favorites.add(user_key)
    return redirect('/second')


def remove_favorite(request):
    new_favorite = Quote.objects.favorite_a_quote(request.POST)
    quote_key = Quote.objects.get(id=new_favorite['quote_id'])
    user_key = User.objects.get(id=new_favorite['user'])
    quote_key.favorites.remove(user_key)


    # select the id of the favorite and delete on cascade
    # context = {
    #     'user': User.objects.get(id=request.session['user_id']),
    #     'quotes': quotes
    # }
    return redirect('/second')



