
from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime

try:
    import pytz
    fuso_br = pytz.timezone("America/Sao_Paulo")
except ImportError:
    fuso_br = None

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "API de Eleições TSE Rodando", 
        "rota_dados": "/api/eleicoes/velas"
    }

@app.get("/api/eleicoes/velas")
def get_velas_api_eleicoes_velas_get(uf: Optional[str] = Query("BR")):
    if fuso_br:
        agora = datetime.now(fuso_br)
    else:
        agora = datetime.now()
    
    # Validações de dia e horário (Domingo de Eleição simulado/real)
    # Exemplo: podemos validar se é domingo (weekday() == 6) ou forçar o ciclo para testes
    eh_domingo = agora.weekday() == 6 or True # Deixado True temporariamente para você testar, mas focado no horário
    hora = agora.hour
    minuto = agora.minute
    
    # Flags de controle de ciclo
    houve_segundo_turno = False  # Altere para True se houver 2º turno
    apuracao_concluida = False   # Altere para True quando fechar 100% das urnas

    # FASE 1: FORA DO HORÁRIO / ANTES DA ELEIÇÃO (< 08:00)
    if hora < 8:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "AGUARDANDO_INICIO",
            "eleicao_encerrada": False,
            "eleicao": {
                "data_eleicao": agora.strftime("%d/%m/%Y"),
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Aguardando Início da Votação"
            },
            "totalizacao": {
                "status_geral": "Eleições ainda não iniciadas (Abre às 08:00)",
                "votos_computados": 0,
                "total_urnas_apuradas": "0 / 472.075"
            },
            "candidatos": [
                {"posicao": 1, "numero": 12, "nome": "Candidato Líder", "partido": "PDT", "percentual": 0.0, "votos": "0 votos", "status_texto": "AGUARDANDO", "cor_vela": "#3b82f6", "cor_badge": "#10B981"},
                {"posicao": 2, "numero": 15, "nome": "Candidato Opositor", "partido": "MDB", "percentual": 0.0, "votos": "0 votos", "status_texto": "AGUARDANDO", "cor_vela": "#eab308", "cor_badge": "#3B82F6"}
            ]
        }

    # FASE 2: SEGUNDO TURNO (Se aplicável)
    if houve_segundo_turno:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "SEGUNDO_TURNO_CONFIRMADO",
            "eleicao_encerrada": False,
            "eleicao": {"data_eleicao": agora.strftime("%d/%m/%Y"), "fase": "2º Turno"},
            "totalizacao": {
                "status_geral": "⚠️ SEGUNDO TURNO DEFINIDO - Disputa entre os 2 finalistas",
                "votos_computados": 1250000,
                "total_urnas_apuradas": "45.000 / 472.075"
            },
            "candidatos": [
                {"posicao": 1, "numero": 13, "nome": "Candidato A", "partido": "PT", "percentual": 51.2, "votos": "640.000 votos", "status_texto": "EM DISPUTA (2º TURNO)", "cor_vela": "#ef4444", "cor_badge": "#F59E0B"},
                {"posicao": 2, "numero": 22, "nome": "Candidato B", "partido": "PL", "percentual": 48.8, "votos": "610.000 votos", "status_texto": "EM DISPUTA (2º TURNO)", "cor_vela": "#22c55e", "cor_badge": "#F59E0B"}
            ]
        }

    # FASE 3: VOTAÇÃO EM ANDAMENTO (Das 08:00 às 17:00)
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
                "status_geral": "Votação em Andamento (Urnas Abertas)",
                "votos_computados": 0,
                "total_urnas_apuradas": "0 / 472.075"
            },
            "candidatos": [
                {"posicao": 1, "numero": 12, "nome": "Candidato Líder", "partido": "PDT", "percentual": 0.0, "votos": "0 votos", "status_texto": "URNAS ABERTAS", "cor_vela": "#3b82f6", "cor_badge": "#10B981"},
                {"posicao": 2, "numero": 15, "nome": "Candidato Opositor", "partido": "MDB", "percentual": 0.0, "votos": "0 votos", "status_texto": "URNAS ABERTAS", "cor_vela": "#eab308", "cor_badge": "#3B82F6"}
            ]
        }

    # FASE 4: APURAÇÃO EM ANDAMENTO (Após as 17:00)
    # Aqui é onde os dados reais do TSE começam a entrar na contagem
    status_geral_texto = "Eleição Encerrada - Presidente Eleito" if apuracao_concluida else "Apuração em Andamento"
    
    return {
        "uf": uf.upper() if uf else "BR",
        "status_conexao": "APURACAO_AO_VIVO",
        "eleicao_encerrada": True,
        "eleicao": {
            "data_eleicao": agora.strftime("%d/%m/%Y"),
            "hora_consulta": agora.strftime("%H:%M:%S"),
            "fase": "Apuração"
        },
        "totalizacao": {
            "status_geral": status_geral_texto,
            "votos_computados": 45000000,
            "total_urnas_apuradas": "472.075 / 472.075 (100%)" if apuracao_concluida else "350.200 / 472.075"
        },
        "candidatos": [
            {
                "posicao": 1,
                "numero": 12,
                "nome": "Candidato Líder",
                "partido": "PDT",
                "percentual": 52.4,
                "votos": "23.580.000 votos",
                "status_texto": "PRESIDENTE ELEITO" if apuracao_concluida else "1º LUGAR PARCIAL",
                "cor_vela": "#3b82f6",
                "cor_badge": "#10B981"
            },
            {
                "posicao": 2,
                "numero": 15,
                "nome": "Candidato Opositor",
                "partido": "MDB",
                "percentual": 47.6,
                "votos": "21.420.000 votos",
                "status_texto": "2º LUGAR",
                "cor_vela": "#eab308",
                "cor_badge": "#3B82F6"
            }
        ]
    }
