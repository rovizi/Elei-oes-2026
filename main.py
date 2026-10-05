from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/api/eleicoes/velas")
def obter_velas(uf: str = "br"):
    agora = datetime.now()
    
    # Define o zeramento exato à meia-noite da virada do dia 24 para o dia 25 de outubro de 2026
    data_zeramento = datetime(2026, 10, 25, 0, 0, 0)
    data_segundo_turno = datetime(2026, 10, 25, 8, 0, 0)
    
    # Período de espera (da meia-noite do dia 25 até a abertura das urnas às 08:00)
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

    # Cenário padrão: Exibe o consolidado do 1º turno com brancos, nulos, total e horários
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
                "votos_validos": 51200000,
                "porcentagem": 48.1,
                "situacao": "CLASSIFICADO PARA O 2º TURNO"
            },
            {
                "nome": "Lula",
                "partido": "PT",
                "numero": 13,
                "votos_validos": 46800000,
                "porcentagem": 43.9,
                "situacao": "CLASSIFICADO PARA O 2º TURNO"
            }
        ]
    }
