import logging
import sqlite3
from datetime import datetime

from banco_de_dados import conecta_banco

logger = logging.getLogger(__name__)

def formata_retorno_consulta(dado):
    dados = {
        "registro_pk": dado[0],
        "humidade_ar": dado[1],
        "direcao": dado[2],
        "pressao": dado[3],
        "velocidade_vento": dado[4],  
        "temperatura_ar": dado[5],  
        "luminosidade": dado[6],  
        "data_registro": dado[7],  
    }

    return dados


def setRegistroEstufaAr(registro: dict = None):
    """_summary_

    Args:
        registro (dict): contem registro a ser armazenado.

    Returns:
        dict: Retorna objeto salvo no banco de dados.
    """

    try:
        conn = conecta_banco()
        cursor = conn.cursor()
        humidade_ar = registro.get("humidade_ar", None)
        direcao_ar = registro.get("direcao", None)
        print(f'Direcao = {direcao_ar}')
        pressao = registro.get("pressao", None)
        velocidade_do_vento = registro.get("velocidade_do_vento", None)
        temperatura_ar = registro.get("temperatura_ar", None)
        luminosidade = registro.get("luminosidade", None)
        data_registro = datetime.now()
        cursor.execute(
            "INSERT INTO estufaAr (humidade_ar, direcao, pressao, velocidade_do_vento, temperatura_ar, luminosidade, data_registro)"
            f" VALUES ({humidade_ar}, '{direcao_ar}', {pressao}, {velocidade_do_vento}, {temperatura_ar}, {luminosidade}, '{data_registro}')"
        )
        conn.commit()
        registro = getRegistroEstufaAr(cursor.lastrowid)
    except Exception as erro:
        logger.error(f"erro = {erro}")
        conn.rollback()

    finally:
        conn.close()

    return registro


def getRegistrosEstufaAr():
    """_summary_

    Returns:
        list: Uma lista de dicionarios contendo os dados sobre a estufaAr consultados no banco de dados
    """
    registros = []

    try:
        conn = conecta_banco()
        cursor = conn.cursor()
        exec = cursor.execute("SELECT * FROM estufaAr")
        dados = exec.fetchall()
        for dado in dados:
            registro = formata_retorno_consulta(dado)
            registros.append(registro)

    except Exception as erro:
        logger.error(f"Houver um erro ao consultar os registros, erro: {erro}")
        registros = []

    finally:
        conn.close()

    return registros


def getRegistroEstufaAr(registro_pk: int):
    """_summary_

    Args:
        registro_pk (int): ID do registro que deve ser consultado

    Returns:
        Dict: Registro consultado
    """

    try:
        if not registro_pk:
            raise Exception("É necessário informar o id do registro")

        conn = conecta_banco()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        exec = cursor.execute(f"SELECT * FROM estufaAr WHERE registro_pk = {registro_pk}")

        dado = exec.fetchone()

        registro = formata_retorno_consulta(dado)


    except Exception as erro:
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro