from flask import Flask, jsonify, request
from pymysql import connect
from werkzeug.security import check_password_hash
import pymysql.cursors

# Configura la aplicación Flask
app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='leverna2003',
                                 db='INVENTORY_MANAGMENT',
                                 cursorclass=pymysql.cursors.DictCursor)



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # obtén los valores de 'email' y 'password' desde el cuerpo de la petición
    email = data.get('email')
    password = data.get('password')

    # crea una conexión a la base de datos
    connection.connect()
    # consulta los datos del empleado con el email dado
    with connection.cursor() as cursor:
        sql = "SELECT Email, Contrasena FROM Empleado WHERE Email = %s"
        cursor.execute(sql, (email,))
        empleado = cursor.fetchone()

    # si no se encontró un empleado con ese email, devuelve un error
    if not empleado:
        return jsonify({"error": "Invalid email or password"}), 401

    # si la contraseña proporcionada no coincide con la contraseña hash almacenada, devuelve un error
    if not check_password_hash(empleado['Contrasena'], password):
        return jsonify({"error": "Invalid email or password"}), 401

    # si el email y la contraseña son correctos, devuelve un token (esto es un ejemplo simple, en una aplicación real
    # el token debería ser generado de forma segura y codificar información relevante sobre el usuario)
    token = "some_token"

    return jsonify({"token": token}), 200



@app.route('/clientes', methods=['GET'])
def get_clientes():
    connection.connect()
    # Crea una conexión a la base de datos
    try:
        with connection.cursor() as cursor:
            # Consulta los nombres de los clientes
            sql = "SELECT Nombre FROM Cliente"
            cursor.execute(sql)
            
            # Obtiene los resultados
            clientes = cursor.fetchall()
            
            # Extrae solo los nombres de los clientes
            nombres = [cliente['Nombre'] for cliente in clientes]
            
            return jsonify(nombres)

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
    finally:
        connection.close()
    

if __name__ == '__main__':
    app.run(debug=True)

