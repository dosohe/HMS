from service import models
from rest_framework import serializers


class Reservation(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = '__all__'