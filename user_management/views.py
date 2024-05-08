from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Profile

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.email = request.POST['email']
        user.save()
        profile = Profile.objects.get(user=user)
        profile.display_name = request.POST['display_name']
        profile.save()
        return redirect('profile')

    return render(request, 'user_management/profile_update.html')
