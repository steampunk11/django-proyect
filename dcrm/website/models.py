#dcrm/ website/models.py
from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    # Método para que en el Admin de Django se vea el nombre y no "Record object"
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class schedule(models.Model):
    id_agendamiento = models.AutoField(primary_key=True)
    agendador = models.CharField(max_length=100)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    concepto = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    
    def __str__(self):
        return f"{self.agendador}"