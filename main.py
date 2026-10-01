from fastapi import FastAPI
from services import buscar_dados_completos

app = FastAPI(
    title="Eleições Brasil",
    description="Acompanhamento visual em tempo real com velas dinâmicas, fotos, cores e congelamento automático pós-eleição.",
    version="1.0.0"
)

# Controle de estado para congelar a API ao fim da apuração
ESTADO_SISTEMA = {
    "congelado": False
}

@app.get("/")
def home():
    return {
        "status": "Online",
        "mensagem": "API Eleições Brasil pronta para rastrear pesquisas hoje e votos reais no domingo!"
    }

@app.get("/api/eleicoes/velas")
def get_velas(uf: str = "br"):
    """
    Retorna o painel com as velas dinâmicas, fotos e cores. 
    Para de atualizar automaticamente assim que o vencedor é declarado.
    """
    if ESTADO_SISTEMA["congelado"]:
        return {
            "aviso": "A apuração foi encerrada e o resultado foi congelado.",
            "dados_congelados": True
        }

    resultado = buscar_dados_completos(uf=uf)

    # Se o sistema detectar que a apuração chegou a 100% e há um eleito definido, trava o sistema
    if isinstance(resultado, dict) and resultado.get("eleicao_encerrada"):
        ESTADO_SISTEMA["congelado"] = True

    return resultado