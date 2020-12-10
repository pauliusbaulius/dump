from django.shortcuts import render
from django.http import HttpResponse

import string
import random
import secrets
# Create your views here.

def index(request):
    #return HttpResponse("Hello, World!")
    length = int(request.GET.get("length", 16))
    uppercase = bool(request.GET.get("uppercase"))
    special = bool(request.GET.get("special"))
    numbers = bool(request.GET.get("numbers"))

    return render(request, "index.html", {"generated_password": generate_password(length, uppercase, special, numbers)})

def generate_password(length, uppercase, special, numbers):

    big_list = list(string.ascii_lowercase)
    big_list += list(string.ascii_uppercase) if uppercase else ""
    big_list += list(string.punctuation) if special else ""
    big_list += list(string.digits) if numbers else ""

    random.seed()
    return ''.join(secrets.choice(big_list) for x in range(length))
