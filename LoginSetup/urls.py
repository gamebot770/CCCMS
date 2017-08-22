from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/$', views.register, name="registration"),
    #url(r'^home/$', views.home,name="homepage"),
    url(r'^register/success/$', views.register_success),
    url(r'^login/$', views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', views.logout, {'next_page': '/login/'}),

]
