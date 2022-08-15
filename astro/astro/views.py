from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from astro.astro.serializers import UserSerializer, GroupSerializer

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.views.generic import View, CreateView, ListView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from astro.astro.forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token, password_reset_token
from django.core.mail import EmailMessage
import json
from datetime import datetime
from datetime import date
import calendar

#import requests
from os import walk
import os  
import random

import locale

def algorithm_run(left_arr,center_arr,right_arr,left,right):
    for i in range(1,9):
        #image1={'image1':"images/Empty.png"}
        #image2={'image2':"images/Empty.png"}
        if left==True:
           left_arr['x1'+str(i)]=str(random.randint(1, 15))
           #image1={'image1':random.choice(['images/fire.png', 'images/earth.png', 'images/water.png','images/air.png'])}
        if right==True:
           right_arr['x2'+str(i)]=str(random.randint(1, 15))
           #image2={'image2':random.choice(['images/fire.png', 'images/earth.png', 'images/water.png','images/air.png'])}
        if left==True or right==True:
           center_arr['x3'+str(i)]=str(random.randint(1, 15))
        #print(left_arr)
        #print(right_arr)
        #print(center_arr)
#     left_arr=[random.randint(1, 8) for i in range (1,8)]
#     center_arr=[random.randint(1, 8) for i in range (1,8)]
#     right_arr=[random.randint(1, 8) for i in range (1,8)]
    return {**left_arr,**center_arr,**right_arr}
# def index(request):
#     return render(request, 'index.html')

months_num={
1:"Январь",
2:"Февраль",
3:"Март",
4:"Апрель",
5:"Май",
6:"Июнь",
7:"Июль",
8:"Август",
9:"Сентябрь",
10:"Октябрь",
11:"Ноябрь",
12:"Декабрь",
"Январь":1,
"Февраль":2,
"Март":3,
"Апрель":4,
"Май":5,
"Июнь":6,
"Июль":7,
"Август":8,
"Сентябрь":9,
"Октябрь":10,
"Ноябрь":11,
"Декабрь":12,
}

def calend(month,year):
    arr={}
    curr_month_dates = calendar.monthcalendar(year, month)
    for i in range(0, len(curr_month_dates) ):
       for j in range(0, len(curr_month_dates[i]) ):
          if curr_month_dates[i][j]==0:
              curr_month_dates[i][j]=""
          arr["d"+str(i+1)+str(j+1)]=curr_month_dates[i][j]
              
    arr['cal_month']=months_num[month]
    arr['cal_year']=year
    
    if month==1:
       arr['last_month']=months_num[12]
       arr['next_month']=months_num[month+1]
    elif month==12:
       arr['next_month']=months_num[1]
       arr['last_month']=months_num[month-1]
    else:
       arr['next_month']=months_num[month+1]
       arr['last_month']=months_num[month-1]
       
    return arr
def save_render(data):
    arr={}
    for i in data:
      if i!="csrfmiddlewaretoken":
          arr[i]=data[i]
    return arr


# (start(day, month), end(day, month))
sign_dates = (
    ((20, 3), (19, 4)),  # Aries
    ((20, 4), (20, 5)),
    ((21, 5), (20, 6)),
    ((21, 6), (22, 7)),
    ((23, 7), (22, 8)),
    ((23, 8), (22, 9)),
    ((23, 9), (22, 10)),
    ((23, 10), (21, 11)),
    ((22, 11), (21, 12)),
    ((22, 12), (19, 1)),
    ((20, 1), (17, 2)),
    ((18, 2), (19, 3)),  # Pisces
)

# English
en_dict = (
    (0, "Aries"),
    (1, "Taurus"),
    (2, "Gemini"),
    (3, "Cancer"),
    (4, "Leo"),
    (5, "Virgo"),
    (6, "Libra"),
    (7, "Scorpio"),
    (8, "Sagittarius"),
    (9, "Capricorn"),
    (10, "Aquarius"),
    (11, "Pisces"),
)

