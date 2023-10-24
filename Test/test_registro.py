import pytest
from usuarios.models import Usuario
from usuarios.views import registro
from django.test import RequestFactory
from django.urls import reverse
import json



@pytest.mark.django_db
def test_user_creation():

    request = RequestFactory().get(reverse('registro'), {'tipoid': 'CC','numid': '1234','nombre': 'juanito',
                                                     'apellido': 'alcachofa','genero': 'helicoptero','correo': 'juanitoA@gmail.com'
                                                     ,'usuario': 'juanAlca', 'contrasenia': '1234', 'direccion': 'algun lugar', 'rol':'cliente'})
    data = json.loads(registro(request))
    assert data['mensaje'] == "Registro exitoso."
    
#caso falta de dirección en cliente
@pytest.mark.django_db
def test_user_creation():

    request = RequestFactory().get(reverse('registro'), {'tipoid': 'CC','numid': '1234','nombre': 'juanito',
                                                     'apellido': 'alcachofa','genero': 'helicoptero','correo': 'juanitoA@gmail.com'
                                                     ,'usuario': 'juanAlca', 'contrasenia': '1234'})

    assert json.loads(registro(request))['mensaje'] == "Registro exitoso."
