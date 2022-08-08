from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_slug
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return '%s' % (self.get_full_name())
        
        
class Favorites(models.Model):
    user = models.CharField(max_length=50, null=True)
    date = models.CharField(max_length=50, null=True)
    rakurs_left = models.CharField(max_length=50, null=True)
    rakurs_center = models.CharField(max_length=50, null=True)
    rakurs_right = models.CharField(max_length=50, null=True)
    unknoun_field = models.CharField(max_length=50, null=True)
    note = models.CharField(max_length=50, null=True)
    alarm = models.BooleanField(null=True, default=False)
    
    def rakurs_left_as_list(self):
        return self.rakurs_left.split('_')
        
    def rakurs_right_as_list(self):
        return self.rakurs_right.split('_')
        
    def rakurs_center_as_list(self):
        return self.rakurs_center.split('_')