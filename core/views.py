from django.contrib.auth import login
from django.shortcuts import redirect, render
from core.forms import CustomUserCreationForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def signUp(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email").lower()
            user = form.save(commit=False)
            user.username = email
            user.save()
            login(request,user)
            messages.success(request, f"User created and logged in successfully" )
            return redirect("/")
        
        else:
            return render(request, "sign-up.html", {"form": form})
    
    form = CustomUserCreationForm()
    
    return render(request, "sign-up.html", {"form": form})