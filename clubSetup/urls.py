from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.clubSetup,name="clubSetup1"),
    url(r'^installClub$',views.installClub,name="clubInstall"),
    url(r'^details/(\d+)/$',views.details,name="clubDetails"),
    url(r'^upload$',views.uploadStudList,name="uploadStudList")
 
]
