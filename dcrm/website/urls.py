from django.urls import path
from . import views

urlpatterns = [ # type: ignore
    path('', views.home, name='home'), # type: ignore
    path('login/',views.login_user, name='login'),# type: ignore
    path('logout/', views.logout_user, name='logout'),# type: ignore
    path('register/', views.register_user, name='register'),# type: ignore
    path('add_record/', views.add_record, name='add_record'),# type: ignore
    path('record/<int:pk>/', views.customer_record, name='record'),# type: ignore# esta ruta es para mostrar los detalles de un registro específico, donde <int:pk> es el identificador del registro.
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),# type: ignore# esta ruta es para eliminar un registro específico, donde <int:pk> es el identificador del registro.
    path('update_record/<int:pk>/', views.update_record, name='update_record'),# type: ignore# esta ruta es para actualizar un registro específico, donde <int:pk> es el identificador del registro.
    path('scheduling/', views.scheduling, name='scheduling'),
    path('schedule/<int:pk>/', views.schedule_card, name='schedule_card'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('delete_schedule/<int:pk>/', views.delete_schedule, name='delete_schedule'),
    path('update_schedule/<int:pk>/', views.update_schedule, name='update_schedule'),     
]
