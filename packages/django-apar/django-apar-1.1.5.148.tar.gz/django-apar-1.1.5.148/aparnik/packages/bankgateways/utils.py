# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from zeep import Client

from aparnik.packages.shops.payments.models import Payment
from aparnik.settings import aparnik_settings, Setting
from .zarinpals.views import send_request as zarinpal_send_request
from .bmi.views import send_request as bmi_send_request
# from .models import Bank


def send_to_bank(request, payment):
    try:
        bmi_send_request(request=request, payment=payment)
    except:
        zarinpal_send_request(request=request, payment=payment)