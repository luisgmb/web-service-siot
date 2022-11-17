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
        conn = connect_to_db()
        conn.execute(
            """
            CREATE TABLE estufaAr (
                registro_pk INTEGER PRIMARY KEY NOT NULL,
                humidade_ar DECIMAL NOT NULL,
                direcao TEXT NOT NULL,
                pressao DECIMAL NOT NULL,
                velocidade_do_vento DECIMAL NOT NULL,
                temperatura_ar DECIMAL NOT NULL,
                data_registro DATETIME NOT NULL
            );
        """
        )

        conn.execute(
            """
            CREATE TABLE estufaSolo (
                registro_pk INTEGER PRIMARY KEY NOT NULL,
                humidade_solo DECIMAL NOT NULL,
                temperatura_solo DECIMAL NOT NULL,
                data_registro DATETIME NOT NULL
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
