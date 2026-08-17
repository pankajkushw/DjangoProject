from django.shortcuts import render, redirect
from bio_data.form import ProfileForm
from bio_data.models import Profile

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'bio_data/home.html', {'form': form})
