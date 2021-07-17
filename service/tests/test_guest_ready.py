import csv
from datetime import datetime
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

from service import models
from service.admin import CsvImportForm
from service.business_logic.guest_ready import GuestReadyCommission

pytestmark = pytest.mark.django_db

def csv_from_dict(data, records=1):
    fieldnames = data.keys()
    csvfile = tempfile.NamedTemporaryFile(mode="w+")
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow(dict(zip(fieldnames, fieldnames)))
    for i in range(records):
        writer.writerow(data)
    csvfile.seek(0)
    return csvfile

class TestCSVForm:
    def test_client_upload_file(self, client):
        name = "test.csv"
        data = b'test1,test2'
        file = SimpleUploadedFile(name, data)
        file_model = CsvImportForm(file)
        file_model.data.seek(0)
        assert data == file_model.data.readline()
        assert name == file_model.data.name

    def test_client_file_upload(self, client):
        name = "test.csv"
        data = b'test1,test2'
        file = SimpleUploadedFile(name, data)
        response = client.post("/admin/service/reservation/import_reservations/", data={"csv_file": file, })
        assert response.status_code == 302

    def test_csv_import(self):
        data = dict([
            ('Reservation', "HMB0001"),
            ('Checkin', datetime(2021, 5, 12)),
            ('Checkout', datetime(2021, 6, 1)),
            ('Flat', "Hawtrey"),
            ('City', "LONDON"),
            ('Net income, EUR', 1200)])
        params = {}
        csvfile = csv_from_dict(data, records=1)
        params["file"] = csvfile
        GuestReadyCommission(params).read()
        csvfile.close()
        assert models.Reservation.objects.first().net_income == 1200
