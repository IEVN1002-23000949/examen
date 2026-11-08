from flask import Flask, jsonify, request, Blueprint
from flask_mysqldb import MySQL
from flask_cors import CORS
from blueprints.pedidos.routes import pedidos_bp
from blueprints.ventas.routes import ventas_bp
 
from config import config
 
app = Flask(__name__)
app.register_blueprint(pedidos_bp)
app.register_blueprint(ventas_bp)
 
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
con = MySQL(app)
 
 
def pagina_no_encontrada(error):

    return "<h1>Pagina no encontrada</h1>"
 
 
if __name__ == "__main__":

    app.config.from_object(config['development'])

    app.register_error_handler(404, pagina_no_encontrada)

    app.run(host='0.0.0.0', port=5000)
 