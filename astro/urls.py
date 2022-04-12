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
    
    path('offer/', views.Offer.as_view(), name='offer'),
    path('favorites/', views.Favorites_View.as_view(), name='favorites'),
    path('agreement/', views.Agreement.as_view(), name='agreement'),
    path('tarif/', views.Tarif.as_view(), name='tarif'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('algorithm/', views.Algorithm.as_view(), name='algorithm'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    #path('login_reg/', views.Login_RegView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='login_'),
    #
    path('', views.Menu.as_view(), name='main'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
    #
    #path('page/', views.index, name='page')
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    
    
handler404 = views.handler_404
handler500 = views.handler_500
handler403 = views.handler_403