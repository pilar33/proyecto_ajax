from django.shortcuts import render, redirect
# Create your views here.
from .forms import CustomUserCreationForm
from django.contrib import messages


def registro(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # Agregar mensaje de éxito
        messages.success(request, "Usuario registrado correctamente.")
        return redirect('login')
    return render(request, 'registration/register.html', {'form': form})


