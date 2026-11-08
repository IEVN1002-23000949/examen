from flask import Blueprint, jsonify, request
from database import mysql
 
ventas_bp = Blueprint(

    'ventas',

    __name__,

    url_prefix='/api/ventas'

)
 
 
def fila_a_diccionario(cursor, fila):

    columnas = [columna[0] for columna in cursor.description]

    return dict(zip(columnas, fila))
 
 
# GET: Consultar ventas por día de la semana

@ventas_bp.route("/dia", methods=['GET'])

def ventas_por_dia():
 
    dia = request.args.get('dia')
 
    if not dia:

        return jsonify({

            'mensaje': 'Debe proporcionar un día',

            'exito': False

        }), 400
 
    dias = [

        'lunes', 'martes', 'miercoles',

        'jueves', 'viernes', 'sabado', 'domingo'

    ]
 
    if dia.lower() not in dias:

        return jsonify({

            'mensaje': 'Día no válido',

            'exito': False

        }), 400
 
    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        sql = """

            SELECT

                p.id_pedido,

                p.nombre_cliente,

                p.fecha_pedido,

                p.total

            FROM pedidos p

            WHERE DAYOFWEEK(p.fecha_pedido) =

                CASE LOWER(%s)

                    WHEN 'domingo' THEN 1

                    WHEN 'lunes' THEN 2

                    WHEN 'martes' THEN 3

                    WHEN 'miercoles' THEN 4

                    WHEN 'jueves' THEN 5

                    WHEN 'viernes' THEN 6

                    WHEN 'sabado' THEN 7

                END

            ORDER BY p.fecha_pedido

        """
 
        cursor.execute(sql, (dia,))
 
        datos = cursor.fetchall()

        ventas = []
 
        for fila in datos:

            venta = fila_a_diccionario(cursor, fila)

            ventas.append(venta)
 
        total_dia = sum(float(venta['total']) for venta in ventas)
 
        return jsonify({

            'ventas': ventas,

            'total_dia': total_dia,

            'mensaje': 'Ventas del día consultadas correctamente',

            'exito': True

        }), 200
 
    except Exception as ex:

        return jsonify({

            'mensaje': 'Error al consultar las ventas: {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()
 
 
# GET: Consultar ventas por mes

@ventas_bp.route("/mes", methods=['GET'])

def ventas_por_mes():
 
    mes = request.args.get('mes')
 
    meses = {

        'enero': 1,

        'febrero': 2,

        'marzo': 3,

        'abril': 4,

        'mayo': 5,

        'junio': 6,

        'julio': 7,

        'agosto': 8,

        'septiembre': 9,

        'octubre': 10,

        'noviembre': 11,

        'diciembre': 12

    }
 
    if not mes or mes.lower() not in meses:

        return jsonify({

            'mensaje': 'Mes no válido',

            'exito': False

        }), 400
 
    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        sql = """

            SELECT

                p.id_pedido,

                p.nombre_cliente,

                p.fecha_pedido,

                p.total

            FROM pedidos p

            WHERE MONTH(p.fecha_pedido) = %s

            ORDER BY p.fecha_pedido

        """
 
        cursor.execute(sql, (meses[mes.lower()],))
 
        datos = cursor.fetchall()

        ventas = []
 
        for fila in datos:

            venta = fila_a_diccionario(cursor, fila)

            ventas.append(venta)
 
        total_mes = sum(float(venta['total']) for venta in ventas)
 
        return jsonify({

            'ventas': ventas,

            'total_mes': total_mes,

            'mensaje': 'Ventas del mes consultadas correctamente',

            'exito': True

        }), 200
 
    except Exception as ex:

        return jsonify({

            'mensaje': 'Error al consultar las ventas: {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()
 
 
# GET: Consultar detalle de una venta

@ventas_bp.route("/detalle/<int:id_pedido>", methods=['GET'])

def detalle_venta(id_pedido):
 
    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        sql = """

            SELECT

                v.id_venta,

                v.id_pedido,

                v.tamano,

                v.ingredientes,

                v.cantidad,

                v.subtotal

            FROM ventas v

            WHERE v.id_pedido = %s

        """
 
        cursor.execute(sql, (id_pedido,))
 
        datos = cursor.fetchall()

        detalle = []
 
        for fila in datos:

            venta = fila_a_diccionario(cursor, fila)

            detalle.append(venta)
 
        if not detalle:

            return jsonify({

                'mensaje': 'No se encontraron pizzas para este pedido',

                'exito': False

            }), 404
 
        return jsonify({

            'detalle': detalle,

            'mensaje': 'Detalle de venta consultado correctamente',

            'exito': True

        }), 200
 
    except Exception as ex:

        return jsonify({

            'mensaje': 'Error al consultar el detalle: {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()

 