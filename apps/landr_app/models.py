from __future__ import unicode_literals

from django.db import models

from ..second_app.models import Quote
import re

import bcrypt
######### define regex ##########
# regex for email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
# regex for password
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])([a-zA-Z\d]{8})')

######### define general functions ##########
# validate if inputString has numbers in it.
def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


######### define Managers  ##########
class UserManager(models.Manager):
    def get_all_users(self):
        print "inside get_all_users"
        return self.all()

    def register_validator(self, postData):
        # perform registration checks and setup response that will be stored in session to communicate user status.
        register_response = {
            'status': False,
            'errors': {},
            'user_id': ''
        }
        # declare vars for validation checks
        entry_email = postData["email"]
        email_count = User.objects.filter(email = entry_email).count()

        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name should be at least 1 characters"
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last name should be at least 1 characters"
        if len(postData['bday']) < 1:
            errors["dob"] = "Date of Birth should be at least 1 characters"
        if has_numbers(postData["first_name"]):
            errors["first_name"] = "First name should not contain any numbers"
        if has_numbers(postData["last_name"]):
            errors["last_name"] = "Last name should not contain any numbers"
        # TO DO add .capitalize before storage

        if len(entry_email) < 1:
            errors["email"] = "Email should be at least 1 characters"
        if not EMAIL_REGEX.match(entry_email):
            errors["email_invalid"] = "Email address is invalid - Please enter a valid email"
        if email_count:
            errors["no_user"] = "Email already an account - Please Login"
        if len(postData['pw']) < 8:
            errors["email_invalid"] = "Password is invalid - Requires one uppercase, one letter, one special character and be at least 8 characters long."
        elif not PASSWORD_REGEX.match(postData['pw']):
            errors["pw_regex"] = "Password is invalid - Requires one uppercase, one letter, one special character and be at least 8 characters long"
        if postData['pw'] != postData['pwc']:
            errors["pw_match"] = "Passwords must be the same"
        if len(errors):
             register_response['errors'] = errors
        else:
            # create new user after valid
            user_pass = postData["pw"]
            bcpass = bcrypt.hashpw(user_pass.encode(), bcrypt.gensalt())
            new_user_dict = {
                'fn': postData["first_name"],
                'ln': postData["last_name"],
                'email': postData["email"],
                'pw': bcpass,
                'bday': postData['bday'],
            }
            new_user = User.objects.create(first_name= new_user_dict['fn'], last_name = new_user_dict['ln'], email = new_user_dict['email'], pw = new_user_dict['pw'], bday = new_user_dict['bday'])
            # create session to pass user ID to login page for reference
            register_response['status'] = True
            register_response['user_id'] = new_user.id
        return register_response


    def login_validator(self, postData):
        # setup helpers for validating email and password
        login_response = {
            'status': False,
            'errors': '',
            'user_id': ''
        }
        print 'inside login validator'
        entry_email = postData["login_email"]
        logging_user = User.objects.filter(email = entry_email)
        login_pass = postData["login_pw"]
        print login_pass
        print logging_user.values('pw')
        user_pass = logging_user.values('pw')
        print user_pass[0]['pw']

        # validate login info
        errors = {}
        if len(entry_email) < 1:
            errors["email"] = "Email address is invalid"
        elif not EMAIL_REGEX.match(entry_email):
            errors["email_invalid"] = "Email address is invalid"
        if not logging_user.count():
            errors["no_user"] = "No user attached to that email address"
            return errors
        # perform check against bcrypted password on server
        # FIX THIS
        elif bcrypt.checkpw(login_pass.encode(), user_pass[0]['pw'].encode()):
            errors["pw_match"] = "Please enter the correct password."

        if len(errors):
            login_response['errors'] = errors
        else:
            # request user id based on email
            login_response['status'] = True
            print logging_user.first().id
            login_response['user_id'] = logging_user.first().id
        print "Login response inside login validator", login_response
        return login_response

    # TO DO - get number of reviews posted by user

######### define Models  ##########
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bday = models.DateField(auto_now=False)
    # dob = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "Quote Desc = first_name: {} - last_name: {} - email: {}".format(self.first_name, self.last_name, self.email)