# Russian
ru_dict = (
    (0, "Овен"),
    (1, "Телец"),
    (2, "Близнецы"),
    (3, "Рак"),
    (4, "Лев"),
    (5, "Дева"),
    (6, "Весы"),
    (7, "Скорпион"),
    (8, "Стрелец"),
    (9, "Козерог"),
    (10, "Водолей"),
    (11, "Рыбы"),
)

# Num
num_dict = (
    (0, "1"),
    (1, "2"),
    (2, "3"),
    (3, "4"),
    (4, "5"),
    (5, "6"),
    (6, "7"),
    (7, "8"),
    (8, "9"),
    (9, "10"),
    (10, "11"),
    (11, "12"),
)


            
images = {
            'fire':'images/fire.png',
            'earth':'images/earth.png',
            'water':'images/water.png',
            'air':'images/air.png',
            'empty':'images/Empty.png',
            }

language_dict = {
    'en_US': en_dict,
    'ru_RU': ru_dict,
    'num': num_dict,
    None: num_dict
}

# @todo use gettext and etc
def _(word_index, language=None):
    if language is not None:
        return language_dict.get(language)[word_index][1]
    language = locale.getlocale()
    return language_dict.get(language[0], language_dict.get('en_US'))[word_index][1]

def get_zodiac_sign(d, month=None, language=None):
    # params
    if month is None:
        month = int(d.month)
        day = int(d.day)
    else:
        day = int(d)
        month = int(month)
    # calculate
    for index, sign in enumerate(sign_dates):
        if (month == sign[0][1] and day >= sign[0][0]) or (month == sign[1][1] and day <= sign[1][0]):
            return _(index, language)
    return ''

def get_images_by_zod(zod_num_get):
    temp=""
    if zod_num_get in ["1","5","9"]:
      temp="fire"
    if zod_num_get in ["2","6","10"]:
      temp="earth"
    if zod_num_get in ["3","7","11"]:
      temp="air"
    if zod_num_get in ["4","8","12"]:
      temp="water"
    return images[temp]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class Offer(View):

