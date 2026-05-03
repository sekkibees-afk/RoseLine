from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import HorseForm
from .models import Horse, Breed, Profile
from django.db.models import Q


def index(request):
    recent_horses = Horse.objects.order_by('-created_at')[:3]
    return render(request, "roseline/index.html", {"recent_horses":recent_horses})


@login_required
def horses(request):
    horses = Horse.objects.filter(owner=request.user)

    breed = request.GET.get("breed")
    gender = request.GET.get("gender")
    status = request.GET.get("status")
    query = request.GET.get("q")

    if breed:
        horses = horses.filter(breed__id=breed)

    if gender:
        horses = horses.filter(gender=gender)

    if status:
        horses = horses.filter(status=status)

    if query:
        horses = horses.filter(
            Q(name__icontains=query) |
            Q(brand_tag__icontains=query)
        )

    breeds = Breed.objects.all()

    return render(request, "roseline/horses.html", {
        "horses": horses,
        "breeds": breeds,
    })

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
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"stable_name": request.user.username}
    )

    if request.method == "POST":

        if "update_name" in request.POST:
            profile.stable_name = request.POST.get("stable_name") or request.user.username
            profile.save()

        if "update_avatar" in request.POST:
            if request.FILES.get("avatar"):
                profile.avatar = request.FILES.get("avatar")
                profile.save()

        if "delete_account" in request.POST:
            user = request.user
            logout(request)
            user.delete()
            return redirect("roseline:index")

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

def log_out(request):
    if request.method == "POST":
        logout(request)
    return redirect("roseline:index")