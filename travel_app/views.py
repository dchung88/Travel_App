from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
    return render(request, "welcome.html")

def register(request):
    print(request.POST)
    errors = User.objects.registrationValidator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    hashedpw = bcrypt.hashpw(request.POST['form_pw'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(name= request.POST['form_name'], username= request.POST['form_username'], password= hashedpw)
    request.session['loggedInUserID'] = newuser.id
    return redirect("/success")

def success(request):
    if 'loggedInUserID' not in request.session:
        errors = {
            'notloggedin': "Must login to proceed"
        }
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    loggedinuser = User.objects.get(id=request.session['loggedInUserID'])
    context = {
        'loggedinuser': loggedinuser,
        'alltrips': Trip.objects.all(),
        'mytrips': Trip.objects.filter(planner = loggedinuser) | Trip.objects.filter(users=loggedinuser),
        'othertrips': Trip.objects.exclude(Q(planner= loggedinuser) | Q(users=loggedinuser))
    }
    return render(request, "travel_dashboard.html", context)

def login(request):
    print(request.POST)
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.filter(username = request.POST['username'])
        user = user[0]
        request.session['loggedInUserID'] = user.id
    return redirect("/success")

def travelPlan(request):
    return render(request, "add_plan.html")

def addPlan(request):
    print(request.POST)
    errors = User.objects.tripValidator(request.POST)
    print(errors) 

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/travelPlan")

    loggedinuser = User.objects.get(id=request.session['loggedInUserID'])
    newtrip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], travel_date_from = request.POST['from'], travel_date_to = request.POST['to'], planner = loggedinuser)

    return redirect("/success")

def join(request, tripID):
    loggedinuser = User.objects.get(id=request.session['loggedInUserID'])
    tripToJoin = Trip.objects.get(id=tripID)
    tripToJoin.users.add(loggedinuser)
    return redirect("/success")

def destination(request, tripID):
    context = {
        'destinationDetail': Trip.objects.get(id=tripID),
    }
    return render(request, "destination.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")
