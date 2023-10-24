import pytest
from django.test import RequestFactory
from django.urls import reverse
from usuarios.models import Usuario
from usuarios.views import login
from usuarios.models import Cliente
import json

@pytest.mark.django_db
def test_login_exitoso():
    user = Usuario(
        tipoid = 'CC',
        numid= 1234,
        nombre= 'Juanito',
        apellido = 'alcachofa',
        genero = 'masculino',
        correo = 'juanitoA@gmail.com',
        usuario = 'juanAlca',
        contrasena = '1234'
    )
    user.save()
    cliente = Cliente(tipoidusuario = 'CC',
    numidusuario = 1234,
    direccion = 'calle asdasdasd')
    cliente.save()
    request = RequestFactory().get(reverse('login'), {'usuario': 'juanAlca', 'contrasenia': '1234', 'rol': 'cliente'})
    
    assert json.loads(login(request))['mensaje'] == "Login exitoso."
@pytest.mark.django_db
def test_login_contrasena_incorrecta():
    user = Usuario(
        tipoid = 'CC',
        numid= 1234,
        nombre= 'Juanito',
        apellido = 'alcachofa',
        genero = 'masculino',
        correo = 'juanitoA@gmail.com',
        usuario = 'juanAlca',
        contrasena = '1234'
    )
    user.save()
    cliente = Cliente(tipoidusuario = 'CC',
    numidusuario = 1234,
    direccion = 'calle asdasdasd')
    cliente.save()
    request = RequestFactory().get(reverse('login'), {'usuario': 'juanAlca', 'contrasenia': '12345', 'rol': 'cliente'})
    
    assert json.loads(login(request))['mensaje'] == "Login exitoso."
 
@pytest.mark.django_db
def test_login_usuario_incorrecto():
    user = Usuario(
        tipoid = 'CC',
        numid= 1234,
        nombre= 'Juanito',
        apellido = 'alcachofa',
        genero = 'masculino',
        correo = 'juanitoA@gmail.com',
        usuario = 'juanAlca',
        contrasena = '1234'
    )
    user.save()
    cliente = Cliente(tipoidusuario = 'CC',
    numidusuario = 1234,
    direccion = 'calle asdasdasd')
    cliente.save()
    request = RequestFactory().get(reverse('login'), {'usuario': 'pedro', 'contrasenia': '1234', 'rol': 'cliente'})
    
    assert json.loads(login(request))['mensaje'] == "Login exitoso."
