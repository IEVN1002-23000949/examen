

from flask import Blueprint, jsonify, request

from database import mysql
 
pedidos_bp = Blueprint(

    'pedidos',

    __name__,

    url_prefix='/api/pedidos'

)
 
 
def fila_a_diccionario(cursor, fila):

    columnas = [columna[0] for columna in cursor.description]

    return dict(zip(columnas, fila))
 
 
# GET: Listar todos los pedidos

@pedidos_bp.route("/", methods=['GET'])

def lista_pedidos():

    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        sql = "SELECT * FROM pedidos"

        cursor.execute(sql)
 
        datos = cursor.fetchall()

        pedidos = []
 
        for fila in datos:

            pedido = fila_a_diccionario(cursor, fila)

            pedidos.append(pedido)
 
        return jsonify({

            'pedidos': pedidos,

            'mensaje': 'Lista de pedidos',

            'exito': True

        }), 200
 
    except Exception as ex:

        return jsonify({

            'mensaje': 'Error {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()
 
 
# GET: Consultar un pedido y sus pizzas

@pedidos_bp.route("/<int:id_pedido>", methods=['GET'])

def leer_pedido(id_pedido):

    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        cursor.execute(

            "SELECT * FROM pedidos WHERE id_pedido=%s",

            (id_pedido,)

        )
 
        fila = cursor.fetchone()
 
        if fila is None:

            return jsonify({

                'mensaje': 'Pedido no encontrado',

                'exito': False

            }), 404
 
        pedido = fila_a_diccionario(cursor, fila)
 
        cursor.execute(

            "SELECT * FROM ventas WHERE id_pedido=%s",

            (id_pedido,)

        )
 
        datos = cursor.fetchall()

        ventas = []
 
        for fila in datos:

            venta = fila_a_diccionario(cursor, fila)

            ventas.append(venta)
 
        return jsonify({

            'pedido': pedido,

            'ventas': ventas,

            'exito': True

        }), 200
 
    except Exception as ex:

        return jsonify({

            'mensaje': 'Error al consultar el pedido {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()
 
 
# POST: Registrar un pedido

@pedidos_bp.route("/", methods=['POST'])

def registrar_pedido():
 
    datos = request.get_json(silent=True)
 
    if not isinstance(datos, dict):

        return jsonify({

            'mensaje': 'Se requiere un objeto JSON',

            'exito': False

        }), 400
 
    nombre = datos.get('nombre_cliente')

    direccion = datos.get('direccion')

    telefono = datos.get('telefono')

    fecha = datos.get('fecha_pedido')

    pizzas = datos.get('pizzas')
 
    if (

        not nombre or

        not direccion or

        not telefono or

        not fecha or

        not isinstance(pizzas, list) or

        len(pizzas) == 0

    ):

        return jsonify({

            'mensaje': 'Faltan datos del pedido o pizzas',

            'exito': False

        }), 400
 
    total = 0
 
    for pizza in pizzas:
 
        if not isinstance(pizza, dict):

            return jsonify({

                'mensaje': 'Datos de pizza inválidos',

                'exito': False

            }), 400
 
        tamano = pizza.get('tamano')

        ingredientes = pizza.get('ingredientes')

        cantidad = pizza.get('cantidad')

        subtotal = pizza.get('subtotal')
 
        if (

            not tamano or

            not ingredientes or

            not isinstance(cantidad, int) or

            cantidad <= 0 or

            not isinstance(subtotal, (int, float)) or

            isinstance(subtotal, bool) or

            subtotal < 0

        ):

            return jsonify({

                'mensaje': 'Datos de pizza incompletos o inválidos',

                'exito': False

            }), 400
 
        total += subtotal
 
    cursor = None
 
    try:

        cursor = mysql.connection.cursor()
 
        # Insertar los datos del cliente

        cursor.execute("""

            INSERT INTO pedidos

                (nombre_cliente, direccion, telefono, fecha_pedido, total)

            VALUES (%s, %s, %s, %s, %s)

        """, (

            nombre,

            direccion,

            telefono,

            fecha,

            total

        ))
 
        id_pedido = cursor.lastrowid
 
        # Insertar las pizzas del pedido

        for pizza in pizzas:
 
            ingredientes = pizza['ingredientes']
 
            if isinstance(ingredientes, list):

                ingredientes = ', '.join(ingredientes)
 
            cursor.execute("""

                INSERT INTO ventas

                    (id_pedido, tamano, ingredientes, cantidad, subtotal)

                VALUES (%s, %s, %s, %s, %s)

            """, (

                id_pedido,

                pizza['tamano'],

                ingredientes,

                pizza['cantidad'],

                pizza['subtotal']

            ))
 
        mysql.connection.commit()
 
        return jsonify({

            'mensaje': 'Pedido registrado correctamente',

            'id_pedido': id_pedido,

            'total': total,

            'exito': True

        }), 201
 
    except Exception as ex:

        mysql.connection.rollback()
 
        return jsonify({

            'mensaje': 'Error al registrar el pedido: {}'.format(ex),

            'exito': False

        }), 500
 
    finally:

        if cursor is not None:

            cursor.close()

 