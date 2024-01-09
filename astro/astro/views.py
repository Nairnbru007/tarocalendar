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

from .dicts_algor import *

months_num_={
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
months_num={
    1:"January",
    2:"Februare",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December",
    "January":1,
    "Februare":2,
    "March":3,
    "April":4,
    "May":5,
    "June":6,
    "July":7,
    "August":8,
    "September":9,
    "October":10,
    "November":11,
    "December":12,
}
def calend(month,year,left_arr="",right_arr=""):
    arr={}
    curr_month_dates = calendar.monthcalendar(year, month)
    #print(curr_month_dates)
    for i in range(0,6):
        for j in range(0,7):
            arr["d"+str(i+1)+str(j+1)]=""
            #arr["class_d"+str(i+1)+str(j+1)]=""
            arr["result_d"+str(i+1)+str(j+1)]=""
    #print(arr)

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
                #print(curr_date_cal)

                #filter
                if left_arr!="" or right_arr!="":
                    obj_db=Calendata.objects.get(date=datetime.strptime(curr_date_cal, '%d.%m.%Y'))
                    #tcd=list(map(int,obj_db.result.split('_')))
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
        data_arr.append([fields[0],fields[1],fields[2]])


    for line in data_arr:
        result=map(str, algorithm_run_glob(line[2]))
        name_comositors = Histpersons.objects.create(
            fio_ru=line[0],
            fio_en=line[1],
            date=datetime.strptime(line[2].replace('\r',''), "%d.%m.%Y").date(),
            types=str(csv_file.name).split('.')[0].upper(),
            result="_".join(result)
        )
        name_comositors.save()
    messages.error(request,'File Ok')
    return HttpResponseRedirect(request.path)

@user_passes_test(lambda u: u.is_superuser)
def upload_calend_(request):
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

@user_passes_test(lambda u: u.is_superuser)
def upload_calend(request):
    if "GET" == request.method:
        data_temp=[]
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


                        data_temp.append(Calendata(
                                date=datetime.strptime(curr_date_cal, "%d.%m.%Y").date(),
                                note='',
                                result="_".join(result)
                        ))

        #print(data_temp)
        Calendata.objects.bulk_create(data_temp)
        return HttpResponseRedirect('/')


def csrf_failure(request, reason=""):
    return render(request, path_to_tmps['403'])

def handler_404(request, exception):
    return render(request, path_to_tmps['404'])

def handler_403(request, exception):
    return render(request, path_to_tmps['403'])

def handler_500(request):
    return render(request, path_to_tmps['500'])