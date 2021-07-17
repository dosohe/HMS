import csv
from dateutil import rrule
from datetime import timedelta
from collections import Counter

from service.models import  Reservation

class GuestReadyCommission:

    GRC = {
        "LONDON": 0.10,
        "PARIS": 0.12,
        "PORTO": 0.09,
    }

    def __init__(self, params):
        self.file = params.get("file")
        self.city = params.get("city")
        self.monthly_grc = {}

    def read(self):
        reader = csv.DictReader(self.file, delimiter=",")
        self._upload_to_db(reader)
        return "Successfully read"

    def _upload_to_db(self, reader):
        for row in reader:
            Reservation.objects.create(
                slug=row["Reservation"],
                check_in=row["Checkin"],
                check_out=row["Checkout"],
                flat=row["Flat"],
                city=row["City"],
                net_income=row["Net income, EUR"],
            )

    @property
    def commission(self):
        if self.city:
            city_incomes = set(Reservation.objects.filter(city=self.city.upper()).values_list('city','net_income'))
            return {f"{self.city.upper()}": sum(self.GRC.get(income[0]) * income[1] for income in city_incomes)}
        city_incomes = set(Reservation.objects.values_list('city','net_income'))
        return {"total": sum(self.GRC.get(income[0]) * income[1] for income in city_incomes)}

     
    @property
    def dict_commission(self):
        city_incomes = Reservation.objects.values('city', 'net_income', 'check_in', 'check_out')
        monthly_grc = list(map(self.count_per_month, city_incomes))
        counter = Counter()
        for x in monthly_grc: 
            counter.update(x)
        return {"monthly_grc": {key : round(dict(counter)[key], 2) for key in dict(counter)}}

    def count_per_month(self, income):
        grc_per_day = (
            self.GRC.get(income['city']) * income['net_income'] / 
            (income['check_out'] - income['check_in']).days
        )
        days_in_month = []
        monthly_grc = {}
        start_day = income['check_in'].day
        for dt in rrule.rrule(rrule.DAILY, dtstart=income['check_in'], until=income['check_out']):
            if dt.day != 1 or start_day == 1:
                days_in_month.append(dt)
                start_day = 0
            else:
                days_in_month.clear()
                days_in_month = [dt]
                prev_month = dt - timedelta(days=1)
                monthly_grc[prev_month.strftime("%m/%Y")] = (
                   monthly_grc[prev_month.strftime("%m/%Y")] + 1 * grc_per_day
                )
            monthly_grc[dt.strftime("%m/%Y")] = (
                (days_in_month[-1] - days_in_month[0]).days * grc_per_day
            )
        return monthly_grc
        