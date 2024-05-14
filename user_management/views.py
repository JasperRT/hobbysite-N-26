from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .models import Profile
from .forms import ProfileForm, RegisterForm


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    update_form = ProfileForm()
    ctx = { "profile": profile, "update_form": update_form }
    if request.method == 'POST':
        update_form = ProfileForm(request.POST)
        if update_form.is_valid():
            profile.display_name = update_form.instance.display_name
            profile.email = update_form.instance.email
            profile.save()
            return render(request, 'user_management/profile_update.html', ctx)
    else:
        return render(request, 'user_management/profile_update.html', ctx)


def register(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            profile = Profile()
            profile.user = user
            profile.display_name = user.username
            profile.email = user.email
            profile.save()
            return redirect('home')
    else:
        reg_form = RegisterForm()
    ctx = { "reg_form": reg_form }
    return render(request, "user_management/register.html", ctx)
