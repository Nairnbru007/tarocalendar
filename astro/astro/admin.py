from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *

from .models import *

#admin.site.register(User_day_left)
#admin.site.register(User_day_right)
#admin.site.register(month_right_in_bd)
#admin.site.register(month_left_in_bd)
admin.site.register(Favorites)
#admin.site.register(User_day_center)
#admin.site.register(Days)


class CustomUserAdmin(UserAdmin):
    add_form = Sign_Up_Form
    model = Users
    list_display = ['username', 'email', ]
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Роль пользователя',
            {
                'fields': (
                    'role',
                )
            }
        )
    )


admin.site.register(Users, CustomUserAdmin)
