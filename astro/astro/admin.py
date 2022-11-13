from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *

from .models import *

#admin.site.register(Favorites)
@admin.register(Favorites)
class Favorites(admin.ModelAdmin):
	list_display = ['id','user','group_name','date_left','rakurs_left','rakurs_center','date_right', 'rakurs_right']
	
#admin.site.register(Payments)
@admin.register(Payments)
class Payments(admin.ModelAdmin):
	list_display = ['id','user','date','tarif','status']
	list_filter = ('user',)
admin.site.register(Histpersons)


class CustomUserAdmin(UserAdmin):
    add_form = Sign_Up_Form
    model = Users
    list_display = ['id','username', 'email', 'role', 'date_end']
    fieldsets = (
        #*UserAdmin.fieldsets,
        (None, {"fields": ("username", "email", "password")}),
        ('Роль пользователя',{'fields': ('role','date_end',)}),
        (
            "Системная информация",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
        
    )


admin.site.register(Users, CustomUserAdmin)

@admin.register(Groupfavorites)
class Groupfavorites(admin.ModelAdmin):
	list_display = ['id','user','name']
