from django.shortcuts import render, redirect
from .models import UsuUsuario
from .forms import UsuarioForm
from .models import UsuCatTipoUsuario
from .models import UsuCatEstado
from .models import Producto, ProCatCategoria, ProCatSubCategoria
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ProductoForm
from .models import VenVenta
from datetime import datetime
from django.http import JsonResponse
from .models import VenVentaProducto





from django.shortcuts import render, redirect
from .models import UsuUsuario
from .forms import UsuarioForm
from .models import UsuCatTipoUsuario
from .models import UsuCatEstado
from .models import VenVentaCategoria

 

def sesion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        contraseña = request.POST['contraseña']
   
        try:
            usuario = UsuUsuario.objects.get(strNombre=nombre_usuario, strPassword=contraseña)
        except UsuUsuario.DoesNotExist:
            return render(request, 'login.html', {'error_message': 'Usuario o contraseña incorrectos'})
        
        return redirect('principal') 
        
    return render(request, 'login.html')    


def bienvenida(request):
    return render(request, 'bienvenida.html')
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UsuCatTipoUsuario, UsuCatEstado
from .forms import UsuarioForm  

def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)  
        if form.is_valid(): 
            form.save()  
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('bienvenida')
        else:
            messages.error(request, 'Error en el formulario. Por favor, corrige los errores e intenta de nuevo.')
            return redirect('bienvenida')
    else:
        tipos_usuario = UsuCatTipoUsuario.objects.all()
        estados = UsuCatEstado.objects.all()
        form = UsuarioForm() 
        return render(request, 'agregar_usuario.html', {
            'form': form,
            'tipos_usuario': tipos_usuario,
            'estados': estados,
        })
    
   
from django.core.paginator import Paginator

def bienvenida(request):
    lista_usuarios =  UsuUsuario.objects.all()  
    paginator = Paginator(lista_usuarios, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bienvenida.html', {'page_obj': page_obj})



from django.shortcuts import render, redirect, get_object_or_404
from .models import UsuUsuario, VenVenta, VenVentaProducto

def eliminar_usuario(request, usuario_id):
   
    usuario = get_object_or_404( UsuUsuario,id=usuario_id)
    
    if request.method == 'POST':
       
        usuario.delete()
  
        return redirect('bienvenida') 

    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

from django.shortcuts import render, redirect


def editar_usuario(request, usuario_id):
    usuario = UsuUsuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        estado = request.POST.get('estado')
        tipo_usuario = request.POST.get('tipo_usuario')
        
     
        usuario.strNombre = nombre
        usuario.idUsuCatEstado = estado
        usuario.idUsuCatTipoUsuario = tipo_usuario
        usuario.save()

       
        return redirect('bienvenida')

    return render(request, 'EditarUsuario.html', {'usuario': usuario})

def buscar_usuarios(request):
    nombre = request.GET.get('nombre')
    estado = request.GET.get('estado')
    tipo = request.GET.get('tipo')

    usuarios =UsuUsuario.objects.all()

    if nombre:
        usuarios = usuarios.filter(strNombre__icontains=nombre)
    if estado:
        usuarios = usuarios.filter(idUsuCatEstado=estado)
    if tipo:
        usuarios = usuarios.filter(idUsuCatTipoUsuario=tipo)

    return render(request, 'tu_template.html', {'usuarios': usuarios})





from django.core.paginator import Paginator

def producto(request):
    categorias = ProCatCategoria.objects.all()
    subcategorias = ProCatSubCategoria.objects.all()
    productos = Producto.objects.all()

    # Definir la cantidad de productos por página
    productos_por_pagina = 4

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        subcategoria_id = request.POST.get('subcategoria')
        nombre_producto = request.POST.get('nombre_producto')  

        if categoria_id:
            productos = Producto.objects.filter(idProCatCategoria=categoria_id)
        elif subcategoria_id:
            productos = Producto.objects.filter(idProCatSubCategoria=subcategoria_id)
        
        if nombre_producto:
            productos = productos.filter(StrNombrePro__icontains=nombre_producto)
    
    # Inicializar el paginador
    paginator = Paginator(productos, productos_por_pagina)
    
    # Obtener el número de página
    page_number = request.GET.get('page')
    
    # Obtener los objetos de la página actual
    page_obj = paginator.get_page(page_number)

    return render(request, 'producto.html', {'categorias': categorias, 'subcategorias': subcategorias, 'productos': page_obj})

def agregar_producto(request):
    categorias = ProCatCategoria.objects.all()
    subcategorias = ProCatSubCategoria.objects.all()

    if request.method == 'POST':
       
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        tipo_producto_id = request.POST.get('tipo_producto')  
        subtipo_producto_id = request.POST.get('subtipo_producto')  
        maximo = request.POST.get('maximo')
        minimo = request.POST.get('minimo')
        costo = request.POST.get('costo')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        
     
        tipo_producto = ProCatCategoria.objects.get(idCat=tipo_producto_id)
        subtipo_producto = ProCatSubCategoria.objects.get(idSubCat=subtipo_producto_id)
        
     
        producto = Producto(
            StrNombrePro=nombre,
            StrDescriptcion=descripcion,
            idProCatCategoria=tipo_producto,
            idProCatSubCategoria=subtipo_producto,
            decMaximo=maximo,
            decMinimo=minimo,
            curCosto=costo,
            curPrecio=precio,
            stock=stock
        )
        
  
        producto.save()

    
        return redirect('producto')

    else:
        # Renderizar el formulario de agregar producto
        return render(request, 'agregar_producto.html', {'categorias': categorias, 'subcategorias': subcategorias})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, VenVentaProducto

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, idPro=producto_id)
    
    if request.method == 'POST':
        # Eliminar registros relacionados en VenVentaProducto
        VenVentaProducto.objects.filter(idProProducto=producto_id).delete()
        
        # Eliminar el producto
        producto.delete()
        
        # Redirigir a la página de productos
        return redirect('producto')
    
    return render(request, 'eliminar_producto.html', {'producto': producto})


