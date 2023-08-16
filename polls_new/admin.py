
from .models import TouristPlace, PaymentItem, PaymentItemAdmin, TouristPlaceAdmin


# account/admin.py
from django.contrib import admin


admin.site.register(TouristPlace, TouristPlaceAdmin)
admin.site.register(PaymentItem, PaymentItemAdmin)