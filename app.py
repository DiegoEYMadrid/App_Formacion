from flask import Flask, request,jsonify
from azure.data.tables import TableServiceClient
from config import Config

app = Flask(__name__)

@app.route("/", methods=['GET'],defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    # print(request.json("docId"))
    return app.send_static_file(path)

@app.route("/test" , methods=['POST'])
def token():
    # print(request.json("docId"))
    return "TEST OK"

@app.route("/getuser" , methods=['GET'])
def getuser():
    user = request.args.get('nombre')
    print(Config.AZURE_STORAGE_USER_TABLE)
    table_service_client = TableServiceClient.from_connection_string(conn_str=Config.AZURE_STORAGE_KEY)
    table_client = table_service_client.get_table_client(table_name=Config.AZURE_STORAGE_USER_TABLE)
    parameters = {"nombre": user}
    name_filter = "nombre eq @nombre"
    print("===parameters=====")
    print(parameters)
    print("====name_filter====")
    print(name_filter)
    queried_entities = table_client.query_entities(
        query_filter=name_filter, select=["nombre"], parameters=parameters
    )
    for entity_chosen in queried_entities:
        print(entity_chosen)
        return entity_chosen
    return "No se ha encontrado al usuario"

@app.route("/insertuser" , methods=['post'])
def insertuser():
    nombre = request.json.get("nombre")
    my_entity = {
                u'PartitionKey':nombre,
                u'RowKey': nombre,
                u'nombre':nombre
            }
    table_service_client = TableServiceClient.from_connection_string(conn_str=Config.AZURE_STORAGE_KEY)
    table_client = table_service_client.get_table_client(table_name=Config.AZURE_STORAGE_USER_TABLE)
    print("Conexion Hecha")
    entity = table_client.create_entity(entity=my_entity)
    return "Usuario Creado"
if __name__ == "__main__":
    app.run(debug=True)
