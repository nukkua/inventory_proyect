from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymysql import connect
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql.cursors

# Configura la aplicación Flask
app = Flask(__name__)


# JWT TOKENIZER
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'ultrasecret'

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='leverna2003',
                                 db='INVENTORY_MANAGMENT',
                                 cursorclass=pymysql.cursors.DictCursor)

# End Point con verificacion jwt, para crear empleados
@app.route('/create_empleado', methods=['POST'])
@jwt_required()
def create_user():
    identity = get_jwt_identity()
    if identity['role']!= 'admin':
        return jsonify({"error": "Unauthorized"}),403

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

# Endpoint LOGIN
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

#EndPoint MenuDelDia
@app.route('/menudeldia', methods=['GET'])
def get_menu():
    connection.connect()
    try: 
        with connection.cursor() as cursor:
            sql = "SELECT * FROM MENU_DEL_DIA_PLATO_V"
            cursor.execute(sql)
            
            platos = cursor.fetchall()
            return jsonify(platos)
    
    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()




#Endpoints referidos a empleados
@app.route('/empleados', methods=['GET'])
def get_empleados():
    connection.connect()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT ID_Empleado, Nombre, Usuario, Contrasena, Rol FROM Empleado"
            cursor.execute(sql)
            empleados = cursor.fetchall()

            resultados = [{"id_empleado":empleado['ID_Empleado'],"nombre": empleado['Nombre'], "usuario": empleado['Usuario'], "contrasena": empleado['Contrasena'], "rol": empleado['Rol']} for empleado in empleados]
            return jsonify(resultados)

    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()




# Endpoints referidos a proveedores
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
            
            resultados = [{"id_proveedor":proveedor['ID_Proveedor'],"nombre": proveedor['Nombre'], "telefono": proveedor['Telefono'], "direccion": proveedor['Direccion']} for proveedor in proveedores]


            return jsonify(resultados)
    
    except pymysql.Error as e:
        return jsonify({"error": "Database error: {}".format(e)}), 500

    finally:
        connection.close()
    

if __name__ == '__main__':
    app.run(debug=True)






