import psycopg2
import json
import logging

def validar_utf8(data):
    """
    Valida se os dados estão em UTF-8.

    Args:
        data: Dados a serem validados.

    Returns:
        True se os dados estão em UTF-8, False caso contrário.
    """
    try:
        if isinstance(data, str):
            data.encode('utf-8')
        elif isinstance(data, dict):
            json.dumps(data, ensure_ascii=False).encode('utf-8')
        return True
    except UnicodeEncodeError:
        return False

def force_utf8_encoding(data):
    """
    Força a codificação dos dados para UTF-8.

    Args:
        data: Dados a serem codificados.

    Returns:
        Os dados codificados em UTF-8.
    """
    if isinstance(data, str):
        try:
            return data.encode("utf-8").decode("utf-8")
        except UnicodeDecodeError as e:
            logging.error("Erro ao forçar codificação UTF-8. Valor: '%s'. Detalhes: %s", data, e)
            raise
    return data

def update_participante_data(conn, cnpj, data):
    try:
        logging.info("Preparando dados para atualização do participante com CNPJ: %s", cnpj)
        logging.debug("Dados recebidos para atualização: %s", data)

        # Forçar codificação UTF-8 para cada campo antes de executar a query
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = force_utf8_encoding(value)

        logging.debug("Todos os campos foram convertidos para UTF-8.")

        cursor = conn.cursor()
        logging.debug("Cursor do banco de dados criado com sucesso.")

        update_query = """
            UPDATE participantes SET
                razao_social = %s,
                situacao_cadastral = %s,
                porte_empresa = %s,
                capital_social = %s,
                cnaes = %s,
                endereco = %s
            WHERE cnpj_cpf = %s;
        """

        razao_social = data.get("razao_social")
        situacao_cadastral = data.get("situacao")
        porte_empresa = data.get("porte")
        capital_social = data.get("capital_social")
        cnaes = json.dumps(data.get("cnaes", []))
        endereco = json.dumps(data.get("endereco", {}))

        # Validação de UTF-8 para todos os campos
        if not validar_utf8(razao_social):
            logging.error("Dados de razão social não estão em UTF-8.")
            raise ValueError("Dados inválidos para razão social.")
        if not validar_utf8(situacao_cadastral):
            logging.error("Dados de situação cadastral não estão em UTF-8.")
            raise ValueError("Dados inválidos para situação cadastral.")
        if not validar_utf8(porte_empresa):
            logging.error("Dados de porte da empresa não estão em UTF-8.")
            raise ValueError("Dados inválidos para porte da empresa.")
        if not validar_utf8(capital_social):
            logging.error("Dados de capital social não estão em UTF-8.")
            raise ValueError("Dados inválidos para capital social.")
        if not validar_utf8(cnaes):
            logging.error("Dados de CNAEs não estão em UTF-8.")
            raise ValueError("Dados inválidos para CNAEs.")
        if not validar_utf8(endereco):
            logging.error("Dados de endereço não estão em UTF-8.")
            raise ValueError("Dados inválidos para endereço.")

        update_values = (
            razao_social,
            situacao_cadastral,
            porte_empresa,
            capital_social,
            cnaes,
            endereco,
            cnpj
        )

        logging.debug("Executando query de atualização com os valores: %s", update_values)
        cursor.execute(update_query, update_values)
        conn.commit()
        logging.info("Dados atualizados com sucesso para o CNPJ: %s", cnpj)
    except Exception as e:
        logging.error("Erro ao atualizar dados do participante com CNPJ: %s. Erro: %s", cnpj, str(e))
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
            logging.debug("Cursor do banco de dados fechado.")

def update_participante_contato(conn, cnpj, contato):
    """
    Atualiza as informações de contato de um participante na tabela `participantes`.

    Args:
        conn: Conexão com o banco de dados.
        cnpj: O CNPJ do participante.
        contato: Dados de contato a serem atualizados.

    Returns:
        O número de linhas afetadas pela atualização.
    """
    cursor = conn.cursor()
    try:
        logging.info("Preparando dados de contato para atualização do participante com CNPJ: %s", cnpj)
        logging.debug("Dados de contato preparados: %s", contato)

        update_query = """
            UPDATE participantes SET
                whatsapp = %s,
                redes_sociais = %s
            WHERE cnpj_cpf = %s;
        """

        cursor.execute(update_query, (
            contato.get("whatsapp"),
            json.dumps(contato.get("redes_sociais", {})) if contato.get("redes_sociais") else None,
            cnpj
        ))

        rows_affected = cursor.rowcount
        conn.commit()
        logging.info("Dados de contato atualizados com sucesso para o CNPJ: %s", cnpj)
    except Exception as e:
        logging.error("Erro ao atualizar dados de contato do participante com CNPJ: %s. Erro: %s", cnpj, str(e))
        raise
    finally:
        cursor.close()