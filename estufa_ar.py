from datetime import datetime
import logging
import sqlite3
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
        direcao = registro.get("direcao", None)
        pressao = registro.get("pressao", None)
        velocidade_do_vento = registro.get("velocidade_do_vento", None)
        temperatura_ar = registro.get("temperatura_ar", None)
        luminosidade = registro.get("luminosidade", None)
        data_registro = datetime.now()
        cursor.execute(
            "INSERT INTO estufaAr (humidade_ar, direcao, pressao, velocidade_do_vento, temperatura_ar, luminosidade, data_registro)"
            f" VALUES ({humidade_ar}, {direcao}, {pressao}, {velocidade_do_vento}, {temperatura_ar}, {luminosidade}, {data_registro})"
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

        if not registro_pk:
            raise Exception("É necessário informar o id do registro")

        humidade_solo = registro.get("humidade_solo", None)
        temperatura_solo = registro.get("temperatura_solo", None)
        data_registro = datetime.now()

        cursor.execute(
            f"SELECT estufaAr SET humidade_solo = {humidade_solo}, temperatura_solo ={temperatura_solo},"
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
