from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _
import datetime
from django.conf import settings

# Create your models here.
class Users(AbstractUser):

    ROLE_Registered = 0
    ROLE_Free = 1
    ROLE_Normal = 2
    ROLE_Full = 3

    email = models.EmailField(verbose_name='E-mail', blank=True, unique=True, null=True)
    email_checked = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    code = models.CharField(max_length=50, blank=True, null=True, default=None)
    reset_password = models.BooleanField(default=False)
    ROLE_CHOICES = (
        (ROLE_Registered, 'Зарегистрированный'),
        (ROLE_Free, 'Начальный'),
        (ROLE_Normal, 'Продвинутый'),
        (ROLE_Full, 'Полный')
    )
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=ROLE_CHOICES, blank=True, null=True, default=0)
    date_end = models.DateField(verbose_name='Дата окончания', default=datetime.date.today,null=True)


class Groupfavorites(models.Model):
    name = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',on_delete = models.DO_NOTHING)
    
    class Meta:
        unique_together = ('name', 'user',)

        
class Payments(models.Model):
    date = models.DateField(_("Date"), default=datetime.date.today)
    id_pay = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=50, null=True)
    tarif = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',on_delete = models.DO_NOTHING)


class Favorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',on_delete = models.DO_NOTHING)
    name_left = models.CharField(max_length=50, null=True)
    rakurs_name_left = models.CharField(max_length=50, null=True)
    name_right = models.CharField(max_length=50, null=True)
    rakurs_name_right = models.CharField(max_length=50, null=True)
    date_left = models.DateField(null=True)
    date_right = models.DateField(null=True)
    date = models.DateField(null=True, default=datetime.date.today)
    rakurs_left = models.CharField(max_length=50, null=True)
    rakurs_center = models.CharField(max_length=50, null=True)
    rakurs_right = models.CharField(max_length=50, null=True)
    unknoun_field = models.CharField(max_length=50, null=True)
    note = models.CharField(max_length=50, null=True)
    alarm = models.BooleanField(null=True, default=False)
    group = models.ForeignKey(Groupfavorites,on_delete = models.DO_NOTHING,null=True,blank=True)
    
    def rakurs_left_as_list(self):
        return self.rakurs_left.split('_')
        
    def rakurs_right_as_list(self):
        return self.rakurs_right.split('_')
        
    def rakurs_center_as_list(self):
        return self.rakurs_center.split('_')
    

    def group_name(self):
        try:
           return self.group.name
        except:
           return "-"

        
class Histpersons(models.Model):
    fio_ru = models.CharField(max_length=1000, null=True)
    fio_en = models.CharField(max_length=1000, null=True)
    date = models.DateField(null=True)
    result = models.CharField(max_length=1000, null=True)
    types = models.CharField(max_length=1000, null=True)
    
    class Meta:
        unique_together = ('fio_ru', 'fio_en', 'date',)
    
    def detail(self):
        return [self.fio_ru,self.fio_en,self.result]
    
class Calendata(models.Model):
    date = models.DateField(null=True,unique=True)
    result = models.CharField(max_length=1000, null=True)
    note = models.CharField(max_length=1000, null=True)