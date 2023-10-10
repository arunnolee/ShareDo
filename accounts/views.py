from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models  import UserModel, DriverModel, Verification
from .form import DriverForm, VerificationForm
from django.contrib.auth.decorators  import login_required
from django.db.models import Q

def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def logout(request):
    logout(request)
    return redirect('login')

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
    # if request.user.groups.filter(name='driver').exists():
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
    # else:
    #     return redirect('verification')

def client(request):
    return render (request, 'client.html')

def driverdoc(request):
    return render(request, 'driverdoc.html')


def table(request):
    
    records = DriverModel.objects.all()
    try:
        if request.user.verification.is_verified == True:
            if request.method == 'POST':
                search = request.POST.get('search')
                if search != None:
                    records = DriverModel.objects.filter(Q(location__contains=search) | Q(destination__contains=search)) 
        else:
            return HttpResponse("You are not verified yet!!!")
        context = {'records': records}
        return render(request, 'table.html', context)
    except:
        return redirect('verification')


# def verified_or_not(request):
#     if request.user.verification.is_verified == True:
#         return redirect('journeytable')
#     else:
#         return redirect('verification')
    
        