from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render,redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import userform,Create_user,Login_user,Update_user,Change_pass,Forgot_pass
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import Form
from service.models import Service
from paginator.models import Paginator
#from django.core.paginator import Paginator
from register.models import Register
from visit_places_home.models import VisitPlaceHome
from cities_towns_about.models import AboutCityTown,CityPlace # city place added by me
from best_offers_about.models import BestOffersAbout
from best_offers_deals.models import BestOfferDeals
from user_reservations.models import Reservation
from payment.models import UserPayment
from django.core.mail import send_mail,EmailMultiAlternatives

from woox_travel.email_utils import send_reservation_confirmation_email #added by me
from email.mime.image import MIMEImage #same added 

from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

import random
import datetime


def homePage(request): 
    home_vist_places_data = VisitPlaceHome.objects.all()
    return render(request, "index.html",{'home_vist_places_data':home_vist_places_data})
    
def aboutPage(request):
    about_city_town_data = AboutCityTown.objects.all()
    about_best_offer_data = BestOffersAbout.objects.all()
    
    data = {
        'title':'About page',
        'about_city_town_data':about_city_town_data,
        'about_best_offer_data':about_best_offer_data,
    }
    return render(request,"about.html",data)


# add by me
# added by me


def city_detail(request, id):
    city = get_object_or_404(AboutCityTown, id=id)
    places = CityPlace.objects.filter(city=city)

    gallery_images = [city.act_img]
    if city.act_img2:
        gallery_images.append(city.act_img2)
    if city.act_img3:
        gallery_images.append(city.act_img3)
    if city.act_img4:
        gallery_images.append(city.act_img4)
    if city.act_img5:
        gallery_images.append(city.act_img5)

    data = {
        'title': city.act_city_name,
        'city': city,
        'gallery_images': gallery_images,
        'places': places,
    }
    return render(request, "city_detail.html", data)
# till here

def dealsPage(request):
    best_offer_deals_data = BestOfferDeals.objects.all()
    data = {
        'title':'Deals page',
        'best_offer_deals_data':best_offer_deals_data,
    }
    return render(request,"deals.html",data)

@login_required(login_url='login')
def reservationPage(request):
    city_town_data = AboutCityTown.objects.all()
    service_data=Service.objects.all().order_by('-service_title')
    data = {
        'title':'Reservation page',
        'service_data':service_data,
        'city_town_data':city_town_data,
    }
    return render(request,"reservation.html",data)

@login_required(login_url='login')
def bookingPage(request):
    data = {
        'title':'Booking page'
    }
    return render(request,"reservation.html",data)
                       
def paginator(request):
    paginator_data = Paginator.objects.all().order_by('paginator_title')[::-1]
    data={
        'title':'Paginator Page',
        'paginator_data':paginator_data,
    }
    return render(request,'pagintor.html',data)

def register(request):
    msg = ""
    id=0
    form = Create_user()
    if request.method == 'POST':
        form = Create_user(request.POST)
        if form.is_valid():
            form.save()
            msg = "Registered Successfully !!"
            messages.success(request,'Registered Successfully !!')
            print('Data Successfully Inserted !!')
            return redirect('/Login')
        else:
            print('Data not Successfully Inserted !')

    data = {
        'title':'Register Page',
        'msg':msg,
        'id':id,
        'form':form,
    }
    return render(request,'register.html',data)

#it will load a particular code on button click
def btnclear(request):  
    return render(request,'register.html')
        
def login_view(request):
    msg = ""
    fn = Login_user() 
    data = {'form': fn}
    if request.method == 'POST':
        fn = Login_user(request.POST)
        try:
            if fn.is_valid():
                uname = fn.cleaned_data.get('un')
                pas = fn.cleaned_data.get('password')
                user = authenticate(request, username=uname, password=pas)
                if user is not None:
                    if not user.is_staff:
                        login(request, user)
                        msg = 'Login Successful !!'
                        messages.success(request,'Login Successfull !!')
                        print('Login Successful !!')
                        data = {
                            'msg': msg,
                            'form': fn,
                        }
                        return redirect('home')
                    else:
                        return render(request,'login.html')
                else:
                    msg = "Invalid username or password !!"

            else:
                print("Form is not valid")
        except Exception as e:
            print(f"An error occurred: {e}")
            msg = f'an error occurred: {e} !!'
            messages.error(request,f'an error occurred: {e} !!')
    
    data = {
        'msg':msg,
        'form':fn
    }
    return render(request, 'login.html', data)