#     def get(self, request, *args, **kwargs):
#         return render(
#             request,
#             'offer.html',
#         )
        
    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
        }
        return render(
            request,
            'offer.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)

class Agreement(View):

#     def get(self, request, *args, **kwargs):
#         return render(
#             request,
#             'agreement.html',
#         )
        
    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
        }
        return render(
            request,
            'agreement.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)

class Menu(View):

    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
        }
        return render(
            request,
            'menu_footer.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
                
class Video(View):

    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
        }
        return render(
            request,
            'video.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)

global glob_context
class Algorithm(View):
        
    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        #requests.session().cookies.clear()
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context={}
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
            'zod_1': "images/Component4.png",
            'zod_2': "images/Component16.png",
            'zod_3': "images/Component22.png",
            'zod_4': "images/Component23.png",
            'zod_5': "images/Component17.png",
            'zod_6': "images/Component26.png",
            'zod_7': "images/Component18.png",
            'zod_8': "images/Component19.png",
            'zod_9': "images/Component20.png",
            'zod_10': "images/Component21.png",
            'zod_11': "images/Component27.png",
            'zod_12': "images/Component28.png",
            'image1':'images/Empty.png',
            'image2':'images/Empty.png',
            'star': 'images/star_border.png',
            }
        
        curr_culend=calend(date.today().month, date.today().year)
        context={**context,**curr_culend}
        
        global glob_context
        glob_context=context
        
        return render(
            request,
            'algorithm.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)

        if request.POST.get('Result'):
            context_zods = {
            'zod_1': "images/Component4.png",
            'zod_2': "images/Component16.png",
            'zod_3': "images/Component22.png",
            'zod_4': "images/Component23.png",
            'zod_5': "images/Component17.png",
            'zod_6': "images/Component26.png",
            'zod_7': "images/Component18.png",
            'zod_8': "images/Component19.png",
            'zod_9': "images/Component20.png",
            'zod_10': "images/Component21.png",
            'zod_11': "images/Component27.png",
            'zod_12': "images/Component28.png",
            'image1':'images/Empty.png',
            'image2':'images/Empty.png',
            'star': 'images/star_border.png',
            }
            data = request.POST
            left_result_={}
            right_result_={}
            center_result_={}
            left=False
            right=False
            
            context={}
            context={**context,**save_render(data)}
            curr_culend=calend(date.today().month, date.today().year)
            context={**context,**curr_culend}
            #context={'date1':data['date1'],'date2':data['date2']}
            
            for i in range(1,9):
               left_result_['x1'+str(i)]=str(data['x1'+str(i)])
               right_result_['x2'+str(i)]=str(data['x2'+str(i)])
               center_result_['x3'+str(i)]=str(data['x3'+str(i)])
            
            zod_left=""
            zod_right=""
            
            try:
               if data['date1']!='':
                  #context={**context,'scales11':'checked'}
                  left=True
                  temp=data['date1'].split('.')
                  zod_left=get_zodiac_sign(temp[0],temp[1],"num")
                  context_zods['zod_'+zod_left]=context_zods['zod_'+zod_left].replace('_red','').replace('_green','').split('.png')[0]+'_green.png'
                  #print(get_images_by_zod(zod_left))
                  context_zods['image1']=get_images_by_zod(zod_left)
                  #print(context_zods['zod_'+zod_left].replace('_red','').replace('_green','').split('.png')[0]+'_green.png')
            except:
               pass
               
            try:
               if data['date2']!='':
                  #context={**context,'scales22':'checked'}
                  right=True
                  temp=data['date2'].split('.')
                  zod_right=get_zodiac_sign(int(temp[0]),int(temp[1]),"num")
                  context_zods['zod_'+zod_right]=context_zods['zod_'+zod_right].replace('_red','').replace('_green','').split('.png')[0]+'_green.png'
                  #print(get_images_by_zod(zod_right))
                  context_zods['image2']=get_images_by_zod(zod_right)
            except:
               pass
               
            if zod_left==zod_right and zod_left!="":
               context_zods['zod_'+zod_left]=context_zods['zod_'+zod_left].replace('_red','').replace('_green','').split('.png')[0]+'_red.png'
            
            context={**context,**context_zods}
               
            result_values=algorithm_run(left_result_,center_result_,right_result_,left,right)
            context={**context,**result_values}
            
            global glob_context
            glob_context=context
            
            return render(request, 'algorithm.html', context=context)
            
        if request.POST.get('Save'):
            context=glob_context
            data = request.POST
            left_result=[]
            right_result=[]
            center_result=[]
            for i in range(1,9):
               left_result.append( str(data['x1'+str(i)]) )
               right_result.append( str(data['x2'+str(i)]) )
               center_result.append( str(data['x3'+str(i)]) )
               
            left_result="_".join(left_result)
            right_result="_".join(right_result)
            center_result="_".join(center_result)
            
            if center_result!="_______":
           
             favorites = Favorites.objects.create(
                user=request.user.username,
                date=datetime.today().strftime('%d.%m.%Y'),

                rakurs_left=left_result,
                rakurs_center=center_result,
                rakurs_right=right_result,
                unknoun_field=1,
                note='Информация о записи',
                alarm=False
             )
             favorites.save()
            #print(left_result)
            #aaa = request.POST.get('x11')
            #print(data['x12'])
            #return HttpResponseRedirect(request.path)
            context={**context,**{'star':'images/favorites_star.png'}}
            glob_context=context
            return render(request, 'algorithm.html', context=context)
            
        if request.POST.get('clear'):
            #return render(request, 'algorithm.html', context={})
            return HttpResponseRedirect(request.path)
            
        if request.POST.get('next_month'):
            context=glob_context
            if months_num[context['cal_month']]==12:
                curr_culend=calend(1, context['cal_year']+1)
            else:
                curr_culend=calend(months_num[context['cal_month']]+1, context['cal_year'])
            context={**context,**curr_culend}
            glob_context=context
               
            #print(context)
            return render(request, 'algorithm.html', context=context)
            
        if request.POST.get('last_month'):
            context=glob_context
            if months_num[context['cal_month']]==1:
                curr_culend=calend(12, context['cal_year']-1)
            else:
                curr_culend=calend(months_num[context['cal_month']]-1, context['cal_year'])
            context={**context,**curr_culend}
            glob_context=context
               
            #print(context)
            return render(request, 'algorithm.html', context=context)
            
        if request.POST.get('years'):
            context=glob_context
            year=int(request.POST['years'])
            curr_culend=calend(months_num[context['cal_month']], year)
            context={**context,**curr_culend,**{'cal_year':year}}
            glob_context=context
               
            #print(context)
            return render(request, 'algorithm.html', context=context)
        


@method_decorator(login_required(login_url='/'), name='dispatch')
class Tarif(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'tarif.html',
        )

class Contacts(View):
    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm
    
    def get(self, request, *args, **kwargs):
        
        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        context = {
            'login_form': login_form,
            'register_form': register_form,
            'forgot_password_form': forgot_password_form,
            'reset_password_form': reset_password_form,
        }
        return render(
            request,
            'contacts.html',context=context,
        )

    def post(self, request, *args, **kwargs):
    
        login_form = self.login_form
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form
        
        if request.POST.get('login'):
            login_form = LoginForm(data=request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if login_form.is_valid():
                if user is not None:
                    if not user.is_active:
                        current_site = get_current_site(request)
                        mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
                        message = render_to_string('confirmation_acc.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = user.email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.success(request,
                                         "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
                                             to_email))
                        return HttpResponseRedirect(request.path)
                    else:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        # messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
                        return HttpResponseRedirect(request.path)
                        
                else:
                    messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
                    return HttpResponseRedirect(request.path)
            else:
                for error in list(login_form.errors.values()):
                    messages.error(request, error)
                return HttpResponseRedirect(request.path)
        if request.POST.get('register'):
            register = Sign_Up_Form(request.POST)
            if register.is_valid():
                user = register.save()
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)
            else:
                for error in list(register.errors.values())[0]:
                   messages.error(request, error)
                   return HttpResponseRedirect(request.path)
        if request.POST.get('forgot_pass'):
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                qs = User.objects.filter(email=email)
                password = User.objects.make_random_password()
                site = get_current_site(request)
                if len(qs) > 0:
                    user = qs[0]
                    user.is_active = False
                    user.reset_password = True
                    user.set_password(password)
                    user.save()
                    mail_subject = 'Сброс пароля на https://tarocalendar.com/'
                    message = render_to_string('password_reset_mail.html', {
                        'user': user,
                        'domain': site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'password': password,
                    })
                    to_email = request.POST.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                messages.success(request,
                                 "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
                                     request.POST.get('email')))
                return HttpResponseRedirect(request.path)



