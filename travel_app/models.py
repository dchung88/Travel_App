from django.db import models
import bcrypt
import datetime

class UserManager(models.Manager):
    def registrationValidator(self, postData):

        errors = {}
        if len(postData['form_name']) < 3:
            errors['invalidName'] = "Name must be at least 3 characters"

        if len(postData['form_username']) < 3:
            errors['invalidUsername'] = "Username must be atleast 3 characters"

        if len(postData['form_pw']) < 8:
            errors['invalidPw'] = "Password must be atleast 8 characters"

        if (postData['form_pw'] != postData['form_cpw']):
            errors['invalidPwMatch'] = "Password and Confirm Password do not match"
        
        usersWithUsername = User.objects.filter(username = postData['form_username'])
        if len(usersWithUsername) > 0:
            errors['usernameTaken'] = "username is already taken"
        print(errors)
        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['username'] = "username is required to login"
        usersWithUsername = User.objects.filter(username = postData['username'])
        print(usersWithUsername)
        if len(usersWithUsername) == 0:
            errors['noMatch'] = "This username is not registered"
        else:
            user = usersWithUsername[0]

            if bcrypt.checkpw(postData['pw'].encode(), user.password.encode()):
                print("password matches")
            else:
                errors['pwmatch'] = "incorrect password"

        return errors

    def tripValidator(self,postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['invalidDestination'] = "Destination entry is required"
        if len(postData['description']) < 1:
            errors['invalidDescription'] = "Description entry is required"
        if len(postData['from']) < 1:
            errors['invalidFrom'] = "Starting date is required"
        if len(postData['to']) < 1:
            errors['invalidTo'] = "Ending date is required"
        if postData['to'] < postData['from']:
            errors['invalidschedule'] = "Cannot have a end date before the start date"
        if postData['from'] < str(datetime.date.today()):
            errors['pasterror'] = "Cannot pick a date in the past"

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    planner = models.ForeignKey(User, related_name="plans", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()