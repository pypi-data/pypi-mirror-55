from django.template.loader import render_to_string
from django.conf import settings


CAMPOS_ENCABEZADOS = (
    ("unique_creator_id", "int"),
    ("instrucciones_especiales", "str"),
    ("numero_pedido_comprador", "int"),
    ("fecha_pedido_comprador", "date"),
    ("numero_pedido_comprador", "int"),
    ("numero_nota", "int"),
    ("ngl_comprador", "int"),
    ("nombre_departamento", "str"),
    ("ngl_vendedor", "int"),
    ("ngl_envio", "int"),
    ("nombre_envio", "str"),
    ("calle_envio", "str"),
    ("ciudad_envio", "str"),
)

CAMPOS_DETALLE = (
    ("lote_producto", "str"),
    ("numero_pedimento", "str"),
    ("fecha_produccion", "date"),
    ("numero_comprador", "str"),
    ("fecha_entrada", "date"),
)

def generar_addenda(diccionario):
    return render_to_string("cfdi/addendas/amece.xml", diccionario)
