from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models  import UserModel, DriverModel, Verification
from .form import DriverForm, VerificationForm
from django.contrib.auth.decorators  import login_required
from .decorators import isVerifiedClient

def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def logins(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        useradmin = authenticate(request, username = username, password = password)
        if useradmin is not None:
            login(request,useradmin)
            return redirect ('dashboard')
        else:
            return HttpResponse("login failed")
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:  #checking if both password matches
            return render(request, 'signup.html', {'error': 'Password doesnot match'})
        if UserModel.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already existed'})
        if UserModel.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already existed'})
        
        UserModel.objects.create(username=username, email=email, password=make_password(password), confirm_password=make_password(confirm_password))
        return redirect('login')
        return HttpResponse('Account Created Successfully')

    return render(request, 'signup.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    return render(request, 'contactus.html')

def verification(request):
    if request.method == 'POST':
            form = VerificationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit=False)
                Verification.objects.create(user_id=request.user.id, **form.cleaned_data)
                return HttpResponse('Verification Process has been submitted....')
            else:
                return HttpResponse('Verification Process submission failed....')
    return render(request, 'verification.html')

@login_required
def driver(request):
    if request.user.groups.filter(name='driver').exists():
        if request.method == 'POST':
            form = DriverForm(request.POST)
            if form.is_valid():
                driver = form.save(commit=False)
                driver.drivername = request.user
                form.save()
                return HttpResponse('Form has been submitted....')
            else:
                print(form.errors)
                return HttpResponse('Form submission failed....')
        else:
            form= DriverForm()
            context ={'form' : form}
        return render(request, 'driver.html', context) 
    else:
        return redirect('verification')

def driverdoc(request):
    return render(request, 'driverdoc.html')

# @isVerifiedClient
def table(request):
    if request.user.verification.is_verified == True:
        records = DriverModel.objects.all()
        context = {'records': records}
        return render(request, 'table.html', context)
    else:
        return redirect('verification')
    
