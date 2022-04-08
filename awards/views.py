from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Profile,Project,Review


# Create your views here.
def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'django_registration/registration_form.html', {'form': form})

def loginrequest(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"loginform": form})

@login_required(login_url='/accounts/login')
def index(request):
    title = "Awwards"
    current_user = request.user
    projects = Project.get_all_projects()
    return render(request, 'index.html',{'title':title,'current_user':current_user,'projects':projects})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    projects = Project.objects.filter(user_id= current_user.id).all()

    return render(request,'profile.html',{'current_user':current_user,'projects':projects})

def logoutUser(request):
 logout(request)
 return redirect(index)
