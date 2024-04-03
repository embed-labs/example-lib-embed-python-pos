import os
import dotenv
import embed_lib as lib

STATUS_CODE = "resultado.status_code"

def configurar():
    dotenv.load_dotenv()

    PRODUTO = "pos"                                                     # produto de pagamento (atual pos)
    SUB_PRODUTO = os.getenv('SUB_PRODUTO')                              # fornecedor/banco/parceiro (atual 1)
    TOKEN = os.getenv('TOKEN')                                          # token de acesso
    USERNAME = os.getenv('USERNAME')                                    # fonecido pela integração
    PASSWORD = os.getenv('PASSWORD')                                    # fonecido pela integração
    POS_NUMERO_SERIAL_PADRAO = os.getenv('POS_NUMERO_SERIAL_PADRAO')    # fonecido pela integração

    input = f"{PRODUTO};{SUB_PRODUTO};{TOKEN};{USERNAME};{PASSWORD};{POS_NUMERO_SERIAL_PADRAO}"
    output = lib.configurar(input)
    print(f"configurar = {output}")

def iniciar():
    OPERACAO = "pos" # produto para processamento
    output = lib.iniciar(OPERACAO)
    print(f"iniciar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def debito(valor):
    OPERACAO = 'debito'     # operação para realizar pagamento em debito
    VALOR = valor           # valor do pagamento em centavos

    input = f"{OPERACAO};{VALOR}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def credito(valor, parcelas=1):
    OPERACAO = 'credito'     # operação para realizar pagamento em debito
    VALOR = valor            # valor do pagamento em centavos
    PARCELAS = parcelas      # quantidade de parcelas (1 a 99)

    input = f"{OPERACAO};{VALOR};{PARCELAS}"
    output = lib.processar(input)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def status():
    OPERACAO = 'get_status' # obtem o status do pagamento
    output = lib.processar(OPERACAO)
    print(f"processar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result

def finalizar():
    OPERACAO = '' # finaliza a API
    output = lib.finalizar(OPERACAO)
    print(f"finalizar = {output}")

    result = lib.obter_valor(output, STATUS_CODE)
    return result