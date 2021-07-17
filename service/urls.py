from rest_framework.routers import DefaultRouter
from django.conf.urls import include, url
from django.urls import path

from service import api, views

router = DefaultRouter(trailing_slash=False)
router.register('reservations', api.ReservationSet, basename='reservations')

urlpatterns = [
    url('api/', include(router.urls)),
    path('', views.index, name='index')
]