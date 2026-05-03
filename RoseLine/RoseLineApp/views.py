from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import HorseForm
from .models import Horse
from django.db.models import Q


def index(request):
    return render(request, "roseline/index.html")


@login_required
def horses(request):
    horses = Horse.objects.filter(owner=request.user, status="ACTIVE")
    return render(request, "roseline/horses.html", {"horses": horses})


@login_required
def horse_detail(request, slug):
    horse = get_object_or_404(Horse, slug=slug)

    siblings = Horse.objects.filter(
        sire=horse.sire,
        dam=horse.dam
    ).exclude(id=horse.id)

    offspring = Horse.objects.filter(
        Q(sire=horse) | Q(dam=horse)
    )

    grandparents = [
        horse.sire.sire if horse.sire and horse.sire.sire else None,
        horse.sire.dam if horse.sire and horse.sire.dam else None,
        horse.dam.sire if horse.dam and horse.dam.sire else None,
        horse.dam.dam if horse.dam and horse.dam.dam else None,
    ]

    context = {
        "horse": horse,
        "sire": horse.sire,
        "dam": horse.dam,
        "siblings": siblings,
        "offspring": offspring,
        "grandparents": grandparents,
    }

    return render(request, "roseline/horse_detail.html", context)

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