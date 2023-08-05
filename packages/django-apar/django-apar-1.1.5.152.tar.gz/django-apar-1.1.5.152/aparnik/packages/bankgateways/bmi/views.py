# -*- coding: utf-8 -*-
import requests
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from zeep import Client
import datetime
import json
from Crypto.Cipher import DES3
import base64
import logging

from aparnik.packages.shops.payments.models import Payment
from aparnik.settings import aparnik_settings, Setting
# from .models import Bank

logging.basicConfig()

def send_request(request, payment):
    order = payment.order_obj
    order_id = order.id
    total_cost = int(order.get_total_cost())
    # TODO: change the link
    API_URL_REQUEST = 'https://sadad.shaparak.ir/vpg/api/v0/Request/PaymentRequest'
    call_back_url = request.build_absolute_uri(reverse('aparnik:bank_gateways:bmi:verify', args=[payment.uuid]))
    merchent_code = Setting.objects.get(key='BANK_MELLI_MERCHENT_CODE').get_value()
    terminal_id = Setting.objects.get(key='BANK_MELLI_TERMINAL_CODE').get_value()
    time_now = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S %P')
    init_data = {
        'TerminalId': terminal_id,
        'MerchantId': merchent_code,
        'Amount': total_cost,
        'SignData': encrypt_des3(terminal_id, order_id, total_cost),
        'ReturnUrl': call_back_url,
        'LocalDateTime': time_now,
        'OrderId': order_id,
        'AdditionalData':  'like username, app_name or etc'
    }

    init_response = requests.post(API_URL_REQUEST, json=init_data)
    response_json = get_json(init_response)
    if response_json['ResCode'] == 0:
        token = response_json['Token']
        url = "https://sadad.shaparak.ir/VPG/Purchase?Token=%s"%token;
        return redirect(url)
    else:
        logging.log(logging.INFO, response_json)
        print(response_json)
        raise Http404  # HttpResponse('Error code: ' + str(result.Status))

def verify(request, uuid):
    return uuid

def get_json(resp):
    """
    :param response:returned response as json when sending a request
    using 'requests' module.

    :return:response's content with json format
    """

    return json.loads(resp.content.decode('utf-8'))


def pad(text,pad_size=16):
    text_length = len(text)
    last_block_size = text_length % pad_size
    remaining_space = pad_size - last_block_size

    text = text + (remaining_space*chr(remaining_space))

    return text

def encrypt_des3(terminal_id, order_id, amount):
    """

    :param terminal_id: String-for example: EUDuTQrp
    :param order_id: integer- for example: 123456
    :param amount: integer - for example: 60000
    :return: encrypt "terminal_id;oreder_id;integer"
    """
    secret_key_bytes = base64.b64decode(Setting.objects.get(key='BANK_MELLI_SECRET_KEY').get_value())
    text = '%s;%s;%s'%(terminal_id, order_id, amount)
    text = pad(text,8)
    cipher = DES3.new(secret_key_bytes, DES3.MODE_ECB)
    my_export = cipher.encrypt(str.encode(text))

    return base64.b64encode(my_export).decode("utf-8")