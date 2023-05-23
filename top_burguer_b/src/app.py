from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from pymysql import connect
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql.cursors

# Configura la aplicación Flask
app = Flask(__name__)


# JWT TOKENIZER
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'ultrasecret'  # replace with your secret key

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='leverna2003',
                                 db='INVENTORY_MANAGMENT',
                                 cursorclass=pymysql.cursors.DictCursor)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    user = data.get('user')
    password = data.get('password')
    role = data.get('role')
    hashed_password = generate_password_hash(password)
    
    try:
        connection.connect()
        with connection.cursor() as cursor:
            sql = "INSERT INTO Empleado (Nombre, Usuario, Contrasena, Rol) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name ,user, hashed_password, role))
            connection.commit()
        return jsonify({"message": "User created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')

    try:
        connection.connect()
        with connection.cursor() as cursor:
            sql = "SELECT Usuario, Contrasena, Rol FROM Empleado WHERE Usuario = %s"
            cursor.execute(sql, (user,))
            empleado = cursor.fetchone()
            if not empleado or not check_password_hash(empleado['Contrasena'], password):
                return jsonify({"error": "Invalid user or password"}), 401

            access_token = create_access_token(identity={"user": user, "role": empleado["Rol"]})
            return jsonify(access_token=access_token), 200

    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()


@app.route('/clientes', methods=['GET'])
def get_clientes():
    connection.connect()
    # Crea una conexión a la base de datos
    try:
        with connection.cursor() as cursor:
            # Consulta los nombres de los clientes
            sql = "SELECT Nombre FROM Cliente"
            cursor.execute(sql)
            clientes = cursor.fetchall()
            nombres = [cliente['Nombre'] for cliente in clientes]
            
            return jsonify(nombres)

    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()


@app.route('/proveedores', methods = ['GET'])
def get_proveedores():
    connection.connect()
    try:
        with connection.cursor() as cursor:
            # Consulta los nombres de los clientes
            sql = "SELECT ID_Proveedor, Nombre, Telefono, Direccion FROM Proveedor;"
            cursor.execute(sql)
            
            # Obtiene los resultados
            proveedores = cursor.fetchall()
            
            # Extrae solo los nombres de los clientes
            resultados = [{"id_proveedor":proveedor['ID_Proveedor'],"nombre": proveedor['Nombre'], "telefono": proveedor['Telefono'], "direccion": proveedor['Direccion']} for proveedor in proveedores]


            return jsonify(resultados)
    
    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()
    

if __name__ == '__main__':
    app.run(debug=True)

