from flask import Flask, request,jsonify

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

if __name__ == "__main__":
    app.run(debug=True)