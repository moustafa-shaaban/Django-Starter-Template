from django.shortcuts import render, redirect
from .forms import ProfileForm

def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})