class Favorites_View(ListView):
    template_name = 'favorites.html'
    paginate_by = 5

    def get_queryset(self):
        self.queryset = Favorites.objects.filter(user=self.request.user.username)
        return super().get_queryset()

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        edit_text = request.POST.get('edit')
        edit_id = request.POST.get('edit_id')
        checked_id = request.POST.getlist('checked')
        if request.POST.get('id'):
            Favorites.objects.get(pk=id).delete()
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('edit_id'):
            Favorites.objects.filter(id=edit_id).update(note=str(edit_text))
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('execute'):
            if request.POST.get('group_actions') == "Удалить выбранные результаты":
                for check_id in checked_id:
                    Favorites.objects.get(pk=check_id).delete()
            return HttpResponseRedirect('/favorites/')

def activate(request, uidb64, token):
    User = get_user_model()
    #try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    #except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        #user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Ваш аккаунт успешно подтверждён.')
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Ссылка недействительна.')
        return HttpResponseRedirect('/')
        
def csrf_failure(request, reason=""):
    return render(request, '403.html')
    
def handler_404(request, exception):
    return render(request, '404.html')

def handler_403(request, exception):
    return render(request, '403.html')

def handler_500(request):
    return render(request, '500.html')
    
    
    
# class Login_RegView(View):
#     login_form = LoginForm
#     register_form = Sign_Up_Form()
#     forgot_password_form = UserForgotPasswordForm()
#     reset_password_form = UserPasswordResetForm
#     
#     def get(self, request, *args, **kwargs):
#     
#         login_form = self.login_form(None)
#         register_form = self.register_form
#         forgot_password_form = self.forgot_password_form
#         reset_password_form = self.reset_password_form
#         
#         context = {
#             'login_form': login_form,
#             'register_form': register_form,
#             'forgot_password_form': forgot_password_form,
#             'reset_password_form': reset_password_form,
#         }
#         
#         return render(
#             request,
#             'login_reg.html', context=context,
#         )
#         
#     def post(self, request, *args, **kwargs):
#     
#         login_form = self.login_form
#         register_form = self.register_form
#         forgot_password_form = self.forgot_password_form
#         reset_password_form = self.reset_password_form
#         
#         if request.POST.get('login'):
#             login_form = LoginForm(data=request.POST)
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username=username, password=password)
#             if login_form.is_valid():
#                 if user is not None:
#                     if user.is_active:
#                         current_site = get_current_site(request)
#                         mail_subject = 'Подтверждение аккаунта на https://tarocalendar.com/'
#                         message = render_to_string('confirmation_acc.html', {
#                             'user': user,
#                             'domain': current_site.domain,
#                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                             'token': account_activation_token.make_token(user),
#                         })
#                         to_email = user.email
#                         email = EmailMessage(
#                             mail_subject, message, to=[to_email]
#                         )
#                         email.send()
#                         messages.success(request,
#                                          "На Ваш электронный адрес {} было направлено письмо, для подтверждения Вашего аккаунта.".format(
#                                              to_email))
#                         return HttpResponseRedirect(request.path)
#                     else:
#                         messages.error(request, 'Ваша учетная запись отключена. Обратитесь к администратору.')
#                         return HttpResponseRedirect(request.path)
#                 else:
#                     messages.error(request, 'Неверный логин или пароль, пожалуйста, повторите попытку.')
#                     return HttpResponseRedirect(request.path)
#             else:
#                 for error in list(login_form.errors.values()):
#                     messages.error(request, error)
#                 return HttpResponseRedirect(request.path)
#         if request.POST.get('register'):
#             register = Sign_Up_Form(request.POST)
#             if register.is_valid():
#                 user = register.save()
#                 user.is_active = False
#                 user.save()
#                 current_site = get_current_site(request)
#                 mail_subject = 'Активация аккаунта на https://tarocalendar.com/'
#                 message = render_to_string('acc_active_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 to_email = request.POST.get('email')
#                 email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#                 )
#                 email.send()
#                 messages.success(request,
#                                  "На Ваш электронный адрес {} было направлено письмо, для активации Вашего аккаунта.".format(
#                                      request.POST.get('email')))
#                 return HttpResponseRedirect(request.path)
#             else:
#                 for error in list(register.errors.values()):
#                     messages.error(request, error)
#                 return HttpResponseRedirect(request.path)
#         if request.POST.get('forgot_pass'):
#             form = UserForgotPasswordForm(request.POST)
#             if form.is_valid():
#                 email = request.POST.get('email')
#                 qs = User.objects.filter(email=email)
#                 password = User.objects.make_random_password()
#                 site = get_current_site(request)
#                 if len(qs) > 0:
#                     user = qs[0]
#                     user.is_active = False
#                     user.reset_password = True
#                     user.set_password(password)
#                     user.save()
#                     mail_subject = 'Сброс пароля на https://tarocalendar.com/'
#                     message = render_to_string('password_reset_mail.html', {
#                         'user': user,
#                         'domain': site.domain,
#                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token': account_activation_token.make_token(user),
#                         'password': password,
#                     })
#                     to_email = request.POST.get('email')
#                     email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#                     )
#                     email.send()
#                 messages.success(request,
#                                  "На Ваш электронный адрес {} было направлено письмо, для сброса Вашего пароля.".format(
#                                      request.POST.get('email')))
#                 return HttpResponseRedirect(request.path)