def forgot_pass(request):
    msg = ""
    global a 
    global mail
    if request.method=='POST':
        try:
            mail = request.POST.get('mail')
            l = User.objects.filter(email=mail)
            if l:
                global a
                a = random.randint(1000,9999)
                subject = 'WoOx Travel Password Reset OTP'
                from_mail = 'urvilvaland1789@gmail.com'
                msg = f'''<div style="margin:0;padding:0;background-color:#f4f7fb;font-family:Arial,Helvetica,sans-serif;">
      <div style="max-width:600px;margin:30px auto;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 8px 25px rgba(0,0,0,0.08);">

        <div style="background:linear-gradient(135deg,#4facfe,#00c6ff);padding:28px 24px;text-align:center;color:#ffffff;">
          <h2 style="margin:0;font-size:28px;">WoOx Travel</h2>
          <p style="margin:8px 0 0;font-size:15px;">Password Reset Verification</p>
        </div>

        <div style="padding:32px 26px;color:#333333;">
          <h3 style="margin-top:0;font-size:22px;">Hello,</h3>
          <p style="font-size:15px;line-height:1.7;margin-bottom:18px;">
            We received a request to reset your account password. Use the OTP below to continue.
          </p>

          <div style="text-align:center;margin:28px 0;">
            <div style="display:inline-block;background:#f1f8ff;border:1px dashed #4facfe;border-radius:12px;padding:16px 30px;">
              <div style="font-size:13px;color:#666;margin-bottom:8px;">Your One-Time Password</div>
              <div style="font-size:32px;letter-spacing:8px;font-weight:700;color:#007bff;">{a}</div>
            </div>
          </div>

          <p style="font-size:14px;line-height:1.7;margin-bottom:10px;">
            This OTP is valid for password reset only. Do not share it with anyone.
          </p>

          <p style="font-size:14px;line-height:1.7;color:#777777;margin-bottom:0;">
            If you did not request this, you can safely ignore this email.
          </p>
        </div>

        <div style="background:#f8f9fa;padding:16px 22px;text-align:center;color:#777;font-size:13px;">
          © 2026 WoOx Travel. Secure account recovery email.
        </div>
      </div>
    </div>  '''
                to = f'{mail}'
                sendMail = EmailMultiAlternatives(subject,msg,from_mail,[to])
                sendMail.content_subtype='html'
                sendMail.send()
                msg = f"OTP successfully send TO {mail} !!"
            else:
                msg = "User does not exist !!"
        except Exception as e:
            msg = f'an error occured{e} !!'
    return render(request,'forgot-pass.html',{'msg':msg})


def OTPvalidate(request):
    global a
    msg_ = ""
    if request.method=='POST':
        try:
            global a
            otp = int(request.POST.get('otp'))
            print(a)
            if otp==a:
                return redirect('update-pass')
            else:
                msg_ = "OTP does not match !!"
        except Exception as e:
            msg_ = f"an error occured{e}"
    return render(request,'forgot-pass.html',{'msg_':msg_})

def update_pass(request):
    global mail
    msg = ""
    if request.method == "POST":
        form = Forgot_pass(request.POST)
        if form.is_valid():
            u = User.objects.get(email=mail)
            if u:
                u.set_password(form.cleaned_data['password1'])
                u.save()
                msg = 'Your password has been successfully updated!'
                return redirect('login')  # Redirect to the login page after password update
        else:
            msg = "Password not updated. Please correct the errors below."
    else:
        form = Forgot_pass()

    data = {'form': form, 'msg': msg}
    return render(request, 'update-pass.html', data)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request,'Logout Succesfull !!')
    return redirect('login')

