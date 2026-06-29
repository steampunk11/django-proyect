#/dcrm/website/admin.py

# esto se configura con el fin de registrar el modelo Record en el admin de django para que se pueda administrar desde el panel de administración de django
from django.contrib import admin
from .models import Record
# Register your models here.
admin.site.register(Record)
