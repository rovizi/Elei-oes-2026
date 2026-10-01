import time
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_ALVO = "https://g1.globo.com/politica/eleicoes/2026/apuracao/presidente.ghtml"

_cache_dados = {
    "timestamp": 0,
    "candidatos": []
}
TEMPO_CACHE = 60

FALLBACK_DATABASE = [
    {
        "nome": "Luiz Inácio Lula da Silva",
        "partido": "PT",
        "numero": 13,
        "posicao": 1,
        "percentual": 36.5,
        "votos": "45.120.300",
        "status_texto": "EM APURAÇÃO (MODO SEGURO)",
        "cor_vela": "#CC0000",
        "foto_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400",
    },
    {
        "nome": "Flávio Bolsonaro",
        "partido": "PL",
        "numero": 22,
        "posicao": 2,
        "percentual": 29.0,
        "votos": "35.800.100",
        "status_texto": "EM APURAÇÃO (MODO SEGURO)",
        "cor_vela": "#002D62",
        "foto_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
    }
]

def raspar_dados_eleitorais():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        response = requests.get(URL_ALVO, headers=headers, timeout=10)
        
        if response.status_code != 200:
            logger.warning(f"O site retornou status {response.status_code}. Usando fallback.")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        lista_candidatos = []
        
        cartoes_candidatos = soup.find_all("div", class_=["candidate-card", "bastian-feed-item", "entity-card"])

        if not cartoes_candidatos:
            return None

        for index, item in enumerate(cartoes_candidatos[:5], start=1):
            nome_elem = item.find(["div", "span", "h2"], class_=["name", "nome-candidato", "text"])
            partido_elem = item.find(["span", "div"], class_=["party", "sigla-partido"])
            votos_elem = item.find(["span", "div"], class_=["votes", "total-votos"])
            
            if nome_elem:
                nome = nome_elem.text.strip()
                partido = partido_elem.text.strip() if partido_elem else "POL"
                votos_str = votos_elem.text.strip() if votos_elem else "0"
                
                lista_candidatos.append({
                    "nome": nome,
                    "partido": partido,
                    "numero": index * 10,
                    "posicao": index,
                    "percentual": 0.0,
                    "votos": votos_str,
                    "status_texto": "AUTOMÁTICO (WEB SCRAPING)",
                    "cor_vela": "#2E7D32",
                    "foto_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400",
                })

        return lista_candidatos if lista_candidatos else None

    except Exception as e:
        logger.error(f"Erro no processo de scraping: {e}")
        return None

def obter_candidatos(uf: str = "br"):
    global _cache_dados
    tempo_atual = time.time()
    
    if _cache_dados["candidatos"] and (tempo_atual - _cache_dados["timestamp"] < TEMPO_CACHE):
        return _cache_dados["candidatos"]
    
    novos_dados = raspar_dados_eleitorais()
    
    if novos_dados:
        _cache_dados["candidatos"] = novos_dados
        _cache_dados["timestamp"] = tempo_atual
        return novos_dados
        
    if _cache_dados["candidatos"]:
        return _cache_dados["candidatos"]
        
    return FALLBACK_DATABASE
