#dcrm/website/views.py
from django.shortcuts import render, redirect 
from .forms import SignUpForm, AddRecordForm, AddScheduleForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponse 
from django.contrib import messages 
from .models import Record, schedule
from django.core.paginator import Paginator 

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

def scheduling(request):
    schedules = schedule.objects.all().order_by('-fecha') 
    
    paginator = Paginator(schedules, 5)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)
    
    if request.user.is_authenticated:
        return render(request, 'scheduling.html', {'schedules': records})
    else:
        return redirect('home')

def login_user(request):
    request.session.set_expiry(3000)
    
def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

def add_record(request):
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

def add_schedule(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar registros.')
        return redirect('home')

    if request.method == 'POST':
        form = AddScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro agregado correctamente.')
            return redirect('scheduling')
    else:
        form = AddScheduleForm()

    return render(request, 'add_schedule.html', {'form': form})

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
    return render(request, 'register.html', {'form':form})

def schedule_card(request, pk):
    if request.user.is_authenticated:
        customer_schedule = schedule.objects.get(id_agendamiento=pk)
        return render(request, 'schedule.html', {'customer_schedule': customer_schedule})
    else:
        messages.error(request, 'Debes iniciar sesión para ver los registros de los clientes.')
        return redirect('home')

def customer_record(request, pk):
    # esta vista es para mostrar el registro de un cliente específico en la plantilla
    # customer_record.html, utilizando el identificador único del cliente
    # (pk) para
    # obtener el registro correspondiente de la base de datos y renderizarlo en la plantilla.
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)  # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        return render(request, 'record.html', {'customer_record': customer_record}) # se renderiza la plantilla record.html con el contexto del registro del cliente
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para ver los registros de los clientes.') # se muestra un mensaje de error al usuario
        return redirect('home') # se redirige al usuario a la página de inicio
    # esta vista es para mostrar el registro de un cliente específico en la plantilla
    # eliminar el registro de un cliente específico utilizando el identificador único del cliente (pk) para obtener el registro correspondiente de la base de datos y eliminarlo, mostrando un mensaje de éxito al usuario y redirigiendo al usuario a la página de inicio después de eliminar el registro del cliente.

def delete_schedule(request, pk):
    if request.user.is_authenticated:
        delete_it = schedule.objects.get(id_agendamiento=pk)
        delete_it.delete()
        messages.success(request, 'Registro eliminado correctamente.')
        return redirect('scheduling')
    else:
        messages.error(request, 'Debes iniciar sesión para eliminar los registros de los clientes.') # se muestra un mensaje de error al usuario
        return redirect('home') 
    
def update_schedule(request, pk): 
    if request.user.is_authenticated:
        current_schedule = schedule.objects.get(id_agendamiento=pk) 
        form = AddScheduleForm(request.POST or None, instance=current_schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado correctamente.') 
            return redirect('scheduling') 
        return render(request, 'update_schedule.html', {'form': form}) 
    else:
        messages.error(request, 'Debes iniciar sesión para actualizar los registros de los clientes.')
        return redirect('home')    
 
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)  # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        delete_it.delete() # se elimina el registro del cliente de la base de datos
        messages.success(request, 'Registro eliminado correctamente.') # se muestra un mensaje de éxito al usuario
        return redirect('home') # se redirige al usuario a la página de inicio después de eliminar el registro del cliente
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para eliminar los registros de los clientes.') # se muestra un mensaje de error al usuario
        return redirect('home') # se redirige al usuario a la página de inicio    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)  # se obtiene el registro del cliente correspondiente al identificador único (pk) de la base de datos
        form = AddRecordForm(request.POST or None, instance=current_record)  # se crea una instancia del formulario de agregar registro con los datos enviados por el usuario o con los datos actuales del registro del cliente
        if form.is_valid(): # se valida el formulario de agregar registro
            form.save() # se guarda el registro del cliente actualizado en la base de datos
            messages.success(request, 'Registro actualizado correctamente.') # se muestra un mensaje de éxito al usuario
            return redirect('home') # se redirige al usuario a la página de inicio después de actualizar el registro del cliente
        return render(request, 'update_record.html', {'form': form}) # se renderiza la plantilla update_record.html con el contexto del formulario de agregar registro
    else:# si el usuario no está autenticado, se muestra un mensaje de error y se redirige a la página de inicio
        messages.error(request, 'Debes iniciar sesión para actualizar los registros de los clientes.') # se muestra un mensaje de error al usuario
        return redirect('home') # se redirige al usuario a la página de inicio