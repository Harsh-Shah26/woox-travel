"""
URL configuration for woox_travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from woox_travel import views



#
urlpatterns = [
    path('',views.homePage,name='home'),
    path('admin/', admin.site.urls),
    path('about.html/',views.aboutPage,name="about"),
    #add by me
    path('city/<int:id>/', views.city_detail, name='city_detail'),
    #till here 
    path('deals.html/',views.dealsPage,name="deals"),
    path('reservation.html/',views.reservationPage,name="reservation"),
    path('booking.html/',views.reservationPage,name="booking"),
    path('pagintor.html/',views.paginator),
    path('register.html/',views.register,name="register"),
    path('Clear/',views.btnclear,name='button-clear'),
    path('Login/',views.login_view,name='login'),
    path('forgot-pass/',views.forgot_pass,name="forgot"),
    path('otp-validate/',views.OTPvalidate,name="opt-validate"),
    path('update-pass/',views.update_pass,name="update-pass"),
    path('Logout/',views.logout_view,name='logout'),
    path('Chaneg-password/',views.change_pass,name='change-pass'),
    path('user_reservation/',views.user_reservation,name='user_reservation'),
    path('cancel_reservation/<int:rid>',views.cancel_reservation,name='cancel-reservation'),
    path('edit_reservation/<int:rid>',views.edit_reservation_detail,name="edit_reservation_detail"),
    path('edit_reservation/update_reservation/<int:rid>',views.update_reservation_detail,name="update_reservation_detail"),
    path('payment/<int:rid>',views.paynow,name='paynow'),
    path('payment-successful/<int:rid>/', views.payment_successful, name='payment_successful'),
    path('download-invoice/<int:rid>/', views.download_invoice_pdf, name='download_invoice_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)