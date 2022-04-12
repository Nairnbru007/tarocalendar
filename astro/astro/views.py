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
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token, password_reset_token
from django.core.mail import EmailMessage

from os import walk
import os  


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
    



# def index(request):
#     return render(request, 'index.html')

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
        

class Algorithm(View):

#     def get(self, request, *args, **kwargs):
#         return render(
#             request,
#             'agreement.html',
#         )
        

    
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

        
@method_decorator(login_required(login_url='/'), name='dispatch')
class Tarif(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'tarif.html',
        )

class Contacts(View):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            'contacts.html',
        )

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