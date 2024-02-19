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
from django.contrib.auth import get_user_model
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
from datetime import datetime, date, timedelta

from django.db.models import Q
from django.shortcuts import redirect
#import requests
from os import walk
import os
import random
import locale
from yookassa import Configuration
import var_dump as var_dump
from yookassa import Payment
import uuid
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

Configuration.account_id = '951224'
Configuration.secret_key = 'test_POrgWM4SZZ2RUTtMIKD1ByjrXaZ_etZ1KXgG7HPChck'

from .dicts_algor import *
path_to_tmps=path_to_tmps_ru
months_num=months_num_ru
language_dict = language_dict
def calend(month,year,left_arr="",right_arr=""):
    arr={}
    curr_month_dates = calendar.monthcalendar(year, month)
    #print(curr_month_dates)
    for i in range(0,6):
        for j in range(0,7):
            arr["d"+str(i+1)+str(j+1)]=""
            #arr["class_d"+str(i+1)+str(j+1)]=""
            arr["result_d"+str(i+1)+str(j+1)]=""
    for i in range(0, len(curr_month_dates) ):
        for j in range(0, len(curr_month_dates[i]) ):
            if curr_month_dates[i][j]==0:
                curr_month_dates[i][j]=""
            arr["d"+str(i+1)+str(j+1)]=curr_month_dates[i][j]
            curr_date_cal=''
            if arr["d"+str(i+1)+str(j+1)]!='':
                if arr["d"+str(i+1)+str(j+1)]<10:
                    curr_date_cal+='0'
                if month<10:
                    curr_date_cal+=str(arr["d"+str(i+1)+str(j+1)])+'.'+'0'+str(month)+'.'+str(year)
                else:
                    curr_date_cal+=str(arr["d"+str(i+1)+str(j+1)])+'.'+str(month)+'.'+str(year)
                if left_arr!="" or right_arr!="":
                    obj_db=Calendata.objects.get(date=datetime.strptime(curr_date_cal, '%d.%m.%Y'))
                    arr["result_d"+str(i+1)+str(j+1)]=str(obj_db.result)
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
        arr['last_month']=months_num[month-1]
    return arr
def hist_pers_show(inp_arr):
    hp_arr={}
    for i in range(1,9):
        hp_arr['c1'+str(i)]=inp_arr[i-1]
    return hp_arr

# @todo use gettext and etc

def user_is_actual(self):
    print(u.role)
