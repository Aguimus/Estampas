from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from .models import Cliente
from .models import Artista
from .models import Admin
from .models import Camiseta,Catalogocamiseta,Catalogoestampa,Estampa, Factura
from django.db.models import Q
import re
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
            except Cliente.DoesNotExist:
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
                                        nombre=request.GET.get('nombre'), apellido=request.GET.get('apellido'),
                                        genero=request.GET.get('genero'), correo=request.GET.get('correo'),
                                        usuario=request.GET.get('usuario'), contrasena=request.GET.get('contrasena'))

        print(nuevo_usuario)
        print("se creo usuario")

        #registro cliente
        if request.GET.get('rol')=='cliente' and request.GET.get('direccion', None) is not None:
            nuevo_usuario.save()
            nuevo_cliente = Cliente (numidusuario = Usuario.objects.get(numid =request.GET.get('numid')),
                                      tipoidusuario = request.GET.get('tipoid'),
                                        direccion =request.GET.get('direccion'))
            print(nuevo_cliente)
            nuevo_cliente.save()
            print("se creo cliente")
            nuevo_usuario.save()
            return response
        elif(request.GET.get('rol')=='artista'):
            nuevo_usuario.save()#registro artista
            nuevo_artista = Artista (tipoidusuario = request.GET.get('tipoid'), numidusuario = Usuario.objects.get(numid =request.GET.get('numid')), utilidad = 0, numventas =0)
            nuevo_artista.save()
            
            print("se creo artista")
            return response
        
        
        return HttpResponse('fallo en el registro')
    else:
        return HttpResponse('fallo en el registro')
    
def catcamiseta(request):
    catcamiseta = Catalogocamiseta.objects.filter(cantdisponible__gt=0)
    data = list()  # wrap in list(), because QuerySet is not JSON serializable
    for o in catcamiseta:
        ##print(o.idcamiseta.idcamiseta)
        camiseta = Camiseta.objects.filter(idcamiseta = o.idcamiseta.idcamiseta).values()
        for i in camiseta:
            response_data = {
            'idcatcamiseta': o.idcatcamiseta,
            'cantcamiseta': o.cantdisponible,
            'informacion': i
            }
            data.append(response_data)
        
    print("rs ",response_data)
    jsonList = json.dumps(data, default=str)
    #print(jsonList)

    
    return HttpResponse(jsonList, content_type='application/json')

def catestampa(request):
    catestampa = Catalogoestampa.objects.filter(cantdisponible__gt=0)
    data = list()
    for o in catestampa:
        estampa = Estampa.objects.filter(idestampa = o.idestampa.idestampa, disponible = True).values()
        for i in estampa:
            usuario = Usuario.objects.get(tipoid = i.get('tipoidartista'), numid = i.get("numidartista"))
            print("user" + usuario.usuario)
            response_data = {
            'cantestampa': o.cantdisponible,
            'informacionEstampa': i,
            'nombre_artista' : usuario.nombre,
            'apellido_artista':usuario.apellido,
            'usuario_artista': usuario.usuario
            }
            data.append(response_data)
            
    print("rs ",response_data)
    jsonList = json.dumps(data, default=str)    
    return HttpResponse(jsonList, content_type='application/json')

def usuarioID(request):
    try:
        usuarioObtenido = Usuario.objects.get(usuario=request.GET.get('usuario'))
        print("usuarioid ", usuarioObtenido.numid, " usuariotipoid ", usuarioObtenido.tipoid)
        data = {
            'tipoid': usuarioObtenido.tipoid,
            'numid': usuarioObtenido.numid
        }
        
        jsonList = json.dumps(data, default=str)    
        return HttpResponse(jsonList, content_type='application/json')
    except Usuario.DoesNotExist:
        usuarioObtenido = None
    return HttpResponse('No existe el usuario')
@csrf_exempt
def generarFactura(request):
    factura = None
    
    try:
        factura = Factura(idfactura = request.GET.get('idfactura'),
                        tipoidcliente = request.GET.get('tipoidcliente'),
                        numidcliente = request.GET.get('numidcliente'),idcamiseta =  Camiseta.objects.get(idcamiseta = request.GET.get('idcamiseta')),
                        idestampa = Estampa.objects.get(idestampa = request.GET.get('idestampa')), preciototal = request.GET.get('preciototal'))
        factura.save()
        print("Se creo la factura")
        return HttpResponse('Registro de factura exitoso')
    except Cliente.DoesNotExist:
        print ('no existe')
        return HttpResponse('el usuario no existe')
    
