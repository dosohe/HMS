from django.shortcuts import render

from service import models


def index(request):
    context = {'reservations': models.Reservation.objects.all()}
    return render(request, 'reservation.html', context)
