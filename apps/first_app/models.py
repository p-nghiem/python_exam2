from django.db import models
import sys, re
from datetime import date, datetime
# from views import *
# from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.

'''
class CourseManager(models.Manager):
    def Validator(self, postData):

        errors = {}
        course = Course.objects.filter(name = postData['name'])

#       print course
        if len(course) > 0:
            errors['exists'] = "Course already exists"
        if len(postData['name']) < 6:
            errors['name'] = "Course name must be at least 6 letters"
        if len(postData['description']) < 15:
            errors['description'] = "Description name must be at least 15 letters"
        
        return errors

class Course(models.Model):
    name = models.CharField(max_length=38)
    description = models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now = True)

    objects = CourseManager()
    '''

class UserManager(models.Manager):
    def Validator(self, postData):
        errors = {}
        #user = User.objects.get() # try this
        firstname = postData['firstname']
        lastname = postData['lastname']
        email = postData['email']
        password = postData['password']
        confirmpassword = postData['confirmpassword']
        birthday = postData['birthday']
        today = date.today()
        print ("today is", today)

        emailexists = User.objects.filter(email=email)

        if len(firstname) < 2 or firstname.isalpha() == False:        # Error first name
            errors['firstname'] = "First name must be at least 2 characters long, letters only"
        if len(lastname) < 2 or lastname.isalpha() == False:          # Error last name
            errors['lastname'] = "Last name must be at least 2 characters long, letters only"
        '''
        *** Need to validate email ***
        if not rejectEmail.match(email):                              # Error email format
            errors['email'] = "Email is not valid"
        if len(emailexists) > 0:
            errors['emailexists'] = "Email is already in use"
        '''
        # if not date.strftime(datetime.date(birthday), "%m/%d/%Y"):
        #    errors['birthdayformat'] = "Birthdate must be in the form MM/DD/YYYY" 
        # if time.strptime(birthday, "%d/%m/%Y") > time.strptime(today,"%d/%m/%Y") :
        #    errors['birthday'] = "Birthday cannot be in the future"
        # if datetime.date(birthday) > today:
        # if time.strptime(birthday, "%d/%m/%Y") > time.strptime(today,"%d/%m/%Y") :
        #   yourdatetime.date() < datetime.today().date()
        #    errors['birthday'] = "Birthday cannot be in the future"
        if len(password) < 8:                                         # Error password
            errors['passwordlength'] = "Password must be at least 8 characters long"
        if password != confirmpassword:                               # Error password match
            errors['passwordmatch'] = "Passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birthday = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = []
    
class Quote(models.Model):
    quote = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    posted_by_id = models.ForeignKey(User, related_name="quotes")
    favorited_by_users = models.ManyToManyField(User, related_name="quotes_favorited")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # def __repr__(self):
    # return "<Book object: {} {} {} {} {}>".format(self.name, self.desc, self.created_at, self.updated_at, self.uploaded_by_id)

