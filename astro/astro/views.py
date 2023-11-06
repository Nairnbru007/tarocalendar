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
from datetime import datetime
from datetime import date,timedelta
import calendar
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

path_to_tmps={
'upload':'upload.html',#+
'403':'403.html',#+
'404':'404.html',#+
'500':'500.html',#+
}

@user_passes_test(lambda u: u.is_superuser)
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, path_to_tmps['upload'], data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(request.path)
        #if file is too large, return
    if csv_file.multiple_chunks():
        messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        return HttpResponseRedirect(request.path)
    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    data_arr = []
    for line in lines:
        fields = line.split(";")
        data_arr.append([fields[0],fields[1]])


    for line in data_arr:
        result=map(str, algorithm_run_glob(line[1]))
        name_comositors = Histpersons.objects.create(
            fio=line[0],
            date=datetime.strptime(line[1].replace('\r',''), "%d.%m.%Y").date(),
            types=str(csv_file.name).split('.')[0].upper(),
            result="_".join(result)
        )
        name_comositors.save()
    messages.error(request,'File Ok')
    return HttpResponseRedirect(request.path)

@user_passes_test(lambda u: u.is_superuser)
def upload_calend(request):
    if "GET" == request.method:

        for i in range(1800,2225):
            for j in range(1,13):
                curr_culend=calend(j,i)
                for k in curr_culend.items():
                    if k[1]!="" and 'class' not in k[0] and k[0][0]=='d':
                        curr_date_cal=''
                        if k[1]<10:
                            curr_date_cal+='0'
                        if j<10:
                            curr_date_cal+=str(k[1])+'.'+'0'+str(j)+'.'+str(i)
                        else:
                            curr_date_cal+=str(k[1])+'.'+str(j)+'.'+str(i)
                        result=map(str, algorithm_run_glob(curr_date_cal))

                        try:
                            data_temp = Calendata.objects.create(
                                date=datetime.strptime(curr_date_cal, "%d.%m.%Y").date(),
                                note='',
                                result="_".join(result)
                            )
                            data_temp.save()
                        except:
                            pass
        return HttpResponseRedirect('/')

def csrf_failure(request, reason=""):
    return render(request, path_to_tmps['403'])

def handler_404(request, exception):
    return render(request, path_to_tmps['404'])

def handler_403(request, exception):
    return render(request, path_to_tmps['403'])

def handler_500(request):
    return render(request, path_to_tmps['500'])