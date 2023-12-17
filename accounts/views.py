from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models  import UserModel, Verification, RideModel, Rent, DriverVerification
from .form import DriverRideForm, VerificationForm, ContactUsForm, DriverVerificationForm
from django.contrib.auth.decorators  import login_required
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def home(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def user_profile(request):
    return render(request, "profile.html")

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
            messages.success(request,"No User Found. Create an account first.")
            return redirect('login')
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
        messages.success(request, "Account created Succesfully")
        return redirect('login')

    return render(request, 'signup.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been submitted:' )
            return redirect('contactus')
        else:
            messages.success(request, 'ERROR: Message not sent.')
            return redirect('contactus')
    else:
        form = ContactUsForm()
        context= {'form': form}
    return render(request, 'contactus.html', context)

def verification(request):
    if request.method == 'POST':
            form = VerificationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit=False)
                Verification.objects.create(user_id=request.user.id, **form.cleaned_data)
                messages.success(request, 'Verification Process has been submitted....')
                return redirect( 'dashboard')
            else:
                messages.error(request, 'Verification Process submission failed....')
                return redirect( 'dashboard')
    return render(request, 'verification.html')

def driver_doc_verification(request):
    if request.method == "POST":
        form = DriverVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            DriverVerification.objects.create(user_id=request.user.id, **form.cleaned_data)
            messages.success(request, 'Driver Verification Process has been submitted....')
            return redirect( 'dashboard')
        else:
            messages.error(request, 'Driver Verification Process submission failed....')
            return redirect( 'dashboard')
    return render(request, "driverdoc.html")

@login_required
def driver(request):
    try:
        if request.user.verification.is_verified == False:
            messages.success(request,"You are not verified yet! Still pending!!!")
            return redirect('dashboard')
    except ObjectDoesNotExist:
        return redirect('verification')
    
    try:
        if request.user.driver_verification.is_verified == False:
            messages.success(request,"You are not verified as driver yet! Your driver verification is Still pending!!!")
            return redirect('dashboard')
    except ObjectDoesNotExist:
        return redirect('driverdoc')

    if request.method == 'POST':
        form = DriverRideForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.drivername = request.user
            form.save()
            messages.success(request, "You have submitted your journey form....")
            return redirect("driver")
        else:
            messages.error(request, 'Form submission failed....')
            return redirect('driver')
    else:
        form= DriverRideForm()
        context ={'form' : form}
    return render(request, 'driver.html', context) 
   

def client(request, driver_id):
    ride_object = RideModel.objects.get(id=driver_id)
    r = Rent.objects.filter(ride=driver_id, requestAccept="A")
    booked_seat = len(r)
    available_seats = ride_object.seats - booked_seat

    if request.method == "POST":
        rent = request.POST.get("rent")
        if Rent.objects.filter(
            Q(requestAccept="A") | Q(requestAccept="P"),
            user_client=request.user, 
            ride=driver_id, 
            ).exists():
            messages.success(request,"You have already booked the seat.")
            return redirect('client',driver_id=driver_id)
        else:
            Rent.objects.create(user_client=request.user, ride=ride_object, rent=rent)
            messages.success(request,"You booked a seat.")
            return redirect('client',driver_id=driver_id)
    context = {'driver': ride_object, 'available_seats': available_seats}
    return render (request, 'client.html', context)


def drivertable(request):

    try:
        if request.user.verification.is_verified == False:
            messages.success(request,"You are not verified yet! Still pending!!!")
            return redirect('dashboard')
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
    try:
        driver = get_object_or_404(RideModel, drivername=request.user)
    except:
        driver = None
 
    driver_rides = Rent.objects.filter(ride=driver).order_by("-created_on")
    context = {'driver_rides': driver_rides}
    return render(request, 'driver_rides.html', context)

def ride_request(request, id):
    ride = Rent.objects.get(id=id)
    context = {'ride': ride}
    return render(request, 'client_table.html', context)


def accept_ride_rent(request, id):
    ride_accp = Rent.objects.get(id = id)
    ride_accp.requestAccept = "A"
    ride_accp.save()
    context = {'ride_accp': ride_accp}
    return render(request, 'driver_accept.html', context)

def driver_reject(request, ride_id):
    ride_rej = get_object_or_404(Rent, id = ride_id)
    ride_rej.requestAccept = "R"
    ride_rej.save()
    # return redirect("bookedtable")
    return render(request, 'driver_reject.html')



def my_ride_detail(request):
    instance = Rent.objects.filter(user_client=request.user).order_by("-created_on")

    context = {'instance': instance}
    return render(request, "my_ride_detail.html", context)
