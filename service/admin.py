import io

from django.contrib import admin
from django.contrib import admin, messages
from django.forms import forms as django_forms
from django.shortcuts import redirect, render
from django.urls import path

from .models import Reservation
from .business_logic.guest_ready import GuestReadyCommission


class CsvImportForm(django_forms.Form):
    csv_file = django_forms.FileField(label="")

@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    ordering = ('slug',)
    change_list_template = 'import_changelist.html'
    list_display = (
        'slug',
        'check_in',
        'check_out',
        'flat',
        'city',
        'net_income',
    )

    def get_urls(self):
            urls = super().get_urls()
            my_urls = [
                path('import_reservations/', self.import_reservations, name='import_reservations'),
            ]
            return my_urls + urls

    def import_reservations(self, request):
        form = CsvImportForm()
        payload = {
            "form": form,
        }
        params = {}
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            csv_file.seek(0)
            params["file"] = io.TextIOWrapper(csv_file.file, encoding='utf-8')
            try:
                msg = GuestReadyCommission(params).read()
                self.message_user(request, msg, level=messages.SUCCESS)
            except Exception as err:
                self.message_user(request, err, level=messages.ERROR)
                return render(
                    request, 'reservation_form.html', payload
                )
            return redirect('..')
        return render(
            request, 'reservation_form.html', payload
        )