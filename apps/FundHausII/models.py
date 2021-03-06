from __future__ import unicode_literals

from django.db import models 
from django.db.models import F
from PIL import Image

import md5
import bcrypt
import os, binascii

import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, postData):
        messages = []
        email = postData['email']
        password = postData['password']
        if len(str(email)) < 1:
            messages.append("email must not be blank!")
        if len(str(email)) < 2:
            messages.append("email must be at least 2 characters long!")
        if len(str(password)) < 1:
            messages.append("password must not be blank")
        if len(str(password)) < 8:
            messages.append("password must be at least 8 characters long!")
        if User.objects.filter(email=email):
            # encode the password to a specific format since the above email is registered
            login_pw = password.encode()
            # encode the registered user's password from database to a specific format
            db_pw = User.objects.get(email=email).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(login_pw, db_pw):
                messages.append("Password is Incorrect!")
        else:
            messages.append("Email has already been registered!")
        return messages

    def register(self, postData):
            print "register process"
            messages = []
            firstName = postData['firstName']
            if len(str(firstName)) < 1:
                messages.append("Error! First name must not be blank!")
            if len(str(firstName)) < 2:
                messages.append("Error! First name must be at least 2 characters long!")

            lastName = postData['lastName']
            if len(str(lastName)) < 1:
                messages.append("Error! Last name must not be blank!")
            if len(str(lastName)) < 2:
                messages.append("Error! Last name must be at least 2 characters long!")

            userName = postData['userName']
            if len(str(userName)) < 1:
                messages.append("Error! User name must not be blank!")
            if len(str(userName)) < 4:
                messages.append("Error! User name must be at least 4 characters long!")

            picture = postData['picture']

            email = postData['email']
            if len(str(email)) < 1:
                messages.append("Error! Email must not be blank!")
            if len(str(email)) < 2:
                messages.append("Error! Email must be at least 2 characters long!")
            if not EMAIL_REGEX.match(email):
                messages.append("Error! Email must be in a valid format!")

            password = postData['password']
            if len(str(password)) < 1 :
                messages.append("Error! Password must not be blank!")
            if len(str(password)) < 8 :
                messages.append("Error! Password must be at least 8 characters long!")

            pwConfirm = postData['pwConfirm']
            if pwConfirm != password:
                messages.append("Error! Passwords must match")
            user_list = User.objects.filter(email=email)
            for user in user_list:
                print user.email
            if user_list:
                messages.append("Error! Email is already in the system!")
            if not messages:
                print "No messages"
                password = password.encode()
                salt = bcrypt.gensalt()
                hashed_pw = bcrypt.hashpw(password, salt)
                # password = password
                print "Create User"
                print hashed_pw
                #Added Picture field for user
                User.objects.create(firstName=firstName, lastName=lastName, userName=userName, picture=picture, email=email, password=hashed_pw)
                print hashed_pw
                print User.objects.all()
                return None
            return messages

class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    userName = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="user_image", blank=True)
    #Added Picture for User
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=25)
    pwConfirm = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
# Create your models here.

    def __unicode__(self):
        return "id: " + str(self.id) + ", First Name: " + str(self.firstName) + ", Last Name: " + str(self.lastName) + ", Username: " + str(self.userName) +  ", Picture:" + str(self.picture) + ", Email: " + str(self.email)+ ", Password:" + str(self.password)

class ProjectManager(models.Manager):
    def createproject(self, postData, first_name):
        # Don't know if I need name field listed in above line
        messages = []

        # founder = name
        # print "{} is the founder of this motherfucking project!".format(founder)

        # if self.donations == None:
        #     self.donations = 0
        # print self.donations

        title = postData['title']
        if len(str(title)) < 1:
            messages.append("Error! Title must not be blank!")
        if len(str(title)) < 10:
            messages.append("Error! Title must be at least 10 characters long!")
        
        about = postData['about']
        if len(str(about)) < 1:
            messages.append("Error! About section must not be blank!")
        if len(str(about)) < 20:
            messages.append("Error! About section must be at least 20 characters long!")

        #Adding Founder Field
        founder = User.objects.get(firstName=first_name)
        print "Founder of New Project: {}".format(founder)

        goal = postData['goal']
        if goal < 1:
            messages.append("Error! Goal must be at least $10!")

        # I deleted progress field on form - It should just be ZERO
        # progress = postData['progress']
        # print "{} is the progress".format(progress)

        if not messages:
            print "Success! No Errors!"
            Project.objects.create(title=title, founder=founder, about=about, goal=goal, progress=0, picture=postData['picture'])
            #Cannot assign "u'Von Miller'": "Project.founder" must be a "User" instance.
            return None
        return messages

class Project(models.Model):
    title = models.CharField(max_length=55)
    founder = models.ForeignKey(User, related_name="founder", null=True, blank=True)
    about = models.CharField(max_length=1000)
    goal = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="project_image", blank=True)
    # Changed Above Line to "media/project_image" instead of just /project_image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Project Title: " + str(self.title) + ", About Project: " + str(self.about) + ", Project Picture: " + str(self.picture) + ", Goal: $" + str(self.goal) + ", Progress: $" + str(self.progress)


# Brand New Donation Model To Test Out

class DonationManager(models.Manager):
    def donate(self, postData, user_id, project_id):
        messages = []
        
        # current_project = Project.objects.get(id=project_id)
        #Changing Above Query into a Donation object class QuerySet(models.QuerySet)
        current_project = Project.objects.get(id=project_id)
        print "Current Project to Donate To: {}".format(current_project)
        current_user = User.objects.get(id=user_id)
        #Changing Below Query into a Donation object class QuerySet(models.QuerySet)
        # current_user = User.objects.get(id=userid)
        print "Current User: {}".format(current_user)

        donation = postData['donation']

        #New code added 
        # donations_list = []
        if len(str(donation)) < 1:
            messages.append("Donation must be an amount greater than 0!")
        if not messages:
            # donations_list.append("Current User: " + current_user +  ", Current Donation: " + donation + "Current Project: " + current_project)
            self.create(donor=current_user, amount=donation, campaign=current_project)
            Project.objects.all().filter(id=project_id).update(progress=F('progress') + int(donation))
        return messages
        #Changed return statement to REMOVE donations list I just created

class Donation(models.Model):
    donor = models.ForeignKey(User, related_name="user_donor")
    amount = models.IntegerField(default=0, null=True)
    campaign = models.ForeignKey(Project, related_name="project_donated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DonationManager()

    def __unicode__(self):
        return "id: " + str(self.id) + ", Donor: " + str(self.donor) + ", Amount: " + str(self.amount) +  ", Campaign: " + str(self.campaign)