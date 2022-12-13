#!/usr/bin/python
import logging
import sqlite3

logger = logging.getLogger(__name__)


def conecta_banco():
    try:
        conn = sqlite3.connect("database.db")
        return conn
    except Exception as erro:
        logger.error(f"Ocorreu um erro ao conectar com o banco de dados, erro: {erro}")


def cria_tabelas():
    """
    Função gera as tabelas usadas para armazenar os dados da estufa de ar e da estufa de solo
    """
    try:
        conn = conecta_banco()
        conn.execute(
            """
            CREATE TABLE estufaAr (
                registro_pk INTEGER PRIMARY KEY AUTOINCREMENT,
                umidade_ar NOT NULL,
                direcao NOT NULL,
                pressao NOT NULL,
                velocidade_do_vento NOT NULL,
                temperatura_ar NOT NULL,
                luminosidade NOT NULL,
                data_registro NOT NULL
            );
        """
        )

        conn.execute(
            """
            CREATE TABLE estufaSolo (
                registro_pk INTEGER PRIMARY KEY AUTOINCREMENT,
                umidade_solo NOT NULL,
                temperatura_solo NOT NULL,
                status_bomba NOT NULL,
                data_registro NOT NULL
            );
        """
        )

        conn.commit()
        print("Tabelas criadas com sucesso")
        return True
    except Exception as erro:
        print(f"Falha na criação das tabelas: {erro}")
        return False
    finally:
        conn.close()