@login_required(login_url='login')
def change_pass(request):
    msg = ""
    if request.method=='POST':
        form = Change_pass(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            msg = "Password Succesfully Changed !!"
            return render(request,'login.html',{'msg':msg})
            
    else:
        form = Change_pass(user=request.user)
    return render(request,'change-password.html',{'form':form})


def user_reservation_get(request):
    user = request.user
    reservation_data = Reservation.objects.filter(username=user.username).order_by('-id')
    return render(request, 'your_reservations.html', {'reservation_data': reservation_data})

def user_reservation_post(request):
    try:
        name = request.POST.get('user_name')
        username = request.POST.get('username')
        price_per_person = float(request.POST.get('price_per_person'))
        number = request.POST.get('phone_number')
        number_of_guest = int(request.POST.get('number_of_guest'))
        check_in_date = request.POST.get('check_in_date')
        email = request.POST.get('email')
        city_name = request.POST.get('city_name')
        tour_dur = request.POST.get('t_dur')
        tour_des = request.POST.get('t_des')

        total_price = price_per_person * number_of_guest
        res_id = random.randint(1000000000, 9999999999)

        ur = Reservation(
            city=city_name,
            username=username,
            user_name=name,
            price_per_person=price_per_person,
            number_of_guest=number_of_guest,
            total_price=total_price,
            email=email,
            phone=number,
            check_in_date=check_in_date,
            tour_duration=tour_dur,
            tour_description=tour_des,
            reservation_id=res_id,
        )

        ur.save()

        # Get selected city data for image
        city_obj = AboutCityTown.objects.filter(act_city_name__iexact=city_name).first()

        subject = f'WoOx Travel Reservation Confirmation - {city_name}'
        from_mail = 'calmcoder2025@gmail.com'
        to = [email]

        msg = f"""
        <div style="margin:0;padding:20px;background:#f4f7fb;font-family:Arial,Helvetica,sans-serif;">
          <div style="max-width:680px;margin:20px auto;background:#ffffff;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.08);">

            <div style="background:linear-gradient(135deg,#1eaaf1,#007bff);padding:28px 24px;text-align:center;color:#ffffff;">
              <h1 style="margin:0;font-size:30px;">WoOx Travel</h1>
              <p style="margin:8px 0 0;font-size:15px;">Reservation Confirmation</p>
            </div>

            <img src="cid:city_image" alt="{city_name}" style="display:block;width:100%;height:280px;object-fit:cover;">

            <div style="padding:30px 26px;color:#333333;">
              <h2 style="margin-top:0;font-size:24px;">Hello {name},</h2>

              <p style="font-size:15px;line-height:1.8;">
                Your travel reservation has been successfully created and recorded in our system.
                Thank you for choosing <strong>WoOx Travel</strong>.
              </p>

              <div style="background:#f8fbff;border:1px solid #dcecff;border-radius:14px;padding:18px 20px;margin:24px 0;">
                <h3 style="margin:0 0 14px;font-size:18px;color:#0d6efd;">Reservation Details</h3>

                <table style="width:100%;border-collapse:collapse;font-size:14px;">
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;width:42%;">Reservation ID</td>
                    <td style="padding:10px 0;">{res_id}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Destination</td>
                    <td style="padding:10px 0;">{city_name}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Check-in Date</td>
                    <td style="padding:10px 0;">{check_in_date}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Duration</td>
                    <td style="padding:10px 0;">{tour_dur}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Guests</td>
                    <td style="padding:10px 0;">{number_of_guest}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Price Per Person</td>
                    <td style="padding:10px 0;">₹{price_per_person}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Total Price</td>
                    <td style="padding:10px 0;"><strong>₹{total_price}</strong></td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Registered Email</td>
                    <td style="padding:10px 0;">{email}</td>
                  </tr>
                  <tr>
                    <td style="padding:10px 0;font-weight:bold;">Phone Number</td>
                    <td style="padding:10px 0;">{number}</td>
                  </tr>
                </table>
              </div>

              <div style="margin-top:24px;">
                <h3 style="font-size:18px;color:#0d6efd;margin-bottom:10px;">Package Summary</h3>
                <div style="font-size:14px;line-height:1.8;color:#555555;">
                  {tour_des}
                </div>
              </div>

              <div style="margin-top:28px;padding:18px;background:#fff8e6;border:1px solid #ffe4a3;border-radius:12px;">
                <p style="margin:0;font-size:14px;line-height:1.8;color:#6b5b00;">
                  This email is a reservation confirmation for your submitted booking request.
                  Please keep it for your records.
                </p>
              </div>

              <p style="margin-top:28px;font-size:15px;line-height:1.8;">
                Regards,<br>
                <strong>WoOx Travel Team</strong>
              </p>
            </div>

            <div style="background:#f8f9fa;padding:16px 22px;text-align:center;color:#777;font-size:13px;">
              © 2026 WoOx Travel. Travel smarter, travel better.
            </div>
          </div>
        </div>
        """

        sendMail = EmailMultiAlternatives(subject, msg, from_mail, to)
        sendMail.content_subtype = 'html'

        # Attach city image inline
        if city_obj and city_obj.act_img:
            try:
                with open(city_obj.act_img.path, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<city_image>')
                    img.add_header('Content-Disposition', 'inline', filename='city.jpg')
                    sendMail.attach(img)
            except Exception as image_error:
                print("Image attach error:", image_error)

        sendMail.send()

        messages.success(request, 'Reservation Successful! Confirmation email sent.')

    except Exception as e:
        print("Reservation email error:", e)
        messages.error(request, f"An error occurred: {e}")

    return redirect('user_reservation')


def user_reservation(request):
    if request.method == 'GET':
        return user_reservation_get(request)
    elif request.method == 'POST':
        return user_reservation_post(request)


@login_required(login_url='login')
def cancel_reservation(request,rid):
    r = Reservation.objects.get(id=rid)
    r.delete()
    messages.success(request,'reservation Canceled !!')
    return redirect('user_reservation')

@login_required(login_url='login')
def edit_reservation_detail(request,rid):
    r = Reservation.objects.get(id=rid)
    city_town_data = AboutCityTown.objects.all()
    return render(request,'update_reservation_detail.html',{'r':r,'city_town_data':city_town_data})

@login_required(login_url='login')
def update_reservation_detail(request,rid):
    if request.method=='POST':
        try:
            r = Reservation.objects.get(id=rid)

            r.price_per_person = float(request.POST.get('price_per_person'))
            r.phone = request.POST.get('phone_number')
            r.number_of_guest = int(request.POST.get('number_of_guest'))
            r.check_in_date = request.POST.get('check_in_date')
            r.city = request.POST.get('city_name')
            r.tour_duration = request.POST.get('t_dur')
            r.tour_description = request.POST.get('t_des')

            r.total_price = r.price_per_person * r.number_of_guest

            r.save()
            messages.success(request, 'Reservation details updated!!')
            return redirect('user_reservation')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    return render(request,'update_reservation_details.html')

def paynow(request, rid):
    r = Reservation.objects.get(id=rid)
    
    if r.payment_status:
        messages.info(request, 'This reservation has already been paid.')
        return redirect('payment_successful', rid=rid)

    if request.method == 'POST':
        res_id = request.POST.get('res-num')
        res_user_id = request.POST.get('res-id')
        uname = request.POST.get('res-user-name')
        u_destination = request.POST.get('res-city')
        u_total_payment = request.POST.get('user-total-payment')
        u_pay_type = request.POST.get('card')
        payment_id = random.randint(10000, 99999)
        dt = datetime.datetime.now()

        if not UserPayment.objects.filter(reservation_id=res_id).exists():
            user_pay = UserPayment(
                reservation_id=res_id,
                reservation_user_id=res_user_id,
                payment_id=payment_id,
                username=uname,
                user_destination=u_destination,
                user_total_payment=u_total_payment,
                user_pay_method=u_pay_type,
                payment_time = dt,
            )
            user_pay.save()
            r.payment_status = True
            r.save()
            
            messages.success(request, 'Payment successfull !!')
        else:
            messages.warning(request, 'This reservation has already been paid.')

    return render(request, 'payment.html', {'r': r})

def payment_successful(request, rid):
    r = Reservation.objects.get(id=rid)
    p = UserPayment.objects.get(reservation_user_id=rid)
    return render(request, 'payment_successfull.html', {'r': r, 'p': p})
   


def download_invoice_pdf(request, rid):
    r = Reservation.objects.get(id=rid)
    p = UserPayment.objects.get(reservation_user_id=rid)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # Header
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(50, height - 60, "WoOx Travel")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 85, "Travel Payment Invoice")

    # Line
    pdf.line(50, height - 95, width - 50, height - 95)

    # Customer / Reservation Info
    y = height - 130
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Reservation Details")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Reservation Number: {p.reservation_id}")

    y -= 20
    pdf.drawString(50, y, f"Destination: {p.user_destination}")

    y -= 20
    pdf.drawString(50, y, f"Username: {p.username}")

    y -= 20
    pdf.drawString(50, y, f"Guest Name: {r.user_name}")

    y -= 20
    pdf.drawString(50, y, f"Email: {r.email}")

    y -= 20
    pdf.drawString(50, y, f"Phone: {r.phone}")

    y -= 20
    pdf.drawString(50, y, f"Check-in Date: {r.check_in_date}")

    y -= 20
    pdf.drawString(50, y, f"Tour Duration: {r.tour_duration}")

    y -= 20
    pdf.drawString(50, y, f"Number of Guests: {r.number_of_guest}")

    # Payment Details
    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Payment Details")

    y -= 25
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Payment ID: {p.payment_id}")

    y -= 20
    pdf.drawString(50, y, f"Payment Method: {p.user_pay_method}")

    y -= 20
    pdf.drawString(50, y, f"Payment Time: {p.payment_time.strftime('%d-%m-%Y %I:%M %p')}")

    y -= 20
    pdf.drawString(50, y, f"Price Per Person: Rs. {r.price_per_person}")

    y -= 20
    pdf.drawString(50, y, f"Total Paid Amount: Rs. {p.user_total_payment}")

    # Status Box
    y -= 40
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Payment Status: Successful")

    # Footer note
    y -= 45
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, "Thank you for choosing WoOx Travel.")
    y -= 18
    pdf.drawString(50, y, "Please keep this invoice for your booking reference.")

    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, 40, "Generated by WoOx Travel Reservation System")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    filename = f"woox_invoice_{p.reservation_id}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)