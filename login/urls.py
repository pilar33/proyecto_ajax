from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import registro

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('register/', registro, name="register"),
    # path('accounts/', include('django.contrib.auth.urls')), 
]