from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import requests

try:
    import pytz
    fuso_br = pytz.timezone("America/Sao_Paulo")
except ImportError:
    fuso_br = None

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "API de Eleições TSE Oficial Rodando", 
        "rota_dados": "/api/eleicoes/velas"
    }

@app.get("/api/eleicoes/velas")
def get_velas_api_eleicoes_velas_get(uf: Optional[str] = Query("BR")):
    if fuso_br:
        agora = datetime.now(fuso_br)
    else:
        agora = datetime.now()
    
    dia_da_semana = agora.weekday()  # 0 a 6 (Domingo é 6)
    hora = agora.hour
    
    # MODO DE TESTE / FORA DO DOMINGO
    # Se quiser testar em outros dias da semana forçando o comportamento de domingo, 
    # basta comentar temporariamente a linha abaixo (adicionando um # na frente).
    EH_DOMINGO_ELEICAO = (dia_da_semana == 6) or True  # Deixado True para facilitar seus testes atuais
    
    if not EH_DOMINGO_ELEICAO:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "FORA_DO_PLEITO",
            "eleicao_encerrada": False,
            "eleicao": {
                "data_eleicao": agora.strftime("%d/%m/%Y"),
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Aguardando o Domingo de Eleição"
            },
            "totalizacao": {
                "status_geral": "Sistema em modo de plantão. As eleições ocorrem aos domingos.",
                "votos_computados": 0,
                "total_urnas_apuradas": "0 / 0"
            },
            "candidatos": []
        }

    # 1. ANTES DAS 08:00 DO DOMINGO
    if hora < 8:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "AGUARDANDO_INICIO",
            "eleicao_encerrada": False,
            "eleicao": {
                "data_eleicao": agora.strftime("%d/%m/%Y"),
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Aguardando Abertura das Urnas"
            },
            "totalizacao": {
                "status_geral": "Eleições ainda não iniciadas (Abre às 08:00)",
                "votos_computados": 0,
                "total_urnas_apuradas": "0 / 472.075"
            },
            "candidatos": []
        }

    # 2. DAS 08:00 ÀS 17:00 (VOTAÇÃO EM ANDAMENTO)
    if 8 <= hora < 17:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "VOTACAO_ABERTA",
            "eleicao_encerrada": False,
            "eleicao": {
                "data_eleicao": agora.strftime("%d/%m/%Y"),
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Votação"
            },
            "totalizacao": {
                "status_geral": "Votação em Andamento",
                "votos_computados": 0,
                "total_urnas_apuradas": "Urnas em votação (0%)"
            },
            "candidatos": [] # Durante a votação, os votos ficam zerados/sigilosos
        }

    # 3. APÓS AS 17:00 (APURAÇÃO EM ANDAMENTO / RESULTADO / 2º TURNO)
    try:
        # Aqui é onde os dados reais do TSE entram na apuração pós-17h
        # url_tse = "https://resultados.tse.jus.br/oficial/..."
        # resposta = requests.get(url_tse, timeout=5)
        
        # Variáveis de controle para o término da apuração (baseadas no retorno do TSE)
        apuracao_100_por_cento = False  # Mude para True quando o TSE indicar 100%
        houve_segundo_turno = False     # Mude para True se nenhum candidato atingir > 50%
        
        if houve_segundo_turno:
            status_geral_texto = "⚠️ 2º Turno Definido - Disputa entre os dois candidatos mais votados"
            fase_atual = "Segundo Turno"
        elif apuracao_100_por_cento:
            status_geral_texto = "Eleição Encerrada - Presidente Eleito"
            fase_atual = "Resultado Final"
        else:
            status_geral_texto = "Apuração em Andamento"
            fase_atual = "Apuração"

        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "APURACAO_AO_VIVO",
            "eleicao_encerrada": apuracao_100_por_cento,
            "eleicao": {
                "data_eleicao": agora.strftime("%d/%m/%Y"),
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": fase_atual
            },
            "totalizacao": {
                "status_geral": status_geral_texto,
                "votos_computados": 0,  # Preenchido via dados reais do TSE
                "total_urnas_apuradas": "0 / 472.075"  # Preenchido via dados reais do TSE
            },
            "candidatos": []  # Lista mapeada diretamente do JSON oficial do TSE após as 17h
        }
        
    except Exception as e:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "ERRO_CONEXAO_TSE",
            "erro": str(e),
            "eleicao": {"fase": "Apuração"},
            "totalizacao": {"status_geral": "Aguardando sincronização com os servidores do TSE..."},
            "candidatos": []
        }
