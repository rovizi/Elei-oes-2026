from fastapi import FastAPI

from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/api/eleicoes/velas")
def obter_velas(uf: str = "br"):
    return {
        "uf": uf.upper(),
        "status_conexao": "APURACAO_1_TURNO_CONCLUIDA",
        "eleicao_encerrada": False,  # O processo eleitoral geral continua até o 2º turno
        "etapa_eleitoral": "Segundo Turno",
        "eleicao": {
            "data_primeiro_turno": "04/10/2026",
            "data_segundo_turno": "25/10/2026",
            "horario_votacao_2_turno": "08:00 às 17:00",
            "hora_consulta": datetime.now().strftime("%H:%M:%S"),
            "fase": "1º Turno Encerrado - 100% Apurado - 2º Turno Agendado"
        },
        "totalizacao": {
            "status_geral": "100% das urnas apuradas. Nao houve maioria absoluta no 1º turno. Segundo turno confirmado para 25/10/2026.",
            "aviso_apuracao": "Atenção: No 2º turno a votação ocorre das 8h às 17h. A apuração inicia-se após as 17h, estando sujeita a atrasos devido a filas nas seções eleitorais.",
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
