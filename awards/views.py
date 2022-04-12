from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UpdateUserProfileForm, ProjectForm,RatingForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Profile,Project,Rates
from pickle import FALSE
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectsSerializer
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse


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
    current_user = User.objects.exclude(id=request.user.id)
    images = Project.objects.all()
    return render(request, 'index.html',{'title':title,'user':current_user,'images':images})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    projects = Project.objects.filter(user_id= current_user.id).all()

    profileForm = UpdateUserProfileForm()
    if request.method == 'POST':
        profileForm = UpdateUserProfileForm(request.POST, request.FILES)
        if profileForm.is_valid():
            profile=profileForm.save(commit=FALSE)
            profile.save()
        else:
        
            profileForm = UpdateUserProfileForm()


    return render(request,'profile.html',{'current_user':current_user,'projects':projects,'profileForm':profileForm})

def logoutUser(request):
 logout(request)
 return redirect(index)

@login_required(login_url='/accounts/login')
def search_results(request):

    if 'search_username' in request.GET and request.GET["search_username"]:
        search_term = request.GET.get("search_username")
        searched_username = Profile.search_profile(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message, 'profile':searched_username})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='login')
def newProjectForm(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            user = current_user
            image.save()
            
            return redirect('/')

    else:
        form = ProjectForm()
    return render(request, 'newproject.html', {"form": form})

class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectsSerializer(all_projects, many=True)
        return Response(serializers.data)


@login_required(login_url='/accounts/login')
def review(request, id):
    project = Project.objects.get(id=id)
    rate = Rates.objects.filter(user=request.user, project=project).first()
    ratings = Rates.objects.all()
    rating_status = None
    if rate is None:
        rating_status = False
    else:
        rating_status = True
    current_user = request.user
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            design = form.cleaned_data['design']
            usability = form.cleaned_data['usability']
            content = form.cleaned_data['content']
            review = Rates()
            review.project = project
            review.user = current_user
            review.design = design
            review.usability = usability
            review.content = content
            review.average = (
                review.design + review.usability + review.content)/3
            review.save()
            return HttpResponseRedirect(reverse('review', args=(project.id,)))
    else:
        form = RatingForm()
    params = {
        'project': project,
        'form': form,
        'rating_status': rating_status,
        'reviews': ratings,
        'ratings': rate
    }
    return render(request, 'projectdets.html', params)