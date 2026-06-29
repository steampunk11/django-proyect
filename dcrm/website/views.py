#dcrm/website/views.py
from django.shortcuts import render, redirect # type: ignore
from .forms import SignUpForm, AddRecordForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib import messages # type: ignore
from .models import Record # type: ignore
from django.core.paginator import Paginator # type: ignore

"""
def index(request):# type: ignore
    return render(request,'home.html',{})# type: ignore
"""

"""
esto es importante para el sistema por que ya empesamos a crear las vista  de la aplicacion , con eso empezamos a dar funcionalidad al sistmea home


"""
def home(request):
    records_list = Record.objects.all().order_by('-created_at')

    paginator = Paginator(records_list, 5)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)
    if request.method == 'POST':

        username = request.POST['username'] 
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)

            messages.success(request, "¡Has iniciado sesión exitosamente!")

            return redirect('home')

        else:

            messages.error(request, "¡Credenciales inválidas 🤐!")
            return redirect('home')

    else:
        return render(request, 'home.html', {'records': records})

def login_user(request):
    request.session.set_expiry(10)
def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')# type: ignore
    return redirect('home')

def add_record(request):# type: ignore
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar registros.')
        return redirect('home')

    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro agregado correctamente.')
            return redirect('home')
    else:
        form = AddRecordForm()

    return render(request, 'add_record.html', {'form': form})

def register_user(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
         
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido al sistema.')
            
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form':form})# type: ignore

def customer_record(request, pk):# type: ignore
    # esta vista es para mostrar el registro de un cliente específico en la plantilla
    # customer_record.html, utilizando el identificador único del cliente
    # (pk) para
    # obtener el registro correspondiente de la base de datos y renderizarlo en la plantilla.
    if request.user.is_authenticated:# type: ignore
        customer_record = Record.objects.get(id=pk) # type: ignore # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        return render(request, 'record.html', {'customer_record': customer_record})# type: ignore # se renderiza la plantilla record.html con el contexto del registro del cliente
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para ver los registros de los clientes.')# type: ignore # se muestra un mensaje de error al usuario
        return redirect('home')# type: ignore # se redirige al usuario a la página de inicio
    # esta vista es para mostrar el registro de un cliente específico en la plantilla
    # eliminar el registro de un cliente específico utilizando el identificador único del cliente (pk) para obtener el registro correspondiente de la base de datos y eliminarlo, mostrando un mensaje de éxito al usuario y redirigiendo al usuario a la página de inicio después de eliminar el registro del cliente.
    
def delete_record(request, pk):# type: ignore
    if request.user.is_authenticated:# type: ignore
        delete_it = Record.objects.get(id=pk) # type: ignore # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        delete_it.delete()# type: ignore # se elimina el registro del cliente de la base de datos
        messages.success(request, 'Registro eliminado correctamente.')# type: ignore # se muestra un mensaje de éxito al usuario
        return redirect('home')# type: ignore # se redirige al usuario a la página de inicio después de eliminar el registro del cliente
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para eliminar los registros de los clientes.')# type: ignore # se muestra un mensaje de error al usuario
        return redirect('home')# type: ignore # se redirige al usuario a la página de inicio    
    
def update_record(request, pk):# type: ignore
    if request.user.is_authenticated:# type: ignore
        current_record = Record.objects.get(id=pk) # type: ignore # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        form = AddRecordForm(request.POST or None, instance=current_record) # type: ignore # se crea una instancia del formulario de agregar registro con los datos enviados por el usuario o con los datos actuales del registro del cliente
        if form.is_valid():# type: ignore # se valida el formulario de agregar registro
            form.save()# type: ignore # se guarda el registro del cliente actualizado en la base de datos
            messages.success(request, 'Registro actualizado correctamente.')# type: ignore # se muestra un mensaje de éxito al usuario
            return redirect('home')# type: ignore # se redirige al usuario a la página de inicio después de actualizar el registro del cliente
        return render(request, 'update_record.html', {'form': form})# type: ignore # se renderiza la plantilla update_record.html con el contexto del formulario de agregar registro
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para actualizar los registros de los clientes.')# type: ignore # se muestra un mensaje de error al usuario
        return redirect('home')# type: ignore # se redirige al usuario a la página de inicio