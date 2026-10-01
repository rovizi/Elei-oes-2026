import requests
from datetime import datetime
from config import TSE_URL_OFICIAL, ANO_ELEICAO, CORES_VELAS

def buscar_dados_completos(uf: str = "br"):
    """
    Controla a fonte de dados com base no momento:
    - Antes do domingo / antes das 17h: Puxa o cenário de pesquisas registradas.
    - Domingo a partir das 17h: Puxa a apuração real direto das urnas do TSE.
    """
    # Verifica se já estamos no domingo de eleição após as 17h (Horário aproximado de início da apuração)
    # Ajuste a data/lógica conforme o dia exato do pleito
    agora = datetime.now()
    e_horario_de_apuracao = (agora.weekday() == 6 and agora.hour >= 17) # Domingo = 6

    if e_horario_de_apuracao:
        # Tenta buscar dados reais do TSE
        url = f"{TSE_URL_OFICIAL}/ele{ANO_ELEICAO}/air/uf/{uf.lower()}/br-c0001-e.json"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados_tse = response.json()
                # Aqui você processa os dados reais do TSE
                return processar_dados_tse(dados_tse)
        except Exception:
            pass

    # Se ainda não for o horário de apuração (ou se o TSE estiver offline), 
    # entrega os dados consolidados de PESQUISAS ELEITORAIS com fotos e cores.
    return obter_dados_pesquisas_atuais()

def processar_dados_tse(dados_brutos):
    """Processa o retorno real das urnas no domingo."""
    # Retorno estruturado com base na apuração real do TSE
    return dados_brutos

def obter_dados_pesquisas_atuais():
    """Retorna o painel baseado nas pesquisas eleitorais atuais (com fotos e partidos)."""
    return {
        "fonte_dados": "Pesquisas Eleitorais Oficializadas",
        "eleicao_encerrada": False,
        "percentual_apurado": 0.0,
        "candidatos": [
            {
                "posicao": 1,
                "nome": "Candidato A",
                "partido": "PTQ",
                "votos_ou_media": "42% (Pesquisa)",
                "percentual": 42.0,
                "status_texto": "Liderando Pesquisas",
                "cor_vela": CORES_VELAS["lider"],
                "eleito": False,
                "foto_url": "https://via.placeholder.com/150"
            },
            {
                "posicao": 2,
                "nome": "Candidato B",
                "partido": "BLD",
                "votos_ou_media": "38% (Pesquisa)",
                "percentual": 38.0,
                "status_texto": "Na Disputa",
                "cor_vela": CORES_VELAS["segundo"],
                "eleito": False,
                "foto_url": "https://via.placeholder.com/150"
            }
        ]
    }