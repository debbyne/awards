from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'awards'

urlpatterns=[
    path('',views.index, name = 'index'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile, name='profile'),
    re_path(r'^newProjectForm/$', views.newProjectForm, name='newProjectForm'),
    path('logout/', views.logoutUser, name='logout'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/profile/', views.ProfileList.as_view()),
    path('api/project/', views.ProjectList.as_view()),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