class Up_date(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.date_end >= date.today():
            #print([self.request.user.date_end,date.today()])
            return True
        else:
            return False
    def handle_no_permission(self):
        return redirect('/tarif/')
class Up_role(UserPassesTestMixin):
    def test_func(self):
        #print(self.request.user.role)
        if self.request.user.role >= 3:
            return True
        else:
            return False
    def handle_no_permission(self):
        return redirect('/tarif/')

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
            path_to_tmps['offer'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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
            path_to_tmps['agreement'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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
            path_to_tmps['menu_footer'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                mail_subject = 'Account activation https://tarocalendar.com/'
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                                 "An email has been sent to your email address {} to activate your account.".format(
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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
            path_to_tmps['video'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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

#@user_passes_test(lambda u: True if u.date_end >= date.today() else False,login_url='/')
@method_decorator(login_required(login_url='/'), name='dispatch')
class Algorithm(View):

    login_form = LoginForm
    register_form = Sign_Up_Form()
    forgot_password_form = UserForgotPasswordForm()
    reset_password_form = UserPasswordResetForm

    def get(self, request, *args, **kwargs):

        try:
            temp_user=User.objects.get(pk=request.user.id)
            if temp_user.date_end < date.today():
                temp_user.role=0
                temp_user.save()
        except:
            pass
        try:
            Payments.objects.filter(user=request.user, date__lte=date.today() - timedelta(days=3)).delete()
            for i in Payments.objects.filter(user=request.user,status='pending'):
                payment_ = Payment.find_one(i.id_pay)
                payment_= payment_.json()
                payment_=json.loads(payment_)
                #print(payment_)
                #print(tarif_dict[payment_['description'].split(' ')[0]])
                if payment_['status']=='succeeded':
                    if tarif_dict[payment_['description'].split(' ')[0]]>=request.user.role:
                        temp_user=User.objects.get(pk=request.user.id)
                        temp_user.role=tarif_dict[payment_['description'].split(' ')[0]]
                        temp_user.date_end=date.today() + timedelta(days=31)
                        temp_user.save()

                    temp_paym=Payments.objects.get(id_pay=i.id_pay)
                    temp_paym.status='succeeded'
                    temp_paym.save()

        except:
            pass


        #requests.session().cookies.clear()

        login_form = self.login_form(None)
        register_form = self.register_form
        forgot_password_form = self.forgot_password_form
        reset_password_form = self.reset_password_form

        grlist=Groupfavorites.objects.filter(user=request.user)

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
            'grps':grlist,
        }

        curr_culend=calend(date.today().month, date.today().year, [],[])
        context={**context,**curr_culend}

        global glob_context
        glob_context=context

        return render(
            request,
            path_to_tmps['algorithm'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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
            if self.request.user.date_end < date.today():
                return redirect('/tarif/')
            if self.request.user.role < 1:
                return redirect('/tarif/')
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
            for i in range(1,9):
                left_result_['x1'+str(i)]=str(data['x1'+str(i)])
                right_result_['x2'+str(i)]=str(data['x2'+str(i)])
                center_result_['x3'+str(i)]=str(data['x3'+str(i)])

            zod_left=""
            zod_right=""
            hist_pers_1={"hstprs1":[],"hstprs1_count":0}
            hist_pers_2={"hstprs2":[],"hstprs2_count":0}
            result_1_9_right=[]
            result_1_9_left=[]

            result_fio={}
            #hist_pers={"hstprs1":Histpersons.objects.all()}

            try:
                temp_gr=data['groups_name']
            except:
                temp_gr=""
            grpps={"grps":Groupfavorites.objects.filter(user=request.user),'groups_name': temp_gr}
            context={**context,**save_render(data),**grpps}

            try:
                if data['date1']!='':
                    if data['fio1']!='':
                        result_fio=fio_to_num(data['fio1'],'1')
                        #result_fio['fio11'] = '1'
                        #result_fio['fio12'] = '2'
                        #result_fio['fio13'] = '3'

                    left=True
                    temp=data['date1'].split('.')
                    zod_left=get_zodiac_sign(temp[0],temp[1],"num")
                    context_zods['zod_'+zod_left]=context_zods['zod_'+zod_left].replace('_red','').replace('_green','').split('.png')[0]+'_green.png'
                    context_zods['image1']=get_images_by_zod(zod_left)

                    left_return=algorithm_run_left(left_result_,data['date1'])
                    left_result_=left_return[0]
                    result_1_9_left=left_return[1]

                    if self.request.user.role >= 3:
                        for hp1 in Histpersons.objects.all():
                            count_matches=0
                            thp1=hp1.detail()[2].split('_')
                            thp1_arr=[0,0,0,0,0,0,0,0]
                            for i in range(8):
                                if thp1[i]!="-":
                                    thp1[i]=int(thp1[i])
                            for i in range(8):
                                for j in range(8):
                                    if thp1[i] == result_1_9_left[j]:
                                        if thp1_arr[i]==0:
                                            thp1_arr[i]=1
                                        if i==j:
                                            thp1_arr[i]=1.1
                            count_matches=sum(thp1_arr)
                            if count_matches>0:
                                hist_pers_1["hstprs1"].append({'fio_ru':hp1.fio_ru,'result':hp1.result,'count':count_matches,'date':hp1.date, 'types':hp1.types.title()})
                        hist_pers_1["hstprs1"] = sorted(hist_pers_1["hstprs1"], key=lambda d: d['count'], reverse=True)
                        hist_pers_1["hstprs1_count"]=len(hist_pers_1["hstprs1"])

                else:
                    left=False
            except:
                left=False
                pass

            try:
                if data['date2']!='':
                    if data['fio1'] != '':
                        result_fio = fio_to_num(data['fio2'], '2')
                    #context={**context,'scales22':'checked'}
                    right=True
                    temp=data['date2'].split('.')
                    zod_right=get_zodiac_sign(int(temp[0]),int(temp[1]),"num")
                    context_zods['zod_'+zod_right]=context_zods['zod_'+zod_right].replace('_red','').replace('_green','').split('.png')[0]+'_green.png'
                    #print(get_images_by_zod(zod_right))
                    context_zods['image2']=get_images_by_zod(zod_right)

                    right_return=algorithm_run_right(right_result_,data['date2'])
                    right_result_=right_return[0]
                    result_1_9_right=right_return[1]

                    if self.request.user.role >= 3:
                        for hp2 in Histpersons.objects.all():
                            count_matches=0
                            thp2=hp2.detail()[2].split('_')
                            thp2_arr=[0,0,0,0,0,0,0,0]
                            for i in range(8):
                                if thp2[i]!="-":
                                    thp2[i]=int(thp2[i])
                            for i in range(8):
                                for j in range(8):
                                    if thp2[i] == result_1_9_right[j]:
                                        if thp2_arr[i]==0:
                                            thp2_arr[i]=1
                                        if i==j:
                                            thp2_arr[i]=1.1
                            count_matches=sum(thp2_arr)
                            if count_matches>0:
                                hist_pers_2["hstprs2"].append({'fio_ru':hp2.fio_ru,'result':hp2.result,'count':count_matches,'date':hp2.date, 'types':hp2.types.title()})
                        hist_pers_2["hstprs2"] = sorted(hist_pers_2["hstprs2"], key=lambda d: d['count'], reverse=True)
                        hist_pers_2["hstprs2_count"]=len(hist_pers_2["hstprs2"])

                else:
                    right=False
            except Exception as e:
                print(e)
                right=False
                pass

            if zod_left==zod_right and zod_left!="":
                context_zods['zod_'+zod_left]=context_zods['zod_'+zod_left].replace('_red','').replace('_green','').split('.png')[0]+'_red.png'

            context={**context,**context_zods}
            context = {**context, **result_fio}

            #print(result_1_9_left)
            curr_culend=calend(date.today().month, date.today().year,result_1_9_left,result_1_9_right)
            context={**context,**curr_culend}

            #print(f'left {left} \nright {right}')
            result_values=algorithm_run_center(left_result_,center_result_,right_result_,left,right,datetime.now().strftime("%d.%m.%Y"))
            context={**context,**result_values,**hist_pers_1,**hist_pers_2}
            #print(datetime.now().strftime("%d.%m.%Y"))

            global glob_context
            glob_context=context

            return render(request, path_to_tmps['algorithm'], context=context)
        if request.POST.get('Save'):
            if self.request.user.role < 3:
                return redirect('/tarif/')

            context = glob_context
            data = request.POST
            left_result = []
            right_result = []
            center_result = []
            date_left_ = None
            date_right_ = None
            name_left_ = None
            name_right_ = None
            rakurs_name_left_result = []
            rakurs_name_right_result = []

            for i in range(1, 9):
                left_result.append(str(data['x1' + str(i)]))
                right_result.append(str(data['x2' + str(i)]))
                center_result.append(str(data['x3' + str(i)]))

            left_result = "_".join(left_result)
            right_result = "_".join(right_result)
            center_result = "_".join(center_result)

            name_left_ = data['fio1']
            name_righ_ = data['fio2']
            try:
                temp_gr = data['groups_name']
                if temp_gr != '':
                    temp_gr = Groupfavorites.objects.filter(user=request.user, name=temp_gr)[0]
                else:
                    temp_gr = None
            except:
                temp_gr = None

            # print(data)

            if center_result != "_______":
                try:
                    date_left_ = datetime.strptime(data['date1'], '%d.%m.%Y').date()
                except:
                    pass
                try:
                    date_right_ = datetime.strptime(data['date2'], '%d.%m.%Y').date()
                except:
                    pass
                if date_left_ != None or date_right_ != None:
                    favorites = Favorites.objects.create(
                        user=User.objects.get(pk=request.user.id),
                        date_left=date_left_,
                        date_right=date_right_,
                        # date = datetime.today().strftime('%d.%m.%Y'),
                        name_left=name_left_,
                        name_right=name_right_,
                        rakurs_left=left_result,
                        rakurs_center=center_result,
                        rakurs_right=right_result,
                        unknoun_field=1,
                        note='Information',
                        alarm=False,
                        group=temp_gr
                    )
                    favorites.save()


            context={**context,**{'star':'images/favorites_star.png'}}
            glob_context=context
            return render(request, path_to_tmps['algorithm'], context=context)
        if request.POST.get('clear'):
            #return render(request, path_to_tmps['algorithm'], context={})
            return HttpResponseRedirect(request.path)
        if request.POST.get('next_month'):
            if self.request.user.role < 3:
                return redirect('/tarif/')
            context=glob_context
            data = request.POST
            left_arr_next=[]
            right_arr_next=[]
            for i in range(0,8):
                if data['x1'+str(i+1)] and context['x1'+str(i+1)]!='':
                    #left_arr_next.append(int(context['x1'+str(i+1)]))
                    left_arr_next.append(context['x1'+str(i+1)])
                if data['x2'+str(i+1)] and context['x2'+str(i+1)]!='':
                    #right_arr_next.append(int(context['x2'+str(i+1)]))
                    right_arr_next.append(context['x2'+str(i+1)])
            if months_num[context['cal_month']]==12:
                curr_culend=calend(1, context['cal_year']+1,left_arr_next,right_arr_next)
            else:
                curr_culend=calend(months_num[context['cal_month']]+1, context['cal_year'],left_arr_next,right_arr_next)
            context={**context,**curr_culend}
            glob_context=context
            return render(request, path_to_tmps['algorithm'], context=context)

        if request.POST.get('last_month'):
            if self.request.user.role < 3:
                return redirect('/tarif/')
            context=glob_context
            data = request.POST
            left_arr_next=[]
            right_arr_next=[]
            for i in range(0,8):
                if data['x1'+str(i+1)] and context['x1'+str(i+1)]!='':
                    #left_arr_next.append(int(context['x1'+str(i+1)]))
                    left_arr_next.append(context['x1'+str(i+1)])
                if data['x2'+str(i+1)] and context['x2'+str(i+1)]!='':
                    #right_arr_next.append(int(context['x2'+str(i+1)]))
                    right_arr_next.append(context['x2'+str(i+1)])
            if months_num[context['cal_month']]==1:
                curr_culend=calend(12, context['cal_year']-1,left_arr_next,right_arr_next)
            else:
                curr_culend=calend(months_num[context['cal_month']]-1, context['cal_year'],left_arr_next,right_arr_next)
            context={**context,**curr_culend}
            glob_context=context
            return render(request, path_to_tmps['algorithm'], context=context)

        if request.POST.get('years'):
            if self.request.user.role < 3:
                return redirect('/tarif/')
            context=glob_context
            data = request.POST
            left_arr_next=[]
            right_arr_next=[]
            for i in range(0,8):
                if data['x1'+str(i+1)] and context['x1'+str(i+1)]!='':
                    #left_arr_next.append(int(context['x1'+str(i+1)]))
                    left_arr_next.append(context['x1'+str(i+1)])
                if data['x2'+str(i+1)] and context['x2'+str(i+1)]!='':
                    #right_arr_next.append(int(context['x2'+str(i+1)]))
                    right_arr_next.append(context['x2'+str(i+1)])
            year=int(request.POST['years'])
            curr_culend=calend(months_num[context['cal_month']], year,left_arr_next,right_arr_next)
            context={**context,**curr_culend,**{'cal_year':year}}
            glob_context=context
            return render(request, path_to_tmps['algorithm'], context=context)

@method_decorator(login_required(login_url='/'), name='dispatch')
class Tarif(View):

    def get(self, request, *args, **kwargs):

        try:
            temp_user=User.objects.get(pk=request.user.id)
            if temp_user.date_end < date.today():
                temp_user.role=0
                temp_user.save()
        except:
            pass
        try:
            Payments.objects.filter(user=request.user, date__lte=date.today() - timedelta(days=3)).delete()
            for i in Payments.objects.filter(user=request.user,status='pending'):
                payment_ = Payment.find_one(i.id_pay)
                payment_= payment_.json()
                payment_=json.loads(payment_)
                #print(payment_)
                #print(tarif_dict[payment_['description'].split(' ')[0]])
                if payment_['status']=='succeeded':
                    if tarif_dict[payment_['description'].split(' ')[0]]>=request.user.role:
                        temp_user=User.objects.get(pk=request.user.id)
                        temp_user.role=tarif_dict[payment_['description'].split(' ')[0]]
                        temp_user.date_end=date.today() + timedelta(days=31)
                        temp_user.save()

                    temp_paym=Payments.objects.get(id_pay=i.id_pay)
                    temp_paym.status='succeeded'
                    temp_paym.save()

        except:
            pass

        return render(
            request,
            path_to_tmps['tarif'],
        )
    def post(self, request, *args, **kwargs):
        if request.POST.get('pay_start'):
            payment = Payment.create({
                "amount": {
                    "value": "300.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.path
                },
                "capture": True,
                "description": str("Start "+request.user.username+' '+request.user.email)
            }, uuid.uuid4())

            var_dump.var_dump(payment)

            payment_ans=payment.json()
            date_ans=json.loads(payment_ans)
            conf_url=date_ans["confirmation"]['confirmation_url']

            pay_create = Payments.objects.create(
                user = User.objects.get(pk=request.user.id),
                id_pay = date_ans["id"],
                status = date_ans["status"],
                tarif = str("Start "+request.user.username+' '+request.user.email)
            )
            pay_create.save()

            return HttpResponseRedirect(conf_url)

        if request.POST.get('pay_standart'):
            payment = Payment.create({
                "amount": {
                    "value": "600.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.path
                },
                "capture": True,
                "description": str("Standart "+request.user.username+' '+request.user.email)
            }, uuid.uuid4())

            var_dump.var_dump(payment)

            payment_ans=payment.json()
            date_ans=json.loads(payment_ans)
            conf_url=date_ans["confirmation"]['confirmation_url']

            pay_create = Payments.objects.create(
                user = User.objects.get(pk=request.user.id),
                id_pay = date_ans["id"],
                status = date_ans["status"],
                tarif = str("Standart "+request.user.username+' '+request.user.email)
            )
            pay_create.save()

            return HttpResponseRedirect(conf_url)

        if request.POST.get('pay_full'):
            payment = Payment.create({
                "amount": {
                    "value": "900.00",
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": request.path
                },
                "capture": True,
                "description": str("Full "+request.user.username+' '+request.user.email)
            }, uuid.uuid4())

            var_dump.var_dump(payment)

            payment_ans=payment.json()
            date_ans=json.loads(payment_ans)
            conf_url=date_ans["confirmation"]['confirmation_url']

            pay_create = Payments.objects.create(
                user = User.objects.get(pk=request.user.id),
                id_pay = date_ans["id"],
                status = date_ans["status"],
                tarif = str("Full "+request.user.username+' '+request.user.email)
            )
            pay_create.save()

            return HttpResponseRedirect(conf_url)

        else:

            return render(request, path_to_tmps['tarif'])

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
            path_to_tmps['contacts'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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

class Commercial(View):
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
            path_to_tmps['commercial'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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

class Description(View):
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
            path_to_tmps['description'],context=context,
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
                        message = render_to_string(path_to_tmps['confirmation_acc'], {
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
                message = render_to_string(path_to_tmps['acc_active_email'], {
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
                    message = render_to_string(path_to_tmps['password_reset_mail'], {
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

@method_decorator(login_required(login_url='/'), name='dispatch')
class Favorites_View(Up_role,Up_date,ListView):
    template_name = path_to_tmps['favorites']
    paginate_by = 5
    model=Favorites

    def get_queryset(self):
        self.queryset = Favorites.objects.filter(user=self.request.user.id)
        return super().get_queryset()

    def get_context_data(self, **kwargs):

        data = super().get_context_data(**kwargs)
        data['grps'] = Groupfavorites.objects.filter(user=self.request.user.id)

        return data

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        edit_text = request.POST.get('edit')
        edit_id = request.POST.get('edit_id')
        checked_id = request.POST.getlist('checked')
        if request.POST.get('creategroup'):
            try:
                name_favorites = Groupfavorites.objects.create(
                    user=User.objects.get(pk=request.user.id),
                    name=request.POST['newgroupname']
                )
                name_favorites.save()
            except:
                pass
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('id'):
            Favorites.objects.get(pk=id).delete()
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('edit_id'):
            Favorites.objects.filter(id=edit_id).update(note=str(edit_text))
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('execute'):
            if request.POST.get('group_actions') == "Delete selected":
                for check_id in checked_id:
                    Favorites.objects.get(pk=check_id).delete()
            return HttpResponseRedirect('/favorites/')
        elif request.POST.get('groups_name'):
            #print("aaaa")
            return HttpResponseRedirect('/favorites/')

        return HttpResponseRedirect('/favorites/')

def activate(request, uidb64, token):
    User = get_user_model()

    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.date_end=date.today() + timedelta(days=2)
        user.role=1
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Ваш аккаунт успешно подтверждён.')
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Ссылка недействительна.')
        return HttpResponseRedirect('/')

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter(name='split')
#@register.filter(needs_autoescape=True)
def split(value, key):
    return value.split(key)

#