from django.urls import path

from . import views

urlpatterns = [
    path('recurso_list/', views.recurso_list, name='recurso_list'),
    path('recurso_addget/<int:id>', views.recurso_addget, name='recurso_addget'),
    path('estado_byid/<int:id>', views.estado_byid, name='estado_byid'),
]
