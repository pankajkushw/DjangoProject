from django.shortcuts import render
#instead of taking view data from view we will take it from forms
from appTwo.forms import NewUserForm
# Create your views here.


def index(request):
    return render(request, 'appTwo/index.html')

def users(request):
    form = NewUserForm()
    
    if request.method == "POST":
        form = NewUserForm(request.POST)

    if form.is_valid():
        form.save(commit=True)
        return index(request)
    else:
        print("Error form invalid")
    return render(request, 'appTwo/users.html', {'form':form})
    



