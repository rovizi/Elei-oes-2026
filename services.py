import time
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL oficial do TSE para apuração em tempo real (exemplo para eleições gerais/presidência)
# O TSE disponibiliza o JSON de totalização no portal de dados abertos/divulgacandcontas
URL_APURACAO_TSE = "https://resultados.tse.jus.br/oficial/ele2026/544/dados-simplificados/br/br-c0001-e000544-r.json"

_cache_dados = {
    "timestamp": 0,
    "candidatos": []
}
TEMPO_CACHE = 30 # Atualiza a cada 30 segundos durante a apuração

# Mapeamento fixo de segurança com as fotos oficiais e cores corretas
FOTOS_E_CORES = {
    "13": {
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Foto_oficial_de_Luiz_In%C3%A1cio_Lula_da_Silva_%28ombros%29_denoise.jpg",
        "cor_vela": "#CC0000"
    },
    "22": {
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2025/12/O-senador-Flavio-Bolsonaro-e1765906268178.jpg?w=1200&h=1200&crop=1",
        "cor_vela": "#002D62"
    }
}

FALLBACK_DATABASE = [
    {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "numero": 13,
        "posicao": 1,
        "percentual": 36.5,
        "votos": "45.120.300",
        "status_texto": "AGUARDANDO DADOS DO TSE",
        "cor_vela": "#CC0000",
        "foto_url": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Foto_oficial_de_Luiz_In%C3%A1cio_Lula_da_Silva_%28ombros%29_denoise.jpg",
    },
    {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "numero": 22,
        "posicao": 2,
        "percentual": 29.0,
        "votos": "35.800.100",
        "status_texto": "AGUARDANDO DADOS DO TSE",
        "cor_vela": "#002D62",
        "foto_url": "https://admin.cnnbrasil.com.br/wp-content/uploads/sites/12/2025/12/O-senador-Flavio-Bolsonaro-e1765906268178.jpg?w=1200&h=1200&crop=1",
    }
]

def buscar_apuracao_tse():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL_APURACAO_TSE, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None

        data = response.json()
        cand_raw = data.get("cand", [])
        
        if not cand_raw:
            return None

        lista_candidatos = []
        for i, item in enumerate(cand_raw[:2], start=1):
            numero = str(item.get("n"))
            nome = item.get("nm")
            votos = item.get("vap")
            percentual = float(item.get("pvap", "0").replace(",", "."))
            
            # Recupera a foto e a cor oficial mapeada para o número
            config = FOTOS_E_CORES.get(numero, {
                "foto_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400",
                "cor_vela": "#333333"
            })

            lista_candidatos.append({
                "nome": nome,
                "partido": item.get("sgp", "PARTIDO"),
                "numero": int(numero),
                "posicao": i,
                "percentual": percentual,
                "votos": f"{int(votos):,}".replace(",", "."),
                "status_texto": "APURAÇÃO OFICIAL TSE (AO VIVO)",
                "cor_vela": config["cor_vela"],
                "foto_url": config["foto_url"],
            })

        return lista_candidatos if lista_candidatos else None

    except Exception as e:
        logger.error(f"Erro ao buscar dados do TSE: {e}")
        return None

def obter_candidatos(uf: str = "br"):
    global _cache_dados
    tempo_atual = time.time()
    
    if _cache_dados["candidatos"] and (tempo_atual - _cache_dados["timestamp"] < TEMPO_CACHE):
        return _cache_dados["candidatos"]
    
    dados_reais = buscar_apuracao_tse()
    
    if dados_reais:
        _cache_dados["candidatos"] = dados_reais
        _cache_dados["timestamp"] = tempo_atual
        return dados_reais
        
    if _cache_dados["candidatos"]:
        return _cache_dados["candidatos"]
        
    return FALLBACK_DATABASE

def buscar_dados_completos(uf: str = "br"):
    return obter_candidatos(uf)
