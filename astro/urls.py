"""astro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from astro.astro import views_ru
from astro.astro import views_en
from astro.astro import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#ru
    path('', views_ru.Menu.as_view(), name='main_ru'),
    path('offer/', views_ru.Offer.as_view(), name='offer_ru'),
    path('favorites/', views_ru.Favorites_View.as_view(), name='favorites_ru'),
    path('agreement/', views_ru.Agreement.as_view(), name='agreement_ru'),
    path('tariff/', views_ru.Tarif.as_view(), name='tariff_ru'),
    path('contacts/', views_ru.Contacts.as_view(), name='contacts_ru'),
    path('commercial/', views_ru.Commercial.as_view(), name='commercial_ru'),
    path('description/', views_ru.Description.as_view(), name='description_ru'),
    path('instruction/', views_ru.Instruction.as_view(), name='instruction_ru'),
    path('video/', views_ru.Video.as_view(), name='video_ru'),
    path('algorithm/', views_ru.Algorithm.as_view(), name='algorithm_ru'),
    path('activate/(<uidb64>)/(<token>)/',views_ru.activate, name='activate_ru'),
    path('reset_pswd/(<uidb64>)/(<token>)/',views_ru.Reset_pswd.as_view(), name='reset_pswd_ru'),
#en
    path('en/', views_en.Menu.as_view(), name='main_en'),
    path('en/offer/', views_en.Offer.as_view(), name='offer_en'),
    path('en/favorites/', views_en.Favorites_View.as_view(), name='favorites_en'),
    path('en/agreement/', views_en.Agreement.as_view(), name='agreement_en'),
    path('en/tariff/', views_en.Tarif.as_view(), name='tariff_en'),
    path('en/contacts/', views_en.Contacts.as_view(), name='contacts_en'),
    path('en/commercial/', views_en.Commercial.as_view(), name='commercial_en'),
    path('en/description/', views_en.Description.as_view(), name='description_en'),
    path('en/instruction/', views_en.Instruction.as_view(), name='instruction_en'),
    path('en/video/', views_en.Video.as_view(), name='video_en'),
    path('en/algorithm/', views_en.Algorithm.as_view(), name='algorithm_en'),
    path('en/activate/(<uidb64>)/(<token>)/',views_en.activate, name='activate_en'),
    path('en/reset_pswd/(<uidb64>)/(<token>)/',views_en.Reset_pswd.as_view(), name='reset_pswd_ru'),
#system
    path('logout_ru/', LogoutView.as_view(next_page='/'), name='logout_ru'),
    path('logout_en/', LogoutView.as_view(next_page='/en'), name='logout_en'),
    path('upload/csv/', views.upload_csv, name='upload_csv'),
    path('upload/data/', views.upload_calend, name='upload_calend'),

    #path('login_reg/', views.Login_RegView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='login_'),
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    
    
handler404 = views.handler_404
handler500 = views.handler_500
handler403 = views.handler_403