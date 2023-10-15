from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models  import UserModel, Verification, RideModel
from .form import DriverRideForm, VerificationForm, ClientRideForm
from django.contrib.auth.decorators  import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def logout_user(request):
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
        # return HttpResponse('Account Created Successfully')

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
    try:
        if request.user.verification.is_verified == False:
            return HttpResponse("You are not verified yet! Still pending!!!")
    except ObjectDoesNotExist:
        return redirect('verification')
    
    if request.method == 'POST':
        form = DriverRideForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.drivername = request.user
            form.save()
            return HttpResponse('Form has been submitted....')
        else:
            print(form.errors)
            return HttpResponse('Form submission failed....')
    else:
        form= DriverRideForm()
        context ={'form' : form}
    return render(request, 'driver.html', context) 
   

def client(request, driver_id):
    if request.method == 'POST':
        form = ClientRideForm(request.POST)
        if form.is_valid():
            # client = form.save(commit=False)
            # client.clientname = request.user
            # form.save()
            RideModel.objects.update(clientname=request.user, **form.cleaned_data)
            return HttpResponse('Your Ride has been booked ...')
        else:
            print(form.errors)
            return HttpResponse('Ride Booking is failed.')
    else:
        driver = RideModel.objects.get(id=driver_id)
        form = ClientRideForm()
        context = {
            'driver':driver,
            'form': form }
    return render (request, 'client.html', context)

def driverdoc(request):
    return render(request, 'driverdoc.html')


def drivertable(request):
    """
    list of destinattion.
    """
    try:
        if request.user.verification.is_verified == False:
            return HttpResponse("You are not verified yet! Still pending!!!")
    except ObjectDoesNotExist:
        return redirect('verification')
    
    records = RideModel.objects.exclude(drivername=request.user)
    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            records = RideModel.objects.filter(Q(location__contains=search) | Q(destination__contains=search))

    context = {'records': records}
    return render(request, 'driver_table.html', context)

def ride_table(request):
    driver_rides = RideModel.objects.filter(drivername=request.user)
    context = {'driver_rides': driver_rides}
    return render(request, 'driver_rides.html', context)


def ride_request(request, id):
    ride = RideModel.objects.get(id=id)
    context = {'ride': ride}
    return render(request, 'client_table.html', context)