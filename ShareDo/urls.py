"""
URL configuration for ShareDo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', views.home, name= 'homepage'),
    path('aboutus/', views.aboutus, name= 'aboutus'),
    path('contactus/', views.contactus, name= 'contactus'),
    path('login/', views.logins, name= 'login'),
    path('logout/',views.logout_user, name='logout'),
    path('signup/', views.signup, name= 'signup'),
    path('dashboard/', views.dashboard, name= 'dashboard'),
    path('documentupload/', views.verification, name= 'verification'),
    path('driverform/', views.driver, name= 'driver'),
    path('driverdocumentupload/', views.driverdoc, name= 'driverdoc'),
    path('journeytable/', views.drivertable, name= 'journeytable'),
    path('clientform/<int:driver_id>/', views.client, name= 'client'),
    path('bookedtable/', views.ride_table, name= 'bookedtable'),
    path('ride-request/<int:id>/', views.ride_request, name= 'ride_request'),
]
