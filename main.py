from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/api/eleicoes/velas")
def obter_velas(uf: str = "br"):
    agora = datetime.now()
    
    # 1. Período de zeramento antes de abrir o 2º turno (madrugada de 24 para 25 de out de 2026)
    data_zeramento = datetime(2026, 10, 25, 0, 0, 0)
    data_segundo_turno = datetime(2026, 10, 25, 8, 0, 0)
    
    if agora >= data_zeramento and agora < data_segundo_turno:
        return {
            "uf": uf.upper(),
            "status_conexao": "AGUARDANDO_DADOS_SEGUNDO_TURNO",
            "eleicao_encerrada": False,
            "etapa_eleitoral": "Segundo Turno",
            "eleicao": {
                "data_segundo_turno": "25/10/2026",
                "horario_votacao": "08:00 às 17:00",
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Aguardando Início da Votação do 2º Turno"
            },
            "totalizacao": {
                "status_geral": "Aguardando dados oficiais. Votação hoje, das 8h às 17h.",
                "votos_computados": 0,
                "votos_brancos": 0,
                "votos_nulos": 0,
                "total_urnas_apuradas": "0 / 0"
            },
            "candidatos": []
        }

    # 2. Simulação de encerramento do 2º turno (ativado após 100% das urnas no dia 25/10/2026 após as 19:00)
    data_fim_eleicao = datetime(2026, 10, 25, 19, 0, 0)
    
    if agora >= data_fim_eleicao:
        return {
            "uf": uf.upper(),
            "status_conexao": "ELEICAO_ENCERRADA",
            "eleicao_encerrada": True,
            "etapa_eleitoral": "Segundo Turno - Finalizado",
            "eleicao": {
                "data_segundo_turno": "25/10/2026",
                "horario_votacao": "08:00 às 17:00",
                "hora_consulta": agora.strftime("%H:%M:%S"),
                "fase": "Eleição Encerrada - 100% Apurado"
            },
            "totalizacao": {
                "status_geral": "Eleição encerrada. 100% das urnas apuradas. Resultado oficial consolidado.",
                "votos_computados": 120000000,
                "votos_brancos": 2000000,
                "votos_nulos": 1500000,
                "total_urnas_apuradas": "100% / 100%"
            },
            "candidatos": [
                {
                    "nome": "Candidato Vencedor",
                    "partido": "PARTIDO",
                    "numero": 00,
                    "logo_partido": "",
                    "votos_validos": 61000000,
                    "porcentagem": 52.5,
                    "situacao": "ELEITO(A)"
                }
            ]
        }

    # 3. Cenário Padrão (Consolidado do 1º Turno com as Logos dos Partidos)
    return {
        "uf": uf.upper(),
        "status_conexao": "APURACAO_1_TURNO_CONCLUIDA",
        "eleicao_encerrada": False,
        "etapa_eleitoral": "Segundo Turno",
        "eleicao": {
            "data_primeiro_turno": "04/10/2026",
            "data_segundo_turno": "25/10/2026",
            "horario_votacao": "08:00 às 17:00",
            "hora_consulta": agora.strftime("%H:%M:%S"),
            "fase": "1º Turno Encerrado - 100% Apurado - 2º Turno Agendado"
        },
        "totalizacao": {
            "status_geral": "100% das urnas apuradas. Segundo turno confirmado para 25/10/2026.",
            "aviso_apuracao": "Atenção: Votação do 2º turno das 8h às 17h. Apuração sujeita a atrasos por filas.",
            "votos_computados": 118500000,
            "votos_brancos": 2100000,
            "votos_nulos": 1400000,
            "total_urnas_apuradas": "100% / 100%"
        },
        "candidatos": [
            {
                "nome": "Flávio Bolsonaro",
                "partido": "PL",
                "numero": 22,
                "logo_partido": "https://i.postimg.cc/q7C3GKf9/PL0.png",
                "votos_validos": 51200000,
                "porcentagem": 48.1,
                "situacao": "CLASSIFICADO PARA O 2º TURNO"
            },
            {
                "nome": "Lula",
                "partido": "PT",
                "numero": 13,
                "logo_partido": "https://i.postimg.cc/KvRvL2hs/PT-(1).png",
                "votos_validos": 46800000,
                "porcentagem": 43.9,
                "situacao": "CLASSIFICADO PARA O 2º TURNO"
            }
        ]
    }
