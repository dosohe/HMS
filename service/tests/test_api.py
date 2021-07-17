from datetime import datetime

import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient

from service.models import Reservation


pytestmark = pytest.mark.django_db

@pytest.fixture
def reser():
    return mixer.blend('service.Reservation', 
        slug = "HMB0001",
        check_in = datetime(2021, 5, 12),
        check_out = datetime(2021, 6, 1),
        flat = "Hawtrey",
        city = "LONDON",
        net_income = 1200,
    )

class TestReservationSet:

    def test_total_commission(self, client: APIClient, reser):
        true_resp = {
            "total": 120
        }
        reser.save()
        response = client.get('/api/reservations/total_commission')
        assert response.status_code == 200
        assert response.json()['total'] == 120
        assert response.json() == true_resp

        reser.net_income = 5000
        reser.save()
        response = client.get('/api/reservations/total_commission')
        assert response.status_code == 200
        assert response.json()['total'] == 500

        reser.delete()
        response = client.get('/api/reservations/total_commission')
        assert response.status_code == 200
        assert response.json()['total'] == 0
    
    def test_city_commission(self, client: APIClient, reser):
        reser.save()
        Reservation.objects.create(
            slug = "HMB0002",
            check_in = datetime(2021, 6, 10),
            check_out = datetime(2021, 6, 14),
            flat = "Hawtrey",
            city = "LONDON",
            net_income = 1150,
        )
        Reservation.objects.create(
            slug = "HMB0003",
            check_in = datetime(2021, 6, 10),
            check_out = datetime(2021, 6, 14),
            flat = "Hawtrey",
            city = "LONDON",
            net_income = 780,
        )
        city_name = "London"
        response = client.get(f'/api/reservations/total_commission?city='
                                     f'{city_name}')
        assert response.status_code == 200
        assert response.json()['LONDON'] == 313
        city_name = "Porto"
        response = client.get(f'/api/reservations/total_commission?city='
                                     f'{city_name}')
        assert response.json()['PORTO'] == 0

    def test_monthly_commission(self, client: APIClient, reser):
        reser.save()
        Reservation.objects.create(
            slug = "HMB0002",
            check_in = datetime(2021, 6, 10),
            check_out = datetime(2021, 6, 14),
            flat = "Hawtrey",
            city = "LONDON",
            net_income = 1150,
        )
        response = client.get('/api/reservations/monthly_commission')
        assert response.status_code == 200
        assert response.json() == {'monthly_grc': {'05/2021': 120.0, '06/2021': 115.0}}

    def test_compare_total_and_montly(self, client: APIClient, reser):
        reser.save()
        Reservation.objects.create(
            slug = "HMB0002",
            check_in = datetime(2021, 6, 10),
            check_out = datetime(2021, 6, 14),
            flat = "Hawtrey",
            city = "LONDON",
            net_income = 1150,
        )
        res_total = client.get('/api/reservations/total_commission')
        res_monthly = client.get('/api/reservations/monthly_commission')
        assert res_total.json()['total'] == sum(res_monthly.json()['monthly_grc'].values())

