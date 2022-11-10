from flask import Flask, request, jsonify
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is MEU MANINHO first API call!'

# ----------- POSTs -----------------------
@app.route('/estufa-ar', methods=["POST"])
def postEstufaAr():
     input_json = request.get_json(force=True)
     with open ("estufar_ar.json", "r+") as fileData:
        data = json.load(fileData)
        jsonString = json.dumps(input_json)
        data.update(jsonString)
        fileData.write(data)
     return jsonify(jsonString)

@app.route('/estufa-solo', methods=["POST"])
def postEstufaSolo():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)


# ----------- GETs -----------------------
@app.route('/estufa-ar', methods=["GET"])
def getEstufaAr():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)

@app.route('/estufa-solo', methods=["GET"])
def getEstufaSolo():
     input_json = request.get_json(force=True) 
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)