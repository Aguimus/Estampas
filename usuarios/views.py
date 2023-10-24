from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from .models import Cliente
from .models import Artista
from .models import Admin
import json
from django.http import HttpResponse
# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'GET':
        response_data = {
        "mensaje": "Login exitoso.",
        "redireccion": "/usuario"
        }
        # Convertir el diccionario a formato JSON
        json_response = json.dumps(response_data)

        # Crear una respuesta JSON
        response = HttpResponse(json_response, content_type='application/json')

        # Redirigir al usuario a la URL especificada en el diccionario JSON
        response['Location'] = response_data["redireccion"]
        try:
            usuarioObtenido = Usuario.objects.get(usuario=request.GET.get('usuario'))
            print("usuario obtenido", usuarioObtenido)
        except Usuario.DoesNotExist:
            usuarioObtenido = None
            return HttpResponse('No existe el usuario')
        #caso cliente
        if request.GET.get('rol') == 'cliente':
            try:
                cliente = Cliente.objects.get(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Usuario.DoesNotExist:
                cliente = None
            if  usuarioObtenido is not None and cliente is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como cliente')
        #caso Artista
        if request.GET.get('rol') == 'artista':
            try:
                artista = Artista.objects.get(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Artista.DoesNotExist:
                artista = None
            if  usuarioObtenido is not None and artista is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como artista')
        #caso admin
        if request.GET.get('rol') == 'admin':
            try:
                admin = Admin.objects.get(tipoidusuario=usuarioObtenido.tipoid, numidusuario=usuarioObtenido.numid)
            except Admin.DoesNotExist:
                admin = None
            if  usuarioObtenido is not None and admin is not None:
                if(usuarioObtenido.contrasena == request.GET.get('contrasena')):
                    return response
                else:
                    return HttpResponse('Contraseña incorrecta')
            else:
                return HttpResponse('El usuario no existe como admin')
        else:
            return HttpResponse('Metodo no GET')

@csrf_exempt
def registro(request):
    nuevo_artista = None
    nuevo_cliente = None
    nuevo_usuario = None
    if request.method == 'POST':
        #creacion del json
        response_data = {
        "mensaje": "Registro exitoso.",
        "redireccion": "/api/login"
        }

        # Convertir el diccionario a formato JSON
        json_response = json.dumps(response_data)

        # Crear una respuesta JSON
        response = HttpResponse(json_response, content_type='application/json')

        # Redirigir al usuario a la URL especificada en el diccionario JSON
        response['Location'] = response_data["redireccion"]


        #registro usuario        
        print(request.GET.get('tipoid'))
        print(request.GET.get('numid'))
        print(request.GET.get('usuario'))
        
        try:
            usuario = Usuario.objects.get(tipoid=request.GET.get('tipoid'), numid=request.GET.get('numid'))
        except Usuario.DoesNotExist:
            usuario = None
        if  usuario is not None:
            return HttpResponse('El usuario no es valido')
        else:
            nuevo_usuario = Usuario(tipoid=request.GET.get('tipoid'), numid=request.GET.get('numid'),
                                        nombre=request.GET.get('nombre'), apellido=request.GET.get('apellido')
                                        , genero=request.GET.get('genero'), correo=request.GET.get('correo'),
                                        usuario=request.GET.get('usuario'), contrasena=request.GET.get('contrasena'))
                


        print(nuevo_usuario)
        print("se creo usuario")
        #print(Usuario.objects.get())
        

        #registro cliente
        if request.GET.get('rol')=='cliente' and request.GET.get('direccion', None) is not None:
            nuevo_cliente = Cliente (numidusuario = Usuario.objects.get(numid =request.GET.get('numid')),
                                      tipoidusuario = request.GET.get('tipoid'),
                                        direccion =request.GET.get('direccion'))
            nuevo_cliente.save()
            print("se creo cliente")
            nuevo_usuario.save()
            return response
        elif(request.GET.get('rol')=='artista'):    #registro artista
            nuevo_artista = Artista (tipoidusuario = request.GET.get('tipoid'), numidusuario = Usuario.objects.get(numid =request.GET.get('numid')), utilidad = 0, numventas =0)
            nuevo_artista.save()
            nuevo_usuario.save()
            print("se creo artista")
            return response
        
        
        return HttpResponse('fallo en el registro')
    else:
        return HttpResponse('fallo en el registro')