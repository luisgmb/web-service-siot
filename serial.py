import logging
from time import sleep

import requests
import RPi.GPIO as GPIO

import serial

logger = logging.getLogger(__name__)

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)

count = 1
comunica_solo = bytearray.fromhex("1C 03 01 21 05")
comunica_ar = bytearray.fromhex("1C 02 01 21 05")


def faz_requisicao(dados, url):
    resposta = requests.post(url=url, json=dados)
    if resposta.status_code == 200:
        logger.info("Requisição realizada com sucesso")
    else:
        logger.error(f"Erro ao realizar a requisição {resposta}")


def leitura_dados_sensores(sensor):
    dados = {}
    GPIO.output(12, GPIO.LOW)
    dados_sensor = ser.read(1)
    if dados_sensor:
        dados_sensor += ser.read_until(b"\x05")
        if sensor == comunica_solo:
            dados.update(
                {
                    "temperatura_ar": dados_sensor[4],
                    "pressao": dados_sensor[5],
                    "umidade_ar": dados_sensor[6],
                    "direcao": dados_sensor[7],
                    "velocidade_do_vento": dados_sensor[8],
                    "luminosidade": dados_sensor[9],
                }
            )
            faz_requisicao(dados, "http://127.0.0.1:5000/estufa-solo/add")
        else:
            dados.update(
                {
                    "temperatura_solo": dados_sensor[4],
                    "umidade_solo": dados_sensor[5],
                    "status_bomba": dados_sensor[6],
                }
            )
            faz_requisicao(dados, "http://127.0.0.1:5000/estufa-ar/add")


def informa_sensor(sensor):
    GPIO.output(12, GPIO.HIGH)
    ser.write(sensor)
    sleep(1)
    leitura_dados_sensores(sensor)


with serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
) as ser:
    ser.flushOutput()
    ser.flushInput()

    i = 0
    while count != None:
        if count == 1:
            informa_sensor(comunica_ar)
        else:
            informa_sensor(comunica_solo)
