from __future__ import unicode_literals

from django.db import models
# from ..landr_app.models import User
# import regex for validation
import re
# import messages for error warnings
from django.contrib import messages




######### define Managers  ##########
class FavoriteManager(models.Manager):
    def get_all_favorites(self):
        print "inside get_all_favorites."
        return self.all()


class QuoteManager(models.Manager):
    def get_all_quotes(self):
        print "inside get_all_quotes"
        return self.all()

    # def quote_validator(self, postData):
    #     quote_valid_response = {
    #         'status': False,
    #         'errors': {},
    #         'user_id': ''
    #     }
    #     # declare vars for validation checks


#     return quote_valid_response

    def quote_create(self, postData):
        author = postData["author"]
        desc = postData["desc"]
        # quote_valid_response = {
        #     'errors': {}
        # }
        # errors = {}
        # if len(author) < 3:
        #     errors["author"] = "Author should be at least 3 characters"
        # if len(desc) < 10:
        #     errors["desc"] = "Quote should be at least 10 characters"

        # if len(errors):
        #     quote_valid_response['errors'] = errors
        #     return quote_valid_response
        # else:
        #     print "in quote create"
        creator = postData['user_id']
        new_author_dict = {
            'author': author,
            'desc': desc,
            'creator': creator
        }
        #     return new_quote
        new_quote = Quote.objects.create(desc = new_author_dict['desc'], author = new_author_dict['author'], creator_id = new_author_dict['creator'])

    def favorite_a_quote(self, postData):
        # get the quote id
        print 'Inside Favorite a quote'
        quote_id = postData['quote_id']
        user = postData['user_id']
        print quote_id
        print user
        new_favorite = {
            'quote_id': quote_id,
            'user': user
        }
        return new_favorite

    def remove_a_quote(self, postData):
        this_quote = postData['quote_id']
        user = postData['user_id']
        quote_tb_removed = {
            'quote_id': this_quote,
            'user': user
        }
        return quote_tb_removed

######## define Quotes Models  ##########
class Quote(models.Model):
    desc = models.TextField(default="A Sample quote by someone")
    # a user can have many quotes but a quote can only have one user that created it.
    creator = models.ForeignKey('landr_app.User', related_name="quote_creator")# working
    # each quote can have many users favorite it
    author = models.CharField(max_length=255) # working
    # users can have many favorite quotes and each quote can be favorited by many users
    favorites = models.ManyToManyField('landr_app.User', related_name="quotes_favorited")
    created_at = models.DateTimeField(auto_now_add=True)# working
    updated_at = models.DateTimeField(auto_now=True)# working
    # UserT = models.ForeignKey('landr_app.User')
    objects = QuoteManager()# working
    def __repr__(self):
        return "Quote Desc = desc: {} - creator: {} - author: {}".format(self.desc, self.creator, self.author)





