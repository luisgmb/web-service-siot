from flask import Flask, request, jsonify
import json
import logging


from estufa_ar import *
from estufa_solo import *
from banco_de_dados import *

app = Flask(__name__)
logger = logging.getLogger(__name__)

class apiEstufaAr():
     
     @app.route("/estufa-ar/add", methods=["POST"])
     def postEstufaAr():
        registro = request.get_json()
        return jsonify(setRegistroEstufaAr(registro))

     @app.route("/estufa-ar", methods=["GET"])
     def getEstufasAr():
        return jsonify(getRegistrosEstufaAr())

     @app.route("/estufa-ar/<registro_pk>", methods=["GET"])
     def getEstufaAr(registro_pk):
        return jsonify(getRegistroEstufaAr(registro_pk))

class apiEstufaSolo():

     @app.route("/estufa-solo/add", methods=["POST"])
     def postEstufaSolo():
        logger.info("entra aqui 1")
        registro = request.get_json()
        return jsonify(setRegistroEstufaSolo(registro))

     @app.route("/estufa-solo", methods=["GET"])
     def getEstufasSolo():
        logger.info("entra aqui 2")
        return jsonify(getRegistrosEstufaSolo())

     @app.route("/estufa-solo/<registro_pk>", methods=["GET"])
     def getEstufaSolo(registro_pk):
        return jsonify(getRegistroEstufaSolo(registro_pk))

