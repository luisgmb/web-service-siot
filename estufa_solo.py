import datetime
import logging
import sqlite3
from banco_de_dados import conecta_banco

logger = logging.getLogger(__name__)


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
        data_registro = datetime.now()
        cursor.execute(
            "INSERT INTO estufaSolo (humidade_solo, temperatura_solo, data_registro)"
            f" VALUES ({humidade_solo}, {temperatura_solo}, {data_registro})"
        )
        conn.commit()
        registro = getRegistroEstufaSolo(cursor.lastrowid)
    except:
        conn().rollback()

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
        cursor.execute("SELECT * FROM estufaSolo")
        dados = cursor.fetchall()

        for dado in dados:
            registro = {
                "registro_pk": dado.get("registro_pk", None),
                "humidade_solo": dado.get("humidade_solo", None),
                "temperatura_solo": dado.get("temperatura_solo", None),
                "data_registro": dado.get("data_registro", None),
            }
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
        cursor.execute(f"SELECT * FROM estufaSolo WHERE registro_pk = {registro_pk}")

        dado = cursor.fetchone()

        registro = {
            "registro_pk": dado.get("registro_pk", None),
            "humidade_solo": dado.get("humidade_solo", None),
            "temperatura_solo": dado.get("temperatura_solo", None),
            "data_registro": dado.get("data_registro", None),
        }

    except Exception as erro:
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro


def atualizaRegistroEstufaSolo(registro: dict, registro_pk: int):
    """_summary_

    Args:
        registro (dict): dados a serem atualizados
        registro_pk (int): ID do registro a ser atualizado

    Returns:
        dict: registro atualizado
    """
    try:
        conn = conecta_banco()
        cursor = conn.cursor()

        if not registro_pk:
            raise Exception("É necessário informar o id do registro")

        humidade_solo = registro.get("humidade_solo", None)
        temperatura_solo = registro.get("temperatura_solo", None)
        data_registro = datetime.now()

        cursor.execute(
            f"SELECT estufaSolo SET humidade_solo = {humidade_solo}, temperatura_solo ={temperatura_solo},"
            f" data_registro={data_registro} WHERE registro_pk={registro_pk}"
        )

        conn.commit()
        registro = getRegistroEstufaSolo(registro_pk)

    except Exception as erro:
        conn.rollback()
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro


def removeRegistroEstufaSolo(registro_pk: int):
    """_summary_

    Args:
        registro_pk (int): ID do registro a ser removido

    Returns:
        tupla:
            status (boolean): Status da remoção
            mensagem (string): Mensagem informando resultado da remoção
    """
    try:
        conn = conecta_banco()
        conn.execute(f"DELETE from estufaSolo WHERE registro_pk={registro_pk}")
        conn.commit()
        mensagem = f"Registro removido {registro_pk} com sucesso"
        logger.info(mensagem)
        status = True, mensagem

    except Exception as erro:
        conn.rollback()
        mensagem = f"Ocorreu um erro ao remover o registro {registro_pk}, erro: {erro}"

        logger.error(mensagem)
        status = False, mensagem

    finally:
        conn.close()

    return status