@csrf_exempt
def actualizarCantidad(request):
    try:
        actualizacion = Catalogocamiseta.objects.get(idcatcamiseta=request.GET.get('idcatcamiseta'))
        actualizacion.cantdisponible = actualizacion.cantdisponible - int(request.GET.get('cantidadComprada'))
        actualizacion.save()
        return HttpResponse('Actaulización de cantidad completa')
    except Catalogocamiseta.DoesNotExist:
        actualizacion = None
        return HttpResponse('No se encontro la camiseta')
    
@csrf_exempt   
def actualizarVentas(request):
    try:
        artista = Artista.objects.get(tipoidusuario = request.GET.get('tipoidusuario'), numidusuario = request.GET.get('numidusuario'))
        artista.utilidad = artista.utilidad + int(request.GET.get('nuevaUtilidad'))
        artista.numventas = artista.numventas + int(request.GET.get('cantidadComprada'))
        artista.save()
        return HttpResponse('Actualización de utilidad completa')
    except Artista.DoesNotExist:
        artista = None
        return HttpResponse('No se encontro el artista')

@csrf_exempt  
def nuevaEstampa (request):
    try:
        # Obtén todos los registros y ordénalos en Python
        registros_ordenados = sorted(Estampa.objects.all(), key=lambda x: int(x.idestampa[2:]))

        # Obtén el último registro
        ultimo_registro = registros_ordenados[-1] if registros_ordenados else None
        id_ultimo_registro = ultimo_registro.idestampa if ultimo_registro else None
        
        # Expresión regular para extraer la parte numérica de la cadena "ES"
        patron = re.compile(r'ES(\d+)')

        # Extraer la parte numérica del id del último registro
        coincidencia = patron.match(id_ultimo_registro)
        parte_numerica = int(coincidencia.group(1)) if coincidencia else None
        parte_numerica = parte_numerica + 1
        nuevaEstampa = None
        nuevaId = 'ES'+str(parte_numerica)

        #usuario = Usuario.objects.get(numid=request.GET.get('numidartista'))
        #print(Artista.objects.get(tipoidusuario=request.GET.get('tipoidartista'), numidusuario=usuario))
        
        nuevaEstampa = Estampa(idestampa = nuevaId, nombre = request.GET.get('nombre'),
                            descripcion = request.GET.get('descripcion'), imgurl = request.GET.get('imgurl'),
                            disponible = True,tema = request.GET.get('tema'), precio = request.GET.get('precio'),
                            rating = 1, tipoidartista = request.GET.get('tipoidartista'), 
                            numidartista = request.GET.get('numidartista'))
        nuevaEstampa.save()

        # Obtén todos los registros y ordénalos en Python
        registros_ordenados = sorted(Catalogoestampa.objects.all(), key=lambda x: int(x.idcatestampa[2:]))

        # Obtén el último registro
        ultimo_registro = registros_ordenados[-1] if registros_ordenados else None
        id_ultimo_registro = ultimo_registro.idcatestampa if ultimo_registro else None
        # Expresión regular para extraer la parte numérica de la cadena "ES"
        patron = re.compile(r'CE(\d+)')

        # Extraer la parte numérica del id del último registro
        coincidencia = patron.match(id_ultimo_registro)
        parte_numericaC = int(coincidencia.group(1)) if coincidencia else None
        parte_numericaC = parte_numericaC + 1

        nuevaidC = 'CE'+str(parte_numericaC)
        nuevoCat = Catalogoestampa(idcatestampa = nuevaidC, idestampa = Estampa.objects.get(idestampa = nuevaId), cantdisponible = 20)

        nuevoCat.save()
        
        return HttpResponse('Registro exitoso')
    except Estampa.DoesNotExist:
        return HttpResponse('ocurrio un error')

@csrf_exempt   
def actualizarEstampa(request):
    try:
        estampa = Estampa.objects.get(idestampa = request.GET.get('idestampa'))
        estampa.nombre = request.GET.get('nombre')
        estampa.descripcion = request.GET.get('descripcion')
        estampa.imgurl = request.GET.get('imgurl')
        estampa.tema = request.GET.get('tema')
        estampa.precio = request.GET.get('precio')
        estampa.disponible = request.GET.get('disponible')
        estampa.save()
        return HttpResponse('Actualización completa')
    except Estampa.DoesNotExist:
        estampa = None
        return HttpResponse('No se encontro la estampa')
    
@csrf_exempt   
def ventasArtista(request):
    try:
        artista = Artista.objects.get(tipoidusuario = request.GET.get('tipoidusuario'),numidusuario =  request.GET.get('numidusuario'))
        data = {
                'utilidad': artista.utilidad,
                'numventas': artista.numventas
            }
            
        jsonList = json.dumps(data, default=str)    
        return HttpResponse(jsonList, content_type='application/json')
    except Usuario.DoesNotExist:
        artista = None
        return HttpResponse('No existe el artista')


