from django.shortcuts import redirect, render
from .forms import CreateUserForm

# not needed if login redirect set in settings
def profile(request):
    return redirect('home')

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, 'signup.html', {'form':form})
