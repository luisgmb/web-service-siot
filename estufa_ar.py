import datetime
import logging
import sqlite3
from banco_de_dados import conecta_banco

logger = logging.getLogger(__name__)


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
        direcao = registro.get("direcao", None)
        pressao = registro.get("pressao", None)
        velocidade_do_vento = registro.get("velocidade_do_vento", None)
        temperatura_ar = registro.get("temperatura_ar", None)
        data_registro = datetime.now()
        cursor.execute(
            "INSERT INTO estufaAr (humidade_ar, direcao, pressao, velocidade_do_vento, temperatura_ar, data_registro)"
            f" VALUES ({humidade_ar}, {direcao}, {pressao}, {velocidade_do_vento}, {temperatura_ar}, {data_registro})"
        )
        conn.commit()
        registro = getRegistroEstufaAr(cursor.lastrowid)
    except:
        conn().rollback()

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
        cursor.execute("SELECT * FROM estufaAr")
        dados = cursor.fetchall()

        for dado in dados:
            registro = {
                "registro_pk": dado.get("registro_pk", None),
                "humidade_ar": dado.get("humidade_ar", None),
                "direcao": dado.get("direcao", None),
                "pressao": dado.get("pressao", None),
                "velocidade_do_vento": dado.get("velocidade_do_vento", None),
                "temperatura_ar": dado.get("temperatura_ar", None),
                "data_registro": dado.get("data_registro", None),
            }
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
        cursor.execute(f"SELECT * FROM estufaAr WHERE registro_pk = {registro_pk}")

        dado = cursor.fetchone()

        registro = {
            "registro_pk": dado.get("registro_pk", None),
            "humidade_ar": dado.get("humidade_ar", None),
            "direcao": dado.get("direcao", None),
            "pressao": dado.get("pressao", None),
            "velocidade_do_vento": dado.get("velocidade_do_vento", None),
            "temperatura_ar": dado.get("temperatura_ar", None),
            "data_registro": dado.get("data_registro", None),
        }

    except Exception as erro:
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro


def atualizaRegistroEstufaAr(registro: dict, registro_pk: int):
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

        humidade_ar = registro.get("humidade_ar", None)
        direcao = registro.get("direcao", None)
        pressao = registro.get("pressao", None)
        velocidade_do_vento = registro.get("velocidade_do_vento", None)
        temperatura_ar = registro.get("temperatura_ar", None)
        data_registro = datetime.now()

        cursor.execute(
            f"SELECT estufaAr SET humidade_ar = {humidade_ar}, direcao = {direcao}, pressao={pressao},"
            f" velocidade_do_vento = {velocidade_do_vento}, temperatura_ar ={temperatura_ar},"
            f" data_registro={data_registro} WHERE registro_pk={registro_pk}"
        )

        conn.commit()
        registro = getRegistroEstufaAr(registro_pk)

    except Exception as erro:
        conn.rollback()
        logger.error(f"Houver um erro ao consultar o registro {registro_pk}, erro: {erro}")
        registro = {}

    finally:
        conn.close()

    return registro


def removeRegistroEstufaAr(registro_pk: int):
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
        conn.execute(f"DELETE from estufaAr WHERE registro_pk={registro_pk}")
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
