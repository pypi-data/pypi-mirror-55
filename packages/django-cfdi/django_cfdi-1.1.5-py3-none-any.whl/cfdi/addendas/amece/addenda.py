from django.template.loader import render_to_string
from django.conf import settings


CAMPOS_ENCABEZADOS = (
    ("unique_creator_id", "int"),
    ("fecha_entrega", "date"),
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

def generar_addenda(diccionario):
    return render_to_string("cfdi/addendas/amece.xml", diccionario)
