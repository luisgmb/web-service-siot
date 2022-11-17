from flask import Flask, request, jsonify
import json

from estufa_ar import *
from estufa_solo import *
from banco_de_dados import *

app = Flask(__name__)

class apiEstufaAr():
     
     @app.route("/estufa-ar/add", methods=["POST"])
     def postEstufaAr():
          registro = request.get_json()
          return jsonify(setRegistroEstufaAr(registro))

     @app.route("/estufa-ar", methods=["GET"])
     def getEstufasAr():
          return jsonify(getRegistrosEstufaAr)

     @app.route("/estufa-ar/<registro_pk>", methods=["GET"])
     def getEstufaAr(registro_pk):
          return jsonify(getRegistroEstufaAr(registro_pk))

     @app.route("/estufa-ar/update", methods=["PUT"])
     def updateEstufaAr():
          registro = request.get_json()
          return jsonify(atualizaRegistroEstufaAr(registro))

     @app.route("/estufa-ar/delete/<registro_pk>", methods=["DELETE"])
     def deleteEstufaAr(registro_pk):
          return jsonify(removeRegistroEstufaAr(registro_pk))

class apiEstufaSolo():

     @app.route("/estufa-solo/add", methods=["POST"])
     def postEstufaSolo():
          registro = request.get_json()
          return jsonify(setRegistroEstufaSolo(registro))

     @app.route("/estufa-solo", methods=["GET"])
     def getEstufasSolo():
          return jsonify(getRegistrosEstufaSolo)

     @app.route("/estufa-solo/<registro_pk>", methods=["GET"])
     def getEstufaSolo(registro_pk):
          return jsonify(getRegistroEstufaSolo(registro_pk))

     @app.route("/estufa-solo/update", methods=["PUT"])
     def updateEstufaSolo():
          registro = request.get_json()
          return jsonify(atualizaRegistroEstufaSolo(registro))

     @app.route("/estufa-solo/delete/<registro_pk>", methods=["DELETE"])
     def deleteEstufaSolo(registro_pk):
          return jsonify(removeRegistroEstufaSolo(registro_pk))



