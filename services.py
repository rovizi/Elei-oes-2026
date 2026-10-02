from fastapi import FastAPI, Query, HTTPException
from typing import Optional

app = FastAPI()

def buscar_dados_completos(uf: str = "BR"):
    """Função exata que o main.py está tentando importar"""
    return {
      "uf": uf.upper() if uf else "BR",
      "status_conexao": "AGUARDANDO_PLEITO",
      "eleicao_encerrada": False,
      "eleicao": {
        "data_eleicao": "04/10/2026",
        "inicio_votacao": "08:00",
        "fim_votacao": "17:00 (Sujeito a tolerância de filas)",
        "inicio_apuracao": "Imediatamente após o encerramento geral das seções (17h00)"
      },
      "totalizacao": {
        "status_geral": "Aguardando encerramento da votação presencial às 17h00",
        "votos_computados": 0,
        "total_urnas_apuradas": "0 / 472.075"
      },
      "candidatos": [
        {
          "posicao": 1,
          "numero": 13,
          "nome": "Lula",
          "partido": "PT",
          "percentual": 0.0,
          "votos": "0 votos",
          "status_texto": "⚠️ ELEIÇÃO NESTE DOMINGO (04/10/2026) — PREPARAÇÃO EM ANDAMENTO",
          "cor_vela": "#ef4444",
          "cor_badge": "#F59E0B",
          "foto_url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9"
        },
        {
          "posicao": 2,
          "numero": 22,
          "nome": "Bolsonaro",
          "partido": "PL",
          "percentual": 0.0,
          "votos": "0 votos",
          "status_texto": "⚠️ ELEIÇÃO NESTE DOMINGO (04/10/2026) — PREPARAÇÃO EM ANDAMENTO",
          "cor_vela": "#22c55e",
          "cor_badge": "#F59E0B",
          "foto_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d"
        }
      ]
    }

@app.get("/")
def raiz():
    return {
        "status": "Online",
        "mensagem": "API Eleições Brasil pronta para rastrear pesquisas hoje e votos reais no domingo!"
    }

@app.get("/api/eleicoes/velas")
def get_velas_api_eleicoes_velas_get(uf: Optional[str] = Query("BR")):
    try:
        return buscar_dados_completos(uf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