from django.shortcuts import render, redirect
from .forms import ProductoForm  # Importa tu formulario

def editar_producto(request, producto_id):
    producto = Producto.objects.get(idPro=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto) 
        if form.is_valid():
            form.save()
            return redirect('producto')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'editar_producto.html', {'form': form, 'producto_id': producto_id})

def puntoventa(request):
    return render(request, 'Puntoventa.html') 



from .models import ProCatCategoria, ProCatSubCategoria
from .models import Producto


from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers

def agregar_venta(request):
    if request.method == 'POST':
        # Obtener el ID del usuario actual
        id_usuario = request.user.id

        # Generar un nuevo folio (puedes implementar tu lógica para generar un nuevo folio aquí)
        nuevo_folio = 'FOLIO-GENERADO'

        # Obtener el ID de la categoría 'Completada'
        categoria_completada = VenVentaCategoria.objects.get(strNombreVentaCategoria='Completada')
        id_categoria_completada = categoria_completada.idVenCat

        # Obtener la fecha actual
        fecha_actual = datetime.now().date()

        # Crear una nueva venta
        nueva_venta = VenVenta(
            idUsuUsuario=id_usuario,
            strFolio=nuevo_folio,
            dtFecha=fecha_actual,
            idVenCatEstado=id_categoria_completada
        )
        nueva_venta.save()

        # Obtener el ID de la venta recién creada
        id_ven_venta = nueva_venta.idVenta

        # Obtener los productos agregados al carrito
        productos_carrito = request.session.get('productos_carrito', [])

        # Guardar cada producto del carrito en la tabla VenVentaProducto
        for producto in productos_carrito:
            id_pro_producto = producto['id']
            dec_cantidad = producto['cantidad']
            cur_total = producto['total']

            venta_producto = VenVentaProducto(
                idVenVenta=id_ven_venta,
                idProProducto=id_pro_producto,
                decCantidad=dec_cantidad,
                curTotal=cur_total
            )
            venta_producto.save()

        return redirect('puntoventa')

    folios = VenVenta.objects.values_list('strFolio', flat=True).distinct()
    categorias = ProCatCategoria.objects.all()
    subcategorias = ProCatSubCategoria.objects.all()
    productos = []

    context = {'folios': folios, 'categorias': categorias, 'subcategorias': subcategorias, 'productos': productos}
    return render(request, 'agregar_venta.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import random
import string
from .models import VenVenta  # Importar el modelo VenVenta
from django.utils import timezone  # Importar timezone si aún no está importado

from django.db import transaction

@require_POST
def generar_venta(request):
    # Lógica para generar un nuevo folio
    folio = 'FOLIO-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    with transaction.atomic():
        # Obtener el último ID de venta y sumar 1
        id_venta = obtener_ultimo_id_venta() + 1  # Obtener el último ID de venta y sumar 1
        
        # Guardar la nueva venta en la base de datos
        id_usuario = 1  # Por ejemplo, aquí se debe establecer el ID del usuario que realiza la venta
        nueva_venta = guardar_venta_en_base_de_datos(folio, id_venta, id_usuario)  # Reemplaza 'id_usuario' con el ID de usuario apropiado
    
    # Devolver el folio y el ID de venta como respuesta JSON
    return JsonResponse({'folio': folio, 'idVenta': id_venta})

def obtener_ultimo_id_venta():
    # Lógica para obtener el último ID de venta de la base de datos
    ultimo_id_venta = VenVenta.objects.latest('idVenta').idVenta
    return ultimo_id_venta

def guardar_venta_en_base_de_datos(folio, id_venta, id_usuario):
    # Obtenemos la fecha actual
    fecha_actual = timezone.now().date()

    # Creamos una instancia del modelo VenVenta y la guardamos en la base de datos
    nueva_venta = VenVenta.objects.create(
        idVenta=id_venta,
        idUsuUsuario_id=id_usuario,  # Cambiar 'idUsuUsuario' por 'idUsuUsuario_id' para asignar el ID directamente
        strFolio=folio,
        dtFecha=fecha_actual,
        idVenCatEstado_id=1  # Asignamos un estado inicial para la venta, por ejemplo, el ID 1
    )

    # Retornamos la instancia de la venta recién creada
    return nueva_venta


def get_productos(request):
    categoria_id = request.GET.get('categoria_id')
    subcategoria_id = request.GET.get('subcategoria_id')
    
    print("categoria_id:", categoria_id)
    print("subcategoria_id:", subcategoria_id)

    productos = []
    if categoria_id and subcategoria_id:
        productos = Producto.objects.filter(idProCatCategoria=categoria_id, idProCatSubCategoria=subcategoria_id).values('idPro', 'StrNombrePro')
    
    return JsonResponse(list(productos), safe=False)

def get_producto_details(request):
    if request.method == 'GET':
        producto_id = request.GET.get('producto_id')
        producto = Producto.objects.get(idPro=producto_id)
        data = {
            'stock': producto.stock,
            'precio': producto.curPrecio,
        }
        return JsonResponse(data)


from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        # Redirige a la página de sesión después de cerrar sesión
        return redirect('sesion')  # Ajusta 'sesion' a la URL de tu página de sesión
    else:
        return render(request, 'logout.html')


def principal(request):
    return render(request, 'Principal.html')



import re
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import VenVentaProducto

from .models import VenVenta


@csrf_exempt
def almacenar_carrito(request):
    if request.method == 'POST':
        # Obtener los datos del carrito de compras del cuerpo de la solicitud
        data = json.loads(request.body.decode('utf-8'))
        
        # Obtener el folio del cuerpo de la solicitud
        folio = data.get('folio_input')
        
        # Extraer solo el número del folio
        folio_number = re.search(r'\d+', folio).group()
        
        try:
            idVenVenta = int(folio_number)
        except ValueError:
            return JsonResponse({'error': 'El folio debe ser un número entero válido'}, status=400)
        
        # Verificar si ya existe una venta con ese folio
        venta_existente = VenVenta.objects.filter(idVenta=idVenVenta).first()
        
        if not venta_existente:
            # Si no existe, crear una nueva venta
            nueva_venta = VenVenta(idVenta=idVenVenta)
            nueva_venta.save()
        
        for producto in data['productos_carrito']:
            idProProducto = producto.get('idProProducto')
            cantidad = producto.get('cantidad')
            total = producto.get('total')

            # Crear una instancia de VenVentaProducto y guardarla en la base de datos
            venta_producto = VenVentaProducto(
                idVenVenta=idVenVenta,  # Usar el folio convertido a entero
                idProProducto=idProProducto,
                decCantidad=cantidad,
                curTotal=total
            )
            venta_producto.save()

        return JsonResponse({'message': 'Los productos se han almacenado en el carrito correctamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)