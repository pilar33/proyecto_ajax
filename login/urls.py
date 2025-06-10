from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('accounts/', include('django.contrib.auth.urls')), 
]