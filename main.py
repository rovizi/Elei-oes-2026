from fastapi import FastAPI

app = FastAPI()

@app.get("/api/eleicoes/velas")
def obter_velas(uf: str = "br"):
    return {
        "uf": uf.upper(),
        "status_conexao": "APURACAO_1_TURNO_ENCERRADA",
        "eleicao_encerrada": False,
        "etapa_eleitoral": "Segundo Turno",
        "eleicao": {
            "data_primeiro_turno": "04/10/2026",
            "data_segundo_turno": "25/10/2026",
            "horario_votacao": "08:00 às 17:00",
            "fase": "1º Turno Encerrado - 2º Turno Agendado"
        },
        "totalizacao": {
            "status_geral": "1º Turno encerrado sem maioria absoluta. Segundo turno confirmado para 25/10/2026.",
            "aviso_apuracao": "Atenção: A votação no 2º turno ocorrerá das 8h às 17h. A apuração dos votos terá início a partir das 17h, estando sujeita a atrasos devido a filas e eleitores votando após o horário de encerramento.",
            "votos_computados": 115000000,
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
