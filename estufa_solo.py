import logging
import sqlite3
from datetime import datetime

from banco_de_dados import conecta_banco

logger = logging.getLogger(__name__)

def formata_retorno_consulta(dado):
    dados = {
        "registro_pk": dado[0],
        "humidade_solo": dado[1],
        "temperatura_solo": dado[2],
        "status_bomba": dado[3],
        "data_registro": dado[4],  
    }

    return dados


def setRegistroEstufaSolo(registro: dict = None):
    """_summary_

    Args:
        registro (dict): contem registro a ser armazenado.

    Returns:
        dict: Retorna objeto salvo no banco de dados.
    """

    try:
        conn = conecta_banco()
        cursor = conn.cursor()
        humidade_solo = registro.get("humidade_solo", None)
        temperatura_solo = registro.get("temperatura_solo", None)
        status_bomba = registro.get("status_bomba", False)
        data_registro = datetime.now()
        cursor.execute(
            f"""INSERT INTO estufaSolo (humidade_solo, temperatura_solo, status_bomba,  data_registro) VALUES ({humidade_solo}, {temperatura_solo}, {status_bomba} ,'{data_registro}');"""
        )
        conn.commit()
        registro = getRegistroEstufaSolo(cursor.lastrowid)
    except Exception as erro:
        logger.error(f"erro = {erro}")
        conn.rollback()

    finally:
        conn.close()

    return registro


def getRegistrosEstufaSolo():
    """_summary_

    Returns:
        list: Uma lista de dicionarios contendo os dados sobre a estufaSolo consultados no banco de dados
    """
    registros = []

    try:
        conn = conecta_banco()
        cursor = conn.cursor()
        exec = cursor.execute("SELECT * FROM estufaSolo")
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


def getRegistroEstufaSolo(registro_pk: int):
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
        exec = cursor.execute(f"SELECT * FROM estufaSolo WHERE registro_pk = {registro_pk}")

        dado = exec.fetchone()

        registro = formata_retorno_consulta(dado)


    except Exception as erro:
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro
