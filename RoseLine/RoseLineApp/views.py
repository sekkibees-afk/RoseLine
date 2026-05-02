from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import HorseForm


def index(request):
    return render(request, "roseline/index.html")


@login_required
def horses(request):
    return render(request, "roseline/horses.html")


@login_required
def horse_detail(request, slug):
    return render(request, "roseline/horse_detail.html", {"slug": slug})


@login_required
def account(request):
    return render(request, "roseline/account.html")


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("roseline:index")
        else:
            error = "Invalid username or password"

    return render(request, "roseline/login.html", {"error": error})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("roseline:login")
    else:
        form = UserCreationForm()

    return render(request, "roseline/signup.html", {"form": form})

@login_required
def add_horse(request):
    if request.method == "POST":
        form = HorseForm(request.POST)

        if form.is_valid():
            horse = form.save(commit=False)
            horse.owner = request.user
            horse.save()
            return redirect("roseline:horses")
    else:
        form = HorseForm()

    return render(request, "roseline/add_horse.html", {"form":form})