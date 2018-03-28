from django.shortcuts import render, HttpResponse, redirect # Added HttpResponse, redirect
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from random import *
import sys, re
import os, binascii
import bcrypt, hashlib # bcrypt instead of md5
from models import *
from django.contrib import messages

rejectEmail = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.

def register(request):
    if request.method == "POST":
      firstname = request.POST['firstname']
      lastname = request.POST['lastname']
      email = request.POST['email']
      password = request.POST['password']
      confirmpassword = request.POST['confirmpassword']

      errors = User.objects.Validator(request.POST)
      print errors
      if len(errors):
        for tag, error in errors.iteritems():
          messages.error(request, error, extra_tags=tag)
  #   else:
  #       Course.objects.create(name = request.POST['name'], description = request.POST['description'])

      else:  # passed validation, register user
        #password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=firstname, last_name=lastname, email=email, password=encrypted_password)
        # User.objects.Create_user(request.POST)
        print "Successful registration"
        request.session['firstname'] = firstname
        return redirect('/success')
    return redirect('/')


def login(request):
    if request.method == "POST":

        errors = {}
        print "in user login"
        email = request.POST['email']
        password = request.POST['password']
        
#       User = get_user_model()
        emailexists = User.objects.filter(email=email)


        if not rejectEmail.match(email):                              # Error email format
            errors['email'] = "Email is not valid"
            request.session['errors'] = errors
            return redirect('/')

        # Check if password match
        else:
            # encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            # password_from_db = User.objects.filter(email=email).first()
            password_from_db = User.objects.get(email=email).password
            if bcrypt.checkpw(password.encode(), password_from_db.encode()):
                # this means we have a successful login!
                print "bcrypt.checkpw = True"
                firstname = User.objects.get(email=email).first_name
                request.session['firstname'] = firstname
                request.session['user_email'] = email
                request.session['user_id'] = 1     # User.objects.get(email=email)
                print "About to redirect to /success"
                return redirect('/success')
            else:
                # invalid password! implement flash message
                errors['password'] = "Password is not valid"
                request.session['errors'] = errors
                print "Invalid password"
                return redirect('/')

    return redirect('/')


def success(request):

    firstname = request.session['firstname']
    # user_email = 'steve@gmail.com'              # debugging request.session['email']
    user_email = request.session['user_email']
#   print ("in /success, firstname:", firstname)
    print ("in /success, user_email equals:", user_email)
    user = User.objects.get(email=user_email)
    user_id = user.id
    print ("user_id equals:", user_id)

#   all_items = Item.objects.all()

    context = {
      'firstname': firstname,
      'user_email': user_email,
      'user_id': user_id,
      'all_favoritequotes': Quote.objects.filter(favorited_by_users=User.objects.get(email=user_email)),  
      'all_quotablequotes': Quote.objects.exclude(favorited_by_users=User.objects.get(email=user_email))    
    }
    print "Context is set up"
    print context

    return render(request,'quotes.html', context)



# the index function is called when root is visited

def index(request):
  '''  *** implement flash messages for errors ***
  errors = request.session['errors']
  print errors
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(request, error, extra_tags=tag)
  '''
  return render(request,'index.html')

def contribute(request):
    if request.method == "POST":
        errors = {}
        # validate item and insert in database
        author = request.POST['author']
        quote = request.POST['quote']
        user_email = request.session['user_email']
        if len(author) < 4: # raise error message
            print "Quote author's name must be more than 3 characters"
            errors['author'] = "Quote author's name must be more than 3 characters"
            request.session['errors'] = errors
            return redirect('/contribute')
        if len(quote) < 11: # raise error message
            print "Quote messae must be more than 10 characters"
            errors['message'] = "Quote messae must be more than 10 characters"
            request.session['errors'] = errors
            return redirect('/contribute')
        else:
            Quote.objects.create(author=author, quote=quote, posted_by_id=User.objects.get(email=user_email))  # match logged user)
            # optional success message  
            print "past Item.objects.create"
    return redirect('/success')   

def add(request):
    if request.method == "POST":
      print "in Add (to Favorites)"
      this_user = User.objects.get(email=request.session['user_email'])
      this_quote = Quote.objects.get(id=request.POST['quote_id'])  
      this_quote.favorited_by_users.add(this_user)
      this_quote.save()
    return redirect('/success')

def remove(request):
    if request.method == "POST":
      print "in Remove"
      this_user = User.objects.get(email=request.session['user_email'])
      this_quote = Quote.objects.get(id=request.POST['quote_id']) 
      this_quote.favorited_by_users.remove(this_user)
      this_quote.save()
    return redirect('/success')

def posts_by_user(request):  #need context
    return render(request,'postsbyuser.html')

'''
  if 'gold_total' not in request.session:
    request.session['gold_total'] = 0  
    gold_total = 0
    print 'Gold Total'
    print gold_total
  if 'activity_log' not in request.session:
    request.session['activity_log'] = {}
  
  activity_log = request.session['activity_log']
  context = {'all_activities': activity_log}
  return render(request,'index.html', context)
'''



