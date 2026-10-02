from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import pytz

app = FastAPI()

# Fuso horário de Brasília para garantir precisão no horário da eleição
fuso_br = pytz.timezone("America/Sao_Paulo")

@app.get("/api/eleicoes/velas")
def get_velas_api_eleicoes_velas_get(uf: Optional[str] = Query("BR")):
    agora = datetime.now(fuso_br)
    
    # Exemplo: Definindo o marco temporal da eleição (Domingo, 04/10/2026)
    # Você pode ajustar a data conforme o dia exato do pleito
    eleicao_encerrada = agora.hour >= 17 # Considera apuração após as 17h00
    
    # 1. LÓGICA DE SEGUNDO TURNO (Ativada se a apuração encerrou e queremos simular/verificar)
    # Aqui você pode colocar uma condição baseada em dados reais ou bandeira de controle
    houve_segundo_turno = False # Mude para True se quiser testar o cenário de 2º turno
    
    if houve_segundo_turno:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "SEGUNDO_TURNO_CONFIRMADO",
            "eleicao_encerrada": False,
            "eleicao": {
                "data_eleicao": "25/10/2026",
                "inicio_votacao": "08:00",
                "fim_votacao": "17:00"
            },
            "totalizacao": {
                "status_geral": "⚠️ SEGUNDO TURNO DEFINIDO - Disputa entre os 2 finalistas",
                "votos_computados": 1250000,
                "total_urnas_apuradas": "45.000 / 472.075"
            },
            "candidatos": [
                {
                    "posicao": 1,
                    "numero": 13,
                    "nome": "Candidato A",
                    "partido": "PT",
                    "percentual": 51.2,
                    "votos": "640.000 votos",
                    "status_texto": "EM DISPUTA (2º TURNO)",
                    "cor_vela": "#ef4444",
                    "cor_badge": "#F59E0B"
                },
                {
                    "posicao": 2,
                    "numero": 22,
                    "nome": "Candidato B",
                    "partido": "PL",
                    "percentual": 48.8,
                    "votos": "610.000 votos",
                    "status_texto": "EM DISPUTA (2º TURNO)",
                    "cor_vela": "#22c55e",
                    "cor_badge": "#F59E0B"
                }
            ]
        }

    # 2. LÓGICA DE APURAÇÃO EM ANDAMENTO OU ENCERRADA (1º Turno)
    status_geral_texto = "Apuração em Andamento" if eleicao_encerrada else "Votação em Andamento (Urnas Abertas)"
    
    return {
        "uf": uf.upper() if uf else "BR",
        "status_conexao": "CONECTADO_AUTOMATICO",
        "eleicao_encerrada": eleicao_encerrada,
        "eleicao": {
            "data_eleicao": agora.strftime("%d/%m/%Y"),
            "hora_consulta": agora.strftime("%H:%M:%S"),
            "fase": "Apuração" if eleicao_encerrada else "Votação"
        },
        "totalizacao": {
            "status_geral": status_geral_texto,
            "votos_computados": 850000 if eleicao_encerrada else 0,
            "total_urnas_apuradas": "150.200 / 472.075" if eleicao_encerrada else "0 / 472.075"
        },
        "candidatos": [
            {
                "posicao": 1,
                "numero": 12,
                "nome": "Candidato Líder",
                "partido": "PDT",
                "percentual": 42.5 if eleicao_encerrada else 0.0,
                "votos": "361.250 votos" if eleicao_encerrada else "0 votos",
                "status_texto": "1º LUGAR PARCIAL",
                "cor_vela": "#3b82f6",
                "cor_badge": "#10B981"
            },
            {
                "posicao": 2,
                "numero": 15,
                "nome": "Candidato Opositor",
                "partido": "MDB",
                "percentual": 38.1 if eleicao_encerrada else 0.0,
                "votos": "323.850 votos" if eleicao_encerrada else "0 votos",
                "status_texto": "2º LUGAR PARCIAL",
                "cor_vela": "#eab308",
                "cor_badge": "#3B82F6"
            }
        ]
    }
