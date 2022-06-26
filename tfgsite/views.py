from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def index(request):
    if request.method == "GET":
        return render(request,"index.html")