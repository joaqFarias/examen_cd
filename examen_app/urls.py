from django.urls import path
from . import views, auth


urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('edit/user/<int:id>', views.edit),
    path('user/<int:id>', views.user),
    path('megusta/<int:id>/<int:id_cita>', views.megusta),
    path('borrar/<int:id_cita>', views.borrar),
]
