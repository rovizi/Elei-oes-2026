from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import requests

try:
    import pytz
    fuso_br = pytz.timezone("America/Sao_Paulo")
except ImportError:
    fuso_br = None

app = FastAPI(
    title="API de Eleições Oficial - TSE",
    description="API FastAPI para apuração em tempo real com dados estritamente reais",
    version="3.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "API de Eleições TSE Oficial Rodando", 
        "rota_dados": "/api/eleicoes/velas"
    }

def buscar_dados_tse_real(uf: str):
    """
    Executa a requisição estritamente real nos servidores de divulgação do TSE.
    Retorna None se a conexão falhar, sem injetar dados fictícios.
    """
    try:
        # URL oficial padrão do TSE para o arquivo de totalização por UF (ex: br ou sp, etc.)
        url_tse = f"https://resultados.tse.jus.br/oficial/ele2026/dados/{uf.lower()}/{uf.lower()}-c0001-e000000-u.json"
        
        response = requests.get(url_tse, timeout=5)
        if response.status_code == 200:
            dados_brutos = response.json()
            
            # Mapeamento do JSON oficial do TSE para o formato consumido pelo seu front-end
            votos_computados = dados_brutos.get("V", 0)
            total_urnas = dados_brutos.get("S", "0 / 0")
            eleicao_encerrada = dados_brutos.get("ast", "N") == "F"
            
            candidatos_formatados = []
            for cand in dados_brutos.get("cand", []):
                candidatos_formatados.append({
                    "id": cand.get("seq"),
                    "nome": cand.get("nm"),
                    "partido": f"{cand.get('sg')} {cand.get('n')}",
                    "votos": cand.get("vap"),
                    "porcentagem": f"{cand.get('pvap')}%",
                    "status_texto": "Eleito" if cand.get("st") == "S" else "Apuração em Andamento",
                    "foto": "",
                    "cor_tag": "#30B0C7"
                })

            return {
                "eleicao_encerrada": eleicao_encerrada,
                "houve_segundo_turno": False,
                "votos_computados": votos_computados,
                "total_urnas_apuradas": total_urnas,
                "candidatos": candidatos_formatados
            }
    except Exception as e:
        print(f"Erro na requisição real ao TSE: {e}")
        
    return None

@app.get("/api/eleicoes/velas")
def get_velas_api_eleicoes_velas_get(uf: Optional[str] = Query("BR")):
    if fuso_br:
        agora = datetime.now(fuso_br)
    else:
        agora = datetime.now()

    # Executa a busca real diretamente na API do TSE
    try:
        dados_reais = buscar_dados_tse_real(uf)

        if not dados_reais:
            return {
                "uf": uf.upper() if uf else "BR",
                "status_conexao": "AGUARDANDO_DADOS_REAIS",
                "eleicao_encerrada": False,
                "eleicao": {
                    "data_eleicao": agora.strftime("%d/%m/%Y"),
                    "hora_consulta": agora.strftime("%H:%M:%S"),
                    "fase": "Aguardando Sincronização com o TSE"
                },
                "totalizacao": {
                    "status_geral": "Servidores do TSE ainda não liberaram os dados ou indisponíveis.",
                    "votos_computados": 0,
                    "total_urnas_apuradas": "0 / 0"
                },
                "candidatos": []
            }

        apuracao_100_por_cento = dados_reais.get("eleicao_encerrada", False)
        houve_segundo_turno = dados_reais.get("houve_segundo_turno", False)
        votos_computados = dados_reais.get("votos_computados", 0)
        total_urnas_apuradas = dados_reais.get("total_urnas_apuradas", "0 / 0")
        lista_candidatos = dados_reais.get("candidatos", [])
        
        if houve_segundo_turno:
            status_geral_texto = "⚠️ 2º Turno Definido"
            fase_atual = "Segundo Turno"
        elif apuracao_100_por_cento:
            status_geral_texto = "Eleição Encerrada - Votação Finalizada"
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
                "votos_computados": votos_computados,  
                "total_urnas_apuradas": total_urnas_apuradas  
            },
            "candidatos": lista_candidatos  
        }
        
    except Exception as e:
        return {
            "uf": uf.upper() if uf else "BR",
            "status_conexao": "ERRO_CONEXAO_TSE",
            "erro": str(e),
            "eleicao": {"fase": "Apuração"},
            "totalizacao": {"status_geral": "Erro crítico ao processar dados reais do TSE."},
            "candidatos": []
